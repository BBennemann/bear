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

        self.voice = 'pt-BR-AntonioNeural'

        self._verificar_dependencias()


    def _verificar_dependencias(self):
        self.mpv_path = shutil.which("mpv")
        if not self.mpv_path:
            raise RuntimeError("MPV player não encontrado. Instale com 'sudo apt install mpv'")


    def _config_recognizer(self):
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.6
        self.recognizer.dynamic_energy_threshold = True

    def gravar_audio(self):
        with sr.Microphone() as source:
            print("\n--- A escutar... (Fala agora) ---")
            
            # Ajusta o ruído de fundo (apenas 0.2s para ser rápido)
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            
            try:
                # 1. Captura o áudio (com limite de tempo para não travar)
                # timeout=5: Espera até 5s para você começar a falar
                # phrase_time_limit=10: Corta se você falar por mais de 10s
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=30)
                audio_data = audio.get_wav_data()
                arquivo_memoria = ("audio.wav", audio_data)

                return arquivo_memoria

            except sr.WaitTimeoutError:
                print("Não detetei fala (tempo esgotado).")
            except sr.UnknownValueError:
                print("Não foi possível entender o áudio.")
            except Exception as e:
                print(f"Erro: {e}")

    def transcrever(self, arquivo: tuple[str, Any]):
        return self.client.audio.transcriptions.create(
                    file=arquivo,
                    model="whisper-large-v3", # O modelo mais preciso
                    prompt="O áudio é em português.", # Contexto opcional ajuda na precisão
                    response_format="text",
                    language="pt" # Força o português
                )

    async def tocar_audio(self, texto: str):
        
        tts = et.Communicate(texto, self.voice)
        
        # Inicia o mpv esperando dados pelo stdin
        cmd = [self.mpv_path, "--no-cache", "--no-terminal", "--", "-"]
        
        try:
            processo = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            async for chunk in tts.stream():
                if chunk["type"] == "audio":
                    processo.stdin.write(chunk["data"])
                    processo.stdin.flush()
            
            if processo.stdin:
                processo.stdin.close()
            processo.wait()
                
        except Exception as e:
            print(f"Erro no stream de áudio: {e}")
