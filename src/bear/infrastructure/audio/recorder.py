import speech_recognition as sr
from bear.domain.models import AudioPayload
from bear.domain.interfaces.audio_recorder import IAudioRecorder
from bear.domain.exceptions import AudioCaptureError

class SpeechRecognitionRecorder(IAudioRecorder):
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self._config_recognizer()
            
    def _config_recognizer(self):
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 1.0
        self.recognizer.dynamic_energy_threshold = True

    def record_audio(self) -> AudioPayload | None:
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
                memory_file = AudioPayload(filename="audio.wav", data=audio_data)

                return memory_file

            except sr.WaitTimeoutError:
                print("No speech detected (timeout).")
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except Exception as e:
                raise AudioCaptureError(f"Failed to capture Audio: {e}")