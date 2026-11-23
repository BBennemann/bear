import pyaudio
import numpy as np

from openwakeword.model import Model
from pathlib import Path

from bear.domain.interfaces.wake_word import IWakeWord
from bear.domain.exceptions import WakeWordError

class OpenWakeWordDetector(IWakeWord):

    def __init__(self, model_path: Path, threshold: float = 0.5):

        self.RATE: int = 16000
        self.CHANNELS = 1
        self.FRAMES = 1280

        self.audio = pyaudio.PyAudio()
        self.model = Model(wakeword_model_paths=[str(model_path)])
        self.threshold = threshold

    def listen_wake_word(self) -> None:
        # Create the stream only for this "waiting" cycle
        stream = self.audio.open(rate=self.RATE, channels=self.CHANNELS, format=pyaudio.paInt16, input=True, frames_per_buffer=self.FRAMES)
        self.model.reset()

        # Wake Word detection loop
        try:
            while True:

                array = np.frombuffer(stream.read(self.FRAMES), dtype=np.int16)
                wake_word = self.model.predict(array)
                
                if wake_word['Hey_Jarvis'] >= self.threshold:
                    print("Bear woke up!")
                    break # Exit waiting loop
        
        except Exception as e:
            raise WakeWordError(f"Wake word detection failed: {e}")
        
        finally:
            self.model.reset()
            stream.stop_stream()
            stream.close()

    def terminate(self) -> None:
        self.audio.terminate()