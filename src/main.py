from services.audio import gravar_audio, transcrever, tocar_audio
from services.gemini import enviar_pergunta
import asyncio

def main():
    audio = gravar_audio()
    texto = transcrever(audio)
    resposta = enviar_pergunta(texto)
    asyncio.run(tocar_audio(resposta))

if __name__ == '__main__':
    main()