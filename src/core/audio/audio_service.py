import speech_recognition as sr
from groq import Groq
from typing import Any
import edge_tts as et
import subprocess
import shutil
from config.config import config

class AudioService():

    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.recognizer = sr.Recognizer()

        self._config_recognizer()

        # Changed to English voice
        self.voice = 'en-US-AriaNeural'

        self._check_dependencies()

    def _check_dependencies(self):
        self.mpv_path = shutil.which("mpv")
        if not self.mpv_path:
            raise RuntimeError("MPV player not found. Install it with 'sudo apt install mpv'")

    def _config_recognizer(self):
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 1.0
        self.recognizer.dynamic_energy_threshold = True

    def record_audio(self):
        with sr.Microphone() as source:
            print("\n--- Listening... (Speak now) ---")
            
            # Adjusts for background noise (only 0.4s to be fast)
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            
            try:
                # 1. Capture audio (with timeout to avoid freezing)
                # timeout=5: Waits up to 5s for you to start speaking
                # phrase_time_limit=30: Cuts off if you speak for more than 30s
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=30)
                audio_data = audio.get_wav_data()
                memory_file = ("audio.wav", audio_data)

                return memory_file

            except sr.WaitTimeoutError:
                print("No speech detected (timeout).")
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except Exception as e:
                print(f"Error: {e}")

    def transcribe(self, file: tuple[str, Any]):
        return self.client.audio.transcriptions.create(
                    file=file,
                    model="whisper-large-v3", # The most accurate model
                    prompt="The audio is in English.", # Optional context helps with accuracy
                    response_format="text",
                    language="en" # Force English
                )

    async def play_audio(self, text: str):
        
        tts = et.Communicate(text, self.voice)
        
        # Starts mpv expecting data via stdin
        cmd = [self.mpv_path, "--no-cache", "--no-terminal", "--", "-"]
        
        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            async for chunk in tts.stream():
                if chunk["type"] == "audio":
                    process.stdin.write(chunk["data"])
                    process.stdin.flush()
            
            if process.stdin:
                process.stdin.close()
            process.wait()
                
        except Exception as e:
            print(f"Error in audio stream: {e}")
