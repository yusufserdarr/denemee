def on_speech_recognized(self, transcript):
    """Konuşma tanıma sonucu geldiğinde"""
    if transcript and transcript != "Ses anlaşılamadı":
        self.process_transcript(transcript) 