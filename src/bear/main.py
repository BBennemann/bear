from bear.infrastructure.llm import LLMFactory
import asyncio
from bear.config import config

from bear.infrastructure.audio.recorder import SpeechRecognitionRecorder
from bear.infrastructure.audio.wake_word import OpenWakeWordDetector
from bear.infrastructure.stt.groq_whisper import GroqWhisperSTT
from bear.infrastructure.tts.edge_tts_service import EdgeMpvTTS

from bear.application.assistant import BearOrchestrator

def run() -> None:

    llm_service = LLMFactory.get_llm_service(config.LLM_PROVIDER)
    wake_word_detector = OpenWakeWordDetector(config.MODEL_PATH)
    recorder = SpeechRecognitionRecorder()
    stt = GroqWhisperSTT(api_key=config.GROQ_API_KEY, language=config.LANGUAGE, prompt=config.profile.stt_prompt)
    tts = EdgeMpvTTS(voice=config.profile.tts_voice)

    orchestrator = BearOrchestrator(llm_service=llm_service, wake_word_detector=wake_word_detector, recorder=recorder, stt=stt, tts=tts)
    asyncio.run(orchestrator.start())
    

if __name__ == '__main__':
    run()