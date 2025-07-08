from TTS.api import TTS

# Load xtts_v2 model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# Print available speakers
print("Available speakers:", tts.speakers)
