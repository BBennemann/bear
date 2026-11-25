import asyncio

from bear.domain.exceptions import BearError

from bear.domain.interfaces.audio_recorder import IAudioRecorder
from bear.domain.interfaces.llm_service import ILLMService
from bear.domain.interfaces.stt_service import ISTTService
from bear.domain.interfaces.tts_service import ITTSService
from bear.domain.interfaces.wake_word import IWakeWord


class BearOrchestrator():

    def __init__(self, llm_service: ILLMService, wake_word_detector: IWakeWord, recorder: IAudioRecorder, stt: ISTTService, tts: ITTSService):
        
        self.llm_service = llm_service
        self.wake_word_detector = wake_word_detector
        self.recorder = recorder
        self.stt = stt
        self.tts = tts

    async def start(self) -> None:
        print("Bear is listening...")
        
        try:
            already_awake = False
            while True:

                try:
                    if not already_awake:
                        self.wake_word_detector.listen_wake_word()
                    already_awake = False
                    # --- Command Logic ---
                    recorded_audio = self.recorder.record_audio()
                    
                    if recorded_audio:
                        transcribed_text = self.stt.transcribe(recorded_audio)
                        print("--- Transcribed: ---", transcribed_text)
                        if transcribed_text:
                            response = self.llm_service.send_query(transcribed_text)
                            speak_task = asyncio.create_task(self.tts.speak(response))
                            wake_task = asyncio.create_task(asyncio.to_thread(self.wake_word_detector.listen_wake_word))
                            done, pending = await asyncio.wait([speak_task, wake_task], return_when=asyncio.FIRST_COMPLETED)

                            if wake_task in done:
                                self.tts.stop()
                                speak_task.cancel()
                            elif speak_task in done:
                                await wake_task
                            already_awake = True
                except BearError as e:
                    print(f"Interaction error: {e}")
                # The loop restarts and recreates the stream above
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.wake_word_detector.terminate()
