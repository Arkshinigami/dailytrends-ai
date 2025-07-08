from TTS.api import TTS

def list_available_models():
    print("Fetching list of available TTS models...\n")
    models = TTS.list_models()
    for idx, model in enumerate(models):
        print(f"{idx+1}. {model}")
    return models

def inspect_model(model_name):
    print(f"\nLoading model: {model_name} ...")
    try:
        tts = TTS(model_name=model_name)
        print("\n✅ Model loaded successfully!")

        # Show supported speakers
        if hasattr(tts, 'speakers') and tts.speakers:
            print("\n🗣 Available Speakers:")
            for speaker in tts.speakers:
                print(f"- {speaker}")
        else:
            print("\n🗣 Single-speaker model")

        # Show supported languages
        if hasattr(tts, 'languages') and tts.languages:
            print("\n🌐 Supported Languages:")
            for lang in tts.languages:
                print(f"- {lang}")
        else:
            print("\n🌐 Language: Default / English")
    except Exception as e:
        print(f"\n❌ Failed to load model: {e}")

if __name__ == "__main__":
    models = list_available_models()

    index = input("\nEnter the number of the model to inspect (e.g., 1): ").strip()
    try:
        selected = models[int(index) - 1]
        inspect_model(selected)
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
