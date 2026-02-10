# 🐻 B.E.A.R. Assistant

> **B**ernardo's **E**lectronic **A**ssistant **R**obot

A personal, modular, and LLM-agnostic voice assistant designed to run efficiently on Linux.

## 🚀 Features

- **Offline Wake Word:** Instant activation with "Bear" using Picovoice Porcupine (no audio sent to the cloud constantly).
- **Natural Voice:** High-quality neural Text-to-Speech (Edge TTS).
- **Fast Hearing:** Near real-time transcription with Groq + Whisper.
- **Agnostic Brain:**
  - Native support for **Google Gemini 2.5 Flash** (fast and free).
  - Support for **OpenAI GPT-4o** (optional).
  - SOLID architecture ready for any other model.
- **Docker Ready:** Runs containerized without headaches.

## 🛠️ Installation

### Prerequisites
- Python 3.12+
- `mpv` (audio player): `sudo apt install mpv`
- `portaudio19-dev` (for microphone): `sudo apt install portaudio19-dev`

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/bear.git
   cd bear
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure keys:
   Copy the example file:
   ```bash
   cp .env.example .env
   ```
   Fill `.env` with your API keys (Groq, Picovoice, Gemini/OpenAI).

## 🎮 Usage

### Running Locally
```bash
python src/main.py
```

## 🧠 AI Configuration

You can swap Bear's "brain" simply by changing a variable in `.env`:

**To use Gemini (Default):**
```ini
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
```

**To use GPT:**
```ini
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_aqui
```