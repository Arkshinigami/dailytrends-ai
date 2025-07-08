# 🎙️ Daily Trend Talk — Automated AI Podcast

> **An AI-powered podcast delivering daily insights on Indian tech, science, and global developments.**  
> No manual editing, no fluff — just news turned into voice with LLaMA 3 + Coqui TTS.

---

## 🔒 Source Code Access

This repository documents the architecture, usage, and publishing details of the **Daily Trend Talk** podcast.  
The core automation code is **not open-sourced** at this time.

💬 Want access or collaboration? [Contact me directly](mailto:arkgrimreaper123@gamil.com)  
❤️ Support the project on [Patreon](patreon.com/TechEkta)

---

## 🎧 Listen to the Podcast

- **RSS Feed:** https://your.github.io/repo-name/media/feed.xml
- **Spotify:** (Add your Spotify link here if available)
- **GitHub Pages:** https://your.github.io/repo-name

---

## 🔧 Project Highlights

- ✅ Automated script generation with **LLaMA 3.1** (via Ollama)
- 🎤 Voice synthesis via **Coqui TTS**
- 📡 Pulls headlines from:
  - BBC News
  - NASA Breaking News
  - PIB (India): Tech, Science, and Economic Affairs
- 🧠 Filters and ranks stories using AI
- 🖼️ Auto-generates episode cover art
- 📢 Publishes RSS feed via GitHub Pages

---

## 🗂️ Directory Structure

docs/
├── media/             # Podcast audio + cover art  
├── feed.xml           # Auto-generated RSS feed  
data/
├── good/              # Accepted scripts  
├── bad/               # Rejected/low quality  
├── processed/         # Deduplication tracking  

---

## 🚀 Automation Stack

| Component           | Tool/Tech            |
|---------------------|----------------------|
| Script Generation   | LLaMA 3.1 via Ollama |
| Text-to-Speech      | Coqui TTS            |
| Audio Handling      | pydub + ffmpeg       |
| RSS Feed Builder    | feedgen              |
| Host & Git Sync     | GitHub Pages         |

---

## 💸 Support the Project

If this project helps you, inspires you, or saves you time — consider supporting it:

[![Patreon](https://img.shields.io/badge/❤️-Support_on_Patreon-orange)](https://patreon.com/TechEkta)

Every contribution helps us upgrade the pipeline, explore more stories, and deliver better audio quality and bonus content.

---

## 📌 Notes

- All sources used are public and copyright-safe  
- Episodes are published daily (auto-run via scheduled script)  
- Want to build your own? Reach out on Patreon for a behind-the-scenes tier  

---

## 📬 Contact

📧 arkgrimreaper123@gamil.com 
🌐 patreon.com/TechEkta
