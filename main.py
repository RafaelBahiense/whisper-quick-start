import whisper
import warnings
from tkinter import Tk, filedialog

warnings.filterwarnings("ignore")

def select_file():
    """Opens a file dialog to select an audio file."""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an audio file",
        filetypes=[("Audio files", "*.m4a *.mp3 *.wav *.ogg *.flac *.aac")]
    )
    return file_path

def save_output():
    """Opens a file dialog to select the output file location."""
    root = Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="Save transcription as",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    return file_path

def choose_model():
    """Prompts the user to select a Whisper model."""
    models = {
        "1": "tiny",
        "2": "tiny.en",
        "3": "base",
        "4": "base.en",
        "5": "small",
        "6": "small.en",
        "7": "medium",
        "8": "medium.en",
        "9": "large",
        "10": "turbo"
    }

    print("Select a Whisper model:")
    print("1. tiny       (Multilingual, ~1GB VRAM, ~10x speed)")
    print("2. tiny.en    (English-only, ~1GB VRAM, ~10x speed)")
    print("3. base       (Multilingual, ~1GB VRAM, ~7x speed)")
    print("4. base.en    (English-only, ~1GB VRAM, ~7x speed)")
    print("5. small      (Multilingual, ~2GB VRAM, ~4x speed)")
    print("6. small.en   (English-only, ~2GB VRAM, ~4x speed)")
    print("7. medium     (Multilingual, ~5GB VRAM, ~2x speed)")
    print("8. medium.en  (English-only, ~5GB VRAM, ~2x speed)")
    print("9. large      (Multilingual, ~10GB VRAM, ~1x speed)")
    print("10. turbo     (Multilingual, ~6GB VRAM, ~8x speed)")

    choice = input("Enter the number corresponding to your choice: ").strip()
    while choice not in models:
        print("Invalid choice. Please select a valid model.")
        choice = input("Enter the number corresponding to your choice: ").strip()

    return models[choice]

def transcribe_audio():
    """Main function to transcribe audio."""
    audio_file = select_file()
    if not audio_file:
        print("No audio file selected.")
        return

    output_file = save_output()
    if not output_file:
        print("No output file selected.")
        return

    model_name = choose_model()

    print(f"Loading Whisper model: {model_name}...")
    model = whisper.load_model(model_name)
    
    print("Transcribing audio...")
    result = model.transcribe(audio_file, verbose=False)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"Transcription saved to {output_file}")

if __name__ == "__main__":
    transcribe_audio()
