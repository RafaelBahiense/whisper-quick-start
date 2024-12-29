# Whisper quick start

This tool allows you to transcribe audio files into text using OpenAI's Whisper model. It features a graphical interface for file selection, customizable model options, and output location.

---

## Features
- **File selection:** GUI-based file selection for input audio and output text files.
- **Model selection:** Choose from a variety of Whisper models based on your hardware and speed preferences.

---

## Installation Instructions

### Step 1: Install `uv`
This project uses **`uv`** to run the application. Install `uv` by following the instructions on the [uv repository](https://github.com/astral-sh/uv).

1. Visit the [uv GitHub page](https://github.com/astral-sh/uv).
2. Download the latest version for your platform.
3. Follow the instructions provided in the repository for installation.

Verify the installation by running:
```bash
uv --version
```

### Step 2: Install `ffmpeg`
The transcription process requires `ffmpeg` for audio processing. Follow the platform-specific instructions below:

#### Windows
1. Use **[Chocolatey](https://chocolatey.org/)** to install `ffmpeg`:
   ```bash
   choco install ffmpeg
   ```
   If Chocolatey is not installed, follow the [official guide](https://chocolatey.org/install) to set it up.

2. Verify installation:
   ```bash
   ffmpeg -version
   ```

#### macOS
1. Use **Homebrew** to install `ffmpeg`:
   ```bash
   brew install ffmpeg
   ```
   If Homebrew is not installed, install it by following the instructions at [brew.sh](https://brew.sh/).

2. Verify installation:
   ```bash
   ffmpeg -version
   ```

#### Linux
1. Use your package manager to install `ffmpeg`:
   - **Debian/Ubuntu:**
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
   - **Fedora:**
     ```bash
     sudo dnf install ffmpeg
     ```
   - **Arch:**
     ```bash
     sudo pacman -S ffmpeg
     ```

2. Verify installation:
   ```bash
   ffmpeg -version
   ```

---

## Running the Project
1. Navigate to the directory containing the project files.
2. Run the project using:
   ```bash
   uv run main.py
   ```
   This will start the tool and allow you to select an audio file, choose a model, and specify an output location.

---

## Model Details
For detailed information on the Whisper models, including their size, VRAM requirements, and relative speed, refer to the [Whisper README section on available models and languages](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages).

---

## Notes
- Ensure `ffmpeg` is installed and accessible from the command line.
- Choose a Whisper model based on your system's VRAM and performance requirements.

---

## License
This project is licensed under the GLWT Public License. See [LICENSE](LICENSE) for details.