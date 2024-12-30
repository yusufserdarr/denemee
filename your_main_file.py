from PyQt5.QtWidgets import QLabel
from textblob import TextBlob
from googletrans import Translator
from utils.emotion_dictionary import TR_EMOTION_DICT
import logging

logger = logging.getLogger(__name__)

class EmotionAnalyzer:
    def __init__(self, parent=None):
        self.translator = Translator()
        self.tr_emotion_dict = {
            "mutlu": ["mutlu", "sevinçli", "neşeli", "harika", "güzel", "muhteşem", "süper"],
            "mutsuz": ["üzgün", "kederli", "mutsuz", "kötü", "berbat", "korkunç"],
            "nötr": ["normal", "fena değil", "idare eder", "orta"],
            "kızgın": ["sinirli", "öfkeli", "kızgın", "rahatsız", "bıktım"],
            "şaşkın": ["şaşkın", "şaşırmış", "hayret", "inanamıyorum", "vay"]
        }
        self.last_transcript = ""
        
        # UI bileşenlerini oluştur
        self.emotion_label = QLabel("Baskın Duygu: -", parent)
        self.confidence_label = QLabel("Güven Skoru: -", parent)
        self.emotions_detail_label = QLabel(parent)
        
    def process_transcript(self, transcript):
        """Yeni transcript geldiğinde çağrılacak fonksiyon"""
        self.last_transcript = transcript
        emotion_result = self.analyze_emotion(transcript)
        self.update_emotion_display(emotion_result)  # Duygu sonuçlarını göstermek için
        
    def update_emotion_display(self, emotion_result):
        """Duygu analizi sonuçlarını arayüzde göster"""
        try:
            # Eğer Qt kullanıyorsanız:
            self.emotion_label.setText(f"Baskın Duygu: {emotion_result['baskın_duygu']}")
            self.confidence_label.setText(f"Güven Skoru: {emotion_result['güven_skoru']:.2f}")
            
            # Duygu yüzdelerini göster
            duygular_text = "\n".join([
                f"{duygu}: %{yuzde:.1f}" 
                for duygu, yuzde in emotion_result['duygular'].items()
            ])
            self.emotions_detail_label.setText(duygular_text)
            
        except Exception as e:
            logger.error(f"Duygu gösterimi hatası: {str(e)}") 

    def analyze_emotion(self, text):
        try:
            if not text or text == "Ses anlaşılamadı":
                return {
                    "duygular": {
                        "mutlu": 0.0,
                        "mutsuz": 0.0,
                        "nötr": 0.0,
                        "kızgın": 0.0,
                        "şaşkın": 0.0
                    },
                    "baskın_duygu": "belirsiz",
                    "güven_skoru": 0.0
                }

            text = text.lower()
            words = text.split()
            total_words = len(words)
            
            emotion_counts = {emotion: 0 for emotion in self.tr_emotion_dict.keys()}
            
            for word in words:
                for emotion, word_list in self.tr_emotion_dict.items():
                    if word in word_list:
                        emotion_counts[emotion] += 1

            emotion_percentages = {}
            total_matches = sum(emotion_counts.values())
            
            if total_matches > 0:
                for emotion, count in emotion_counts.items():
                    percentage = (count / total_words) * 100
                    emotion_percentages[emotion] = round(percentage, 1)
            else:
                try:
                    translated = self.translator.translate(text, dest='en')
                    analysis = TextBlob(translated.text)
                    polarity = analysis.sentiment.polarity
                    subjectivity = analysis.sentiment.subjectivity
                    
                    if polarity > 0:
                        emotion_percentages = {
                            "mutlu": round(polarity * 100, 1),
                            "mutsuz": 0.0,
                            "nötr": round((1 - abs(polarity)) * 100, 1),
                            "kızgın": 0.0,
                            "şaşkın": round(subjectivity * 50, 1)
                        }
                    elif polarity < 0:
                        emotion_percentages = {
                            "mutlu": 0.0,
                            "mutsuz": round(abs(polarity) * 50, 1),
                            "nötr": round((1 - abs(polarity)) * 100, 1),
                            "kızgın": round(abs(polarity) * 50, 1),
                            "şaşkın": round(subjectivity * 50, 1)
                        }
                    else:
                        emotion_percentages = {
                            "mutlu": 0.0,
                            "mutsuz": 0.0,
                            "nötr": 100.0,
                            "kızgın": 0.0,
                            "şaşkın": round(subjectivity * 50, 1)
                        }
                except:
                    emotion_percentages = {emotion: 0.0 for emotion in self.tr_emotion_dict.keys()}
                    emotion_percentages["nötr"] = 100.0

            baskın_duygu = max(emotion_percentages.items(), key=lambda x: x[1])
            
            return {
                "duygular": emotion_percentages,
                "baskın_duygu": baskın_duygu[0],
                "güven_skoru": baskın_duygu[1] / 100
            }
                
        except Exception as e:
            logger.error(f"Duygu analizi hatası: {str(e)}")
            return {
                "duygular": {emotion: 0.0 for emotion in self.tr_emotion_dict.keys()},
                "baskın_duygu": "belirsiz",
                "güven_skoru": 0.0
            } 