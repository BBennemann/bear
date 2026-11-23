
class BearError(Exception):
    pass

class AudioCaptureError(BearError):
    pass

class TranscriptionError(BearError):
    pass

class SpeechSynthesisError(BearError):
    pass

class WakeWordError(BearError):
    pass
class LLMProviderError(BearError):
    pass


