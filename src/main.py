from core.audio import AudioService
from core.llm import LLMFactory
import asyncio
import pyaudio
import openwakeword
from openwakeword.model import Model
import numpy as np
from config.config import config
from pathlib import Path

async def main(llm_service, audio_service):
    RATE: int = 16000
    CHANNELS = 1
    FRAMES = 1280

    current_dir = Path(__file__).parent # Get current file path
    model_path = str(current_dir / 'models' / 'Hey_Jarvis.onnx') # Build absolute path

    model = Model(wakeword_model_paths=[model_path])
    audio = pyaudio.PyAudio()

    print("Bear is listening...")

    try:
        while True:
            # Create the stream only for this "waiting" cycle
            stream = audio.open(rate=RATE, channels=CHANNELS, format=pyaudio.paInt16, input=True, frames_per_buffer=FRAMES)
            model.reset()

            # Wake Word detection loop
            while True:

                array = np.frombuffer(stream.read(FRAMES), dtype=np.int16)
                wake_word = model.predict(array)
                
                if wake_word['Hey_Jarvis'] >= 0.5:
                    print("Bear woke up!")
                    model.reset()
                    stream.stop_stream()
                    stream.close()
                    break # Exit waiting loop
            
            # --- Command Logic ---
            recorded_audio = audio_service.record_audio()
            
            if recorded_audio:
                transcribed_text = audio_service.transcribe(recorded_audio)
                print("--- Transcribed: ---", transcribed_text)
                if transcribed_text:
                    response = llm_service.send_query(transcribed_text)
                    await audio_service.play_audio(response)
            
            # The loop restarts and recreates the stream above
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        audio.terminate()

if __name__ == '__main__':
    llm_service = LLMFactory.get_llm_service(config.LLM_PROVIDER)
    audio_service = AudioService()
    asyncio.run(main(llm_service, audio_service))