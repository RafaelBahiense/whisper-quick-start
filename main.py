import warnings
import whisper
import os
import json
from pathlib import Path
from typing import Optional, Tuple
from tkinter import Tk, filedialog, StringVar
from tkinter import ttk
import torch

warnings.filterwarnings("ignore")


CONFIG_FILE = "config.json"

if os.name == "nt":
    WHISPER_CACHE_DIR = Path(os.getenv("LOCALAPPDATA", Path.home() / ".cache")) / "whisper"
else:
    WHISPER_CACHE_DIR = Path.home() / ".cache" / "whisper"

MODEL_OPTIONS = [
    ("tiny (Multilingual)", "tiny"),
    ("tiny.en (English-only)", "tiny.en"),
    ("base (Multilingual)", "base"),
    ("base.en (English-only)", "base.en"),
    ("small (Multilingual)", "small"),
    ("small.en (English-only)", "small.en"),
    ("medium (Multilingual)", "medium"),
    ("medium.en (English-only)", "medium.en"),
    ("large (Multilingual)", "large"),
    ("turbo (Multilingual)", "turbo")
]

LANGUAGE_OPTIONS = [
    ("English", "en"),
    ("Portuguese (Brazil)", "pt"),
    ("Spanish", "es"),
    ("French", "fr"),
    ("German", "de"),
    ("Italian", "it"),
    ("Chinese", "zh"),
    ("Japanese", "ja"),
]

OUTPUT_FORMAT_OPTIONS = [
    ("SRT (SubRip)", "srt"),
    ("TXT (Plain Text)", "txt")
]

def load_config() -> dict:
    """
    Load the user's previous selections from the configuration file.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    return {
        "model": MODEL_OPTIONS[0][1],
        "language": LANGUAGE_OPTIONS[0][1],
        "output_format": OUTPUT_FORMAT_OPTIONS[0][1]
    }

def save_config(config: dict):
    """
    Save the user's selections to the configuration file.
    """
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def get_downloaded_models() -> list:
    """
    Check which Whisper models are already downloaded.
    """
    return [f.stem for f in WHISPER_CACHE_DIR.glob("*.bin")] if WHISPER_CACHE_DIR.exists() else []

_loaded_models = {}

def get_model(model_name: str):
    """
    Load the Whisper model with caching.
    If available, move model to GPU.
    """
    if model_name not in _loaded_models:
        print(f"Loading Whisper model: {model_name}...")
        model = whisper.load_model(model_name)
        if torch.cuda.is_available():
            print("cuda avaliable")
            model = model.to("cuda")
        _loaded_models[model_name] = model
    return _loaded_models[model_name]

def choose_options_gui() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Open a GUI window with three dropdowns:
      - Whisper model
      - Transcription language
      - Output format (SRT or TXT)
    Returns (model_name, language_code, output_format).
    If the user cancels, returns (None, None, None).
    """
    previous_config = load_config()
    downloaded_models = get_downloaded_models()

    root = Tk()
    root.title("Select Options")
    root.geometry("360x320")

    style = ttk.Style(root)
    style.theme_use("clam")

    selected = {"model": None, "language": None, "output_format": None}

    def on_ok():
        selected_model_label = model_var.get().split(" (Downloaded)")[0].strip()
        selected_language_label = lang_var.get()
        selected_output_format_label = output_format_var.get()

        selected["model"] = next((val for (label, val) in MODEL_OPTIONS if label == selected_model_label), None)
        selected["language"] = next((val for (label, val) in LANGUAGE_OPTIONS if label == selected_language_label), None)
        selected["output_format"] = next((val for (label, val) in OUTPUT_FORMAT_OPTIONS if label == selected_output_format_label), None)

        save_config(selected)
        root.destroy()

    def on_cancel():
        root.destroy()

    main_frame = ttk.Frame(root, padding="10 10 10 10")
    main_frame.pack(fill="both", expand=True)

    model_label = ttk.Label(main_frame, text="Select Whisper Model:")
    model_label.pack(pady=(10, 5))
    model_var = StringVar(value=next((label for (label, val) in MODEL_OPTIONS if val == previous_config.get("model", MODEL_OPTIONS[0][1])), MODEL_OPTIONS[0][0]))
    model_values = [f"{label} {'(Downloaded)' if val in downloaded_models else ''}" for (label, val) in MODEL_OPTIONS]
    model_cb = ttk.Combobox(
        main_frame,
        textvariable=model_var,
        values=model_values,
        state="readonly"
    )
    model_cb.pack(pady=(0, 10))

    lang_label = ttk.Label(main_frame, text="Select Language:")
    lang_label.pack(pady=(10, 5))
    lang_var = StringVar(value=next((label for (label, val) in LANGUAGE_OPTIONS if val == previous_config.get("language", LANGUAGE_OPTIONS[0][1])), LANGUAGE_OPTIONS[0][0]))
    lang_cb = ttk.Combobox(
        main_frame,
        textvariable=lang_var,
        values=[opt[0] for opt in LANGUAGE_OPTIONS],
        state="readonly"
    )
    lang_cb.pack(pady=(0, 10))

    output_format_label = ttk.Label(main_frame, text="Select Output Format:")
    output_format_label.pack(pady=(10, 5))
    output_format_var = StringVar(value=next((label for (label, val) in OUTPUT_FORMAT_OPTIONS if val == previous_config.get("output_format", OUTPUT_FORMAT_OPTIONS[0][1])), OUTPUT_FORMAT_OPTIONS[0][0]))
    output_format_cb = ttk.Combobox(
        main_frame,
        textvariable=output_format_var,
        values=[opt[0] for opt in OUTPUT_FORMAT_OPTIONS],
        state="readonly"
    )
    output_format_cb.pack(pady=(0, 10))

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=(10, 0))
    ok_button = ttk.Button(button_frame, text="OK", command=on_ok)
    ok_button.pack(side="left", padx=(5, 5))
    cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_button.pack(side="left", padx=(5, 5))
    button_frame.pack(anchor="center")

    root.mainloop()
    return selected["model"], selected["language"], selected["output_format"]

def select_file() -> Optional[str]:
    """
    Open a file dialog to select an audio file.
    Returns the selected file path or None if canceled.
    """
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an audio file",
        filetypes=[("Audio files", "*.m4a *.mp3 *.wav *.ogg *.flac *.aac")]
    )
    return file_path

def save_output(output_format: str) -> Optional[str]:
    """
    Open a file dialog to select the output file location.
    Sets the default extension based on the output format.
    Returns the selected file path or None if canceled.
    """
    root = Tk()
    root.withdraw()
    if output_format == "srt":
        filetypes = [("Subtitle files", "*.srt")]
        def_ext = ".srt"
    else:
        filetypes = [("Text files", "*.txt")]
        def_ext = ".txt"
    file_path = filedialog.asksaveasfilename(
        title="Save transcription as",
        defaultextension=def_ext,
        filetypes=filetypes
    )
    return file_path

def format_timestamp(seconds: float) -> str:
    """
    Format seconds into SRT timestamp format (HH:MM:SS,mmm).
    """
    millis = int((seconds - int(seconds)) * 1000)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02},{millis:03}"

def transcribe_audio() -> None:
    """
    Main function to:
      1. Let the user select model, language, and output format.
      2. Pick an audio file and output file location.
      3. Perform transcription.
      4. Save the transcription in the selected format.
    """
    model_name, lang_code, output_format = choose_options_gui()
    if not model_name or not lang_code or not output_format:
        print("One or more selections were not made. Exiting.")
        return

    audio_file = select_file()
    if not audio_file:
        print("No audio file selected. Exiting.")
        return

    output_file = save_output(output_format)
    if not output_file:
        print("No output file selected. Exiting.")
        return

    # Load the model (with caching and GPU support)
    model = get_model(model_name)

    language_name = whisper.tokenizer.LANGUAGES.get(lang_code, "Unknown")
    print(f"Transcribing audio in language: {language_name}...")

    result = model.transcribe(audio_file, language=lang_code, verbose=False)

    if output_format == "srt":
        # Write SRT output with minimal extra newlines
        with open(output_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"]):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                f.write(f"{i + 1}\n")
                f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                f.write(f"{text}\n")
                # Write a single blank line between segments except after the last one
                if i < len(result["segments"]) - 1:
                    f.write("\n")
    else:
        transcript = " ".join(segment["text"].strip() for segment in result["segments"])
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)

    print(f"Transcription saved to {output_file}")

if __name__ == "__main__":
    transcribe_audio()
