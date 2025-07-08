# llama_api.py
"""
Shared API client for local Ollama-powered LLaMA 3.1 server.
"""
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"

def llama_generate(prompt: str) -> str:
    """
    Send a prompt to local Ollama server and return the generated text response.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json().get("response", "")

# build_podcast.py
"""
Automated Podcast Pipeline using shared LLaMA API:
1. git pull
2. Fetch headlines from RSS sources
3. Skip processed
4. Generate scripts via llama_api.llama_generate()
5. Synthesize audio (Coqui TTS)
6. Create cover art
7. Classify good/bad content
8. Select best candidate
9. Build RSS feed
10. git commit & push
"""
import os
import random
import sys
import subprocess
import json
import random
import textwrap
import feedparser
import numpy as np
from scipy.io.wavfile import write
from llama_api import llama_generate
from TTS.api import TTS
from pydub import AudioSegment, effects, silence
from PIL import Image, ImageDraw, ImageFont
from feedgen.feed import FeedGenerator

# Ensure eSpeak & FFmpeg on PATH
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\eSpeak\command_line"
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# Configuration
RSS_SOURCES = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://pib.gov.in/rssfeed/technology.aspx",
    "https://pib.gov.in/rssfeed/science_technology.aspx",
    "https://pib.gov.in/rssfeed/economic_affairs.aspx",
]
PROCESSED_FILE = "data/processed/processed.json"
GOOD_DIR = "data/good"
BAD_DIR = "data/bad"
MEDIA_DIR = "docs/media"
FEED_FILE = "docs/feed.xml"
PODCAST_TITLE = "Insight Echo: Daily Trends"
BASE_URL = "https://arkshinigami.github.io/dailytrends-ai/media"
MIN_WORDS = 300
MIN_DURATION = 180  # seconds
MAX_CANDIDATES = 3

# Helpers
def run_cmd(cmd):
    """Run a shell command and warn on failure without stopping the script."""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[WARNING] Command {cmd} failed: {e}")

# Create needed dirs
def ensure_dirs():
    for path in [os.path.dirname(PROCESSED_FILE), GOOD_DIR, BAD_DIR, MEDIA_DIR]:
        os.makedirs(path, exist_ok=True)

# Load/save processed headlines
def load_processed():
    if not os.path.exists(PROCESSED_FILE):
        return set()
    return set(json.load(open(PROCESSED_FILE, 'r', encoding='utf8')))

def save_processed(done):
    json.dump(list(done), open(PROCESSED_FILE, 'w', encoding='utf8'), indent=2)

# Collect new headlines
def collect_headlines():
    done = load_processed()
    candidates = []
    for url in RSS_SOURCES:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title.strip()
            if title and title not in done and title not in candidates:
                candidates.append(title)
                break
        if len(candidates) >= MAX_CANDIDATES:
            break
    return candidates

# Initialize TTS model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# Podcast audio synthesis
def synthesize(script: str, path: str):
    speakers = ["Gracie Wise", "Daisy Studious", "Andrew Chipper"]
    selected = random.choice(speakers)
    print(f"[INFO] Using speaker: {selected}")

    parts = textwrap.wrap(script, width=240)
    combined = AudioSegment.empty()

    for part in parts:
        wav = tts.tts(part, speaker=selected, language="en")
        write("temp.wav", 22050, np.array(wav))
        audio = AudioSegment.from_wav("temp.wav")
        audio = audio.set_frame_rate(22050).set_channels(1).set_sample_width(2)
        pause = AudioSegment.silent(duration=300, frame_rate=22050)
        pause = pause.set_channels(1).set_sample_width(2)
        combined += audio + pause

    norm = effects.normalize(combined)
    norm.export(path, format='mp3')
    return norm.duration_seconds, len(script.split())

# Generate cover art
def make_cover(title: str, path: str):
    w, h = 1400, 1400
    img = Image.new('RGB', (w, h)); draw = ImageDraw.Draw(img)
    for y in range(h):
        ratio = y / h
        r = int(255 * (1 - ratio) + 30 * ratio)
        g = int(255 * (1 - ratio) + 60 * ratio)
        b = int(255 * (1 - ratio) + 180 * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 120))
    img = Image.alpha_composite(img.convert('RGBA'), overlay)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arialbd.ttf", 80)
    tw, th = draw.textsize(title, font)
    draw.text(((w - tw) / 2, (h - th) / 2), title, fill='white', font=font)
    img.convert('RGB').save(path)

# Build RSS feed
def build_feed():
    fg = FeedGenerator()
    fg.title(PODCAST_TITLE)
    fg.link(href=BASE_URL, rel='self')
    fg.description('Automated daily trend podcast')
    for fn in sorted(os.listdir(MEDIA_DIR)):
        if not fn.endswith('.mp3'): continue
        fe = fg.add_entry()
        fe.id(f"{BASE_URL}/{fn}")
        fe.title(os.path.splitext(fn)[0])
        fe.description('Support on Patreon: https://patreon.com/TechEkta')
        fe.enclosure(f"{BASE_URL}/{fn}", 0, 'audio/mpeg')
    fg.rss_file(FEED_FILE)

# Main
if __name__ == '__main__':
    run_cmd(['git', 'pull'])
    ensure_dirs()
    processed = load_processed()
    headlines = collect_headlines()
    results = []
    for title in headlines:
        script = llama_generate(f"Write a 5-minute podcast script on: '{title}'. Include intro, 3 points, closing.")
        mp3 = os.path.join(MEDIA_DIR, f"{title}.mp3")
        dur, words = synthesize(script, mp3)
        folder = GOOD_DIR if words >= MIN_WORDS and dur >= MIN_DURATION else BAD_DIR
        with open(os.path.join(folder, f"{title}.txt"), 'w', encoding='utf8') as f:
            f.write(script)
        results.append((title, words, dur))
        processed.add(title)
    if results:
        good = [r for r in results if r[1] >= MIN_WORDS and r[2] >= MIN_DURATION]
        if good:
            best = max(good, key=lambda x: x[1])
            make_cover(best[0], os.path.join(MEDIA_DIR, f"{best[0]}.png"))
    build_feed()
    save_processed(processed)
    run_cmd(['git', 'add', '.'])
    run_cmd(['git', 'commit', '-m', f"Auto-publish batch: {', '.join(headlines)}"])
    run_cmd(['git', 'push'])
    print("Done. Processed:", headlines)
