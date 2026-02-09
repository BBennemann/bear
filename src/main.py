from services.audio import AudioService
from services.gemini import enviar_pergunta
import asyncio
from pvrecorder import PvRecorder
import pvporcupine
from config.config import config
from pathlib import Path

async def main():
    current_dir = Path(__file__).parent # Pega o caminho do arquivo atual
    model_path = current_dir / 'models' / 'bear_porcupine.ppn' # Constrói o caminho absoluto

    audio_service = AudioService()

    porcupine = pvporcupine.create(
        access_key=config.PICOVOICE_API_KEY,
        keyword_paths=[model_path]
    )

    print("Bear está ouvindo...")

    try:
        while True:
            # Cria o gravador apenas para esse ciclo de "espera"
            recorder = PvRecorder(frame_length=porcupine.frame_length)
            recorder.start()
            
            # Loop de detecção da Wake Word
            while True:
                pcm = recorder.read()
                keyword_index = porcupine.process(pcm)
                
                if keyword_index >= 0:
                    print("Bear acordou!")
                    break # Sai do loop de espera
            
            # Libera o microfone COMPLETAMENTE para o outro processo usar
            recorder.stop()
            recorder.delete()

            # --- Lógica de Comando ---
            audio = audio_service.gravar_audio()
            
            if audio:
                texto = audio_service.transcrever(audio)
                print("--- Transcrito: ---", texto)
                if texto:
                    resposta = enviar_pergunta(texto)
                    asyncio.run(audio_service.tocar_audio(resposta))
            
            # O loop reinicia e recria o recorder lá em cima
            
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if 'porcupine' in locals():
            porcupine.delete()

if __name__ == '__main__':
    main()