import warnings
import whisper
from typing import Optional, Tuple
from tkinter import Tk, filedialog, StringVar
from tkinter import ttk

warnings.filterwarnings("ignore")

# List of models to display in the dropdown (label, value)
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

# List of languages to display in the dropdown (label, code)
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

def choose_model_and_language_gui() -> Tuple[Optional[str], Optional[str]]:
    """
    Open a GUI window with two dropdowns (ttk.Combobox):
      - One for selecting the Whisper model
      - One for selecting the transcription language
    Returns (model_name, language_code).
    If the user closes the window or hits 'Cancel', returns (None, None).
    """

    root = Tk()
    root.title("Select Model and Language")
    root.geometry("320x220")

    style = ttk.Style(root)
    style.theme_use("clam")

    selected = {"model": None, "language": None}

    def on_ok():
        selected_model_label = model_var.get()
        selected_language_label = lang_var.get()

        selected["model"] = next((val for (label, val) in MODEL_OPTIONS if label == selected_model_label), None)
        selected["language"] = next((val for (label, val) in LANGUAGE_OPTIONS if label == selected_language_label), None)
        root.destroy()

    def on_cancel():
        root.destroy()

    main_frame = ttk.Frame(root, padding="10 10 10 10")
    main_frame.pack(fill="both", expand=True)

    model_label = ttk.Label(main_frame, text="Select Whisper Model:")
    model_label.pack(pady=(10, 5))

    model_var = StringVar(value=MODEL_OPTIONS[0][0])
    model_cb = ttk.Combobox(
        main_frame,
        textvariable=model_var,
        values=[opt[0] for opt in MODEL_OPTIONS],
        state="readonly"
    )
    model_cb.pack(pady=(0, 10))
    model_cb.current(0)

    lang_label = ttk.Label(main_frame, text="Select Language:")
    lang_label.pack(pady=(10, 5))

    lang_var = StringVar(value=LANGUAGE_OPTIONS[0][0])
    lang_cb = ttk.Combobox(
        main_frame,
        textvariable=lang_var,
        values=[opt[0] for opt in LANGUAGE_OPTIONS],
        state="readonly"
    )
    lang_cb.pack(pady=(0, 10))
    lang_cb.current(0)

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=(10, 0))

    ok_button = ttk.Button(button_frame, text="OK", command=on_ok)
    ok_button.pack(side="left", padx=(5, 5))

    cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
    cancel_button.pack(side="left", padx=(5, 5))

    button_frame.pack(anchor="center")

    root.mainloop()

    return selected["model"], selected["language"]


def select_file() -> Optional[str]:
    """
    Opens a file dialog to select an audio file.
    Returns the selected file path or None if canceled.
    """
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an audio file",
        filetypes=[("Audio files", "*.m4a *.mp3 *.wav *.ogg *.flac *.aac")]
    )
    return file_path


def save_output() -> Optional[str]:
    """
    Opens a file dialog to select the output file location.
    Returns the selected file path or None if canceled.
    """
    root = Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        title="Save transcription as",
        defaultextension=".srt",
        filetypes=[("Subtitle files", "*.srt")]
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
    1. Let user pick model & language (GUI).
    2. Let user pick audio file & output file location.
    3. Perform the transcription with timestamps.
    4. Save the transcription in SRT format.
    """

    model_name, lang_code = choose_model_and_language_gui()
    if not model_name or not lang_code:
        print("Model or language was not selected. Exiting.")
        return

    audio_file = select_file()
    if not audio_file:
        print("No audio file selected. Exiting.")
        return

    output_file = save_output()
    if not output_file:
        print("No output file selected. Exiting.")
        return

    print(f"Loading Whisper model: {model_name}...")
    model = whisper.load_model(model_name)

    language_name = whisper.tokenizer.LANGUAGES.get(lang_code, "Unknown")

    print(f"Transcribing audio in language: {language_name}...")
    result = model.transcribe(audio_file, language=lang_code, verbose=False)

    with open(output_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"]):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            f.write(f"{i + 1}\n")
            f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            f.write(f"{text}\n\n")

    print(f"Transcription saved to {output_file}")


if __name__ == "__main__":
    transcribe_audio()
