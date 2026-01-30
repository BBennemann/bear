from services.audio import gravar_audio, transcrever, tocar_audio
from services.gemini import enviar_pergunta
import asyncio
from pvrecorder import PvRecorder
import pvporcupine
from config.config import config
import os

def main():
    porcupine = pvporcupine.create(
        access_key=config.PICOVOICE_API_KEY,
        keyword_paths=["src/models/bear_porcupine.ppn"]
    )

    recorder = PvRecorder(frame_length=porcupine.frame_length)

    print("Bear está ouvindo...")

    try:
        recorder.start()

        while True:
            pcm = recorder.read()
            
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                print("Bear acordou!")
                
                recorder.stop()

                audio = gravar_audio()
                if audio:

                    texto = transcrever(audio)
                    print("--- Transcrito: ---", texto)
                    if texto:
                        resposta = enviar_pergunta(texto)
                        asyncio.run(tocar_audio(resposta))

                recorder.start()

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        recorder.stop()
        recorder.delete()
        porcupine.delete()

if __name__ == '__main__':
    main()