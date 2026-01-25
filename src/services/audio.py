import speech_recognition as sr
from groq import Groq
from typing import Any
import edge_tts as et
import pygame
import time
from pygame import mixer
from config.config import config

# Inicializa o cliente Groq
client = Groq(api_key=config.GROQ_API_KEY)

def gravar_audio():
    # Inicializa o reconhecedor de microfone
    recognizer = sr.Recognizer()

    # Ajustes para detetar quando paras de falar mais rápido
    recognizer.energy_threshold = 300  # Sensibilidade
    recognizer.pause_threshold = 1.5   # Segundos de silêncio para considerar fim da frase
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("\n--- A escutar... (Fala agora) ---")
        
        # Ajusta o ruído de fundo (apenas 0.5s para ser rápido)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            # 1. Captura o áudio (com limite de tempo para não travar)
            audio = recognizer.listen(source)
            audio_data = audio.get_wav_data()
            arquivo_memoria = ("audio.wav", audio_data)

            return arquivo_memoria

        except sr.WaitTimeoutError:
            print("Não detetei fala (tempo esgotado).")
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio.")
        except Exception as e:
            print(f"Erro: {e}")

def transcrever(arquivo: tuple[str, Any]):
    return client.audio.transcriptions.create(
                file=arquivo,
                model="whisper-large-v3", # O modelo mais preciso
                prompt="O áudio é em português.", # Contexto opcional ajuda na precisão
                response_format="text",
                language="pt" # Força o português
            )

async def tocar_audio(texto: str):
    voz = 'pt-BR-AntonioNeural'
    tts = et.Communicate(texto, voz)
    await tts.save('audio.mp3')
    pygame.init()
    mixer.music.load('audio.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)
    pygame.quit()
