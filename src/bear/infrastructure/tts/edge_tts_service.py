import edge_tts as et
import subprocess
import shutil

from bear.domain.interfaces.tts_service import ITTSService
from bear.domain.exceptions import SpeechSynthesisError

class EdgeMpvTTS(ITTSService):

    def __init__(self):
        # Changed to English voice
        self.voice = 'en-US-AriaNeural'

        self._check_dependencies()

    def _check_dependencies(self):
        self.mpv_path = shutil.which("mpv")
        if not self.mpv_path:
            raise SpeechSynthesisError("MPV player not found. Install it with 'sudo apt install mpv'")


    async def speak(self, text: str) -> None:
        
        tts = et.Communicate(text, self.voice)
        
        # Starts mpv expecting data via stdin
        cmd = [self.mpv_path, "--no-cache", "--no-terminal", "--", "-"]
        
        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            async for chunk in tts.stream():
                if chunk["type"] == "audio":
                    process.stdin.write(chunk["data"])
                    process.stdin.flush()
            
            if process.stdin:
                process.stdin.close()
            process.wait()
                
        except Exception as e:
            raise SpeechSynthesisError(f"Error in audio stream: {e}")