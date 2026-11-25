import edge_tts as et
import subprocess
import asyncio
import shutil

from bear.domain.interfaces.tts_service import ITTSService
from bear.domain.exceptions import SpeechSynthesisError

class EdgeMpvTTS(ITTSService):

    def __init__(self, voice: str):
        # Changed to English voice
        self.voice = voice

        self._check_dependencies()
        self._process: asyncio.subprocess.Process | None = None

    def _check_dependencies(self):
        self.mpv_path = shutil.which("mpv")
        if not self.mpv_path:
            raise SpeechSynthesisError("MPV player not found. Install it with 'sudo apt install mpv'")

    async def speak(self, text: str) -> None:
        
        tts = et.Communicate(text, self.voice)
        
        # Starts mpv expecting data via stdin
        cmd = [self.mpv_path, "--no-cache", "--no-terminal", "--", "-"]
        
        try:
            self._process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            async for chunk in tts.stream():
                if chunk["type"] == "audio":
                    self._process.stdin.write(chunk["data"])
                    await self._process.stdin.drain()
            
            if self._process.stdin:
                self._process.stdin.close()
            await self._process.wait()
                
        except Exception as e:
            raise SpeechSynthesisError(f"Error in audio stream: {e}")

    def stop(self) -> None:
        if self._process and self._process.returncode is None:
            self._process.terminate()