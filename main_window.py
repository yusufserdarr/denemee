from PyQt5.QtWidgets import QMainWindow
from your_main_file import EmotionAnalyzer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Duygu analizi sınıfını başlat
        self.emotion_analyzer = EmotionAnalyzer(self)
        
        # Etiketleri layout'a ekle
        self.layout.addWidget(self.emotion_analyzer.emotion_label)
        self.layout.addWidget(self.emotion_analyzer.confidence_label)
        self.layout.addWidget(self.emotion_analyzer.emotions_detail_label) 

    def update_transcript(self, text):
        """Yeni transcript geldiğinde çağrılacak fonksiyon"""
        self.transcript_text = text 