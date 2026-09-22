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
    RATE = 16000
    CHANNELS = 1
    FRAMES = 1280

    current_dir = Path(__file__).parent # Pega o caminho do arquivo atual
    model_path = str(current_dir / 'models' / 'Hey_Jarvis.onnx') # Constrói o caminho absoluto

    model = Model(wakeword_model_paths=[model_path])
    audio = pyaudio.PyAudio()

    print("Bear está ouvindo...")

    try:
        while True:
            # Cria o gravador apenas para esse ciclo de "espera"
            stream = audio.open(rate=RATE, channels=CHANNELS, format=pyaudio.paInt16, input=True, frames_per_buffer=FRAMES)

            # Loop de detecção da Wake Word
            while True:

                array = np.frombuffer(stream.read(FRAMES), dtype=np.int16)
                wake_word = model.predict(array)
                
                if wake_word['Hey_Jarvis'] >= 0.5:
                    print("Bear acordou!")
                    model.reset()
                    stream.stop_stream()
                    stream.close()
                    break # Sai do loop de espera
            
            # Libera o microfone COMPLETAMENTE para o outro processo usar

            # --- Lógica de Comando ---
            gravado = audio_service.gravar_audio()
            
            if gravado:
                texto = audio_service.transcrever(gravado)
                print("--- Transcrito: ---", texto)
                if texto:
                    resposta = llm_service.enviar_pergunta(texto)
                    await audio_service.tocar_audio(resposta)
            
            # O loop reinicia e recria o recorder lá em cima
            
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        audio.terminate()

if __name__ == '__main__':
    llm_service = LLMFactory.get_llm_service(config.LLM_PROVIDER)
    audio_service = AudioService()
    asyncio.run(main(llm_service, audio_service))