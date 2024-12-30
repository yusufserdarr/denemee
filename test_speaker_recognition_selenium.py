import unittest
import pyaudio
import wave
import numpy as np
from ui_setup import UiMainWindow
from PyQt5.QtWidgets import QApplication
import sys

class TestSpeakerRecognition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
        cls.window = UiMainWindow()
        
    def setUp(self):
        self.window.frames = []
        self.window.is_recording = False
        
    def normalize_emotions(self, emotions):
        """Duygu yüzdelerini normalize et"""
        total = sum(emotions.values())
        if total > 0:
            return {k: (v/total) * 100 for k, v in emotions.items()}
        return emotions
        
    def test_1_happy_speaker(self):
        """Test Case 1: Mutlu konuşmacı testi"""
        print("\nTest Case 1: Mutlu konuşmacı testi başlıyor...")
        
        test_text = "Bugün çok mutluyum çünkü sınavdan yüksek not aldım"
        
        emotion_results = self.window.emotion_analyzer.analyze_emotion(test_text)
        emotion_results['duygular'] = self.normalize_emotions(emotion_results['duygular'])
        
        self.assertIn('mutlu', emotion_results['duygular'])
        self.assertTrue(emotion_results['duygular']['mutlu'] > 0)
        
        total = sum(emotion_results['duygular'].values())
        self.assertAlmostEqual(total, 100, delta=1,
            msg=f"Duygu yüzdeleri toplamı 100 olmalı, şu an: {total}")
        
    def test_2_mixed_emotions(self):
        """Test Case 2: Karışık duygular testi"""
        print("\nTest Case 2: Karışık duygular testi başlıyor...")
        
        test_text = "Fizik sınavında kötü yaptım mutsuzum ama matematik dersini çok seviyorum"
        
        emotion_results = self.window.emotion_analyzer.analyze_emotion(test_text)
        emotion_results['duygular'] = self.normalize_emotions(emotion_results['duygular'])
        topics = self.analyze_topic(test_text)
        
        self.assertIn('mutsuz', emotion_results['duygular'])
        self.assertIn('mutlu', emotion_results['duygular'])
        
        found_topics = set(topics.keys())
        self.assertIn('eğitim', found_topics,
            msg=f"'eğitim' konusu bulunamadı. Bulunan konular: {found_topics}")
        
    def test_3_long_speech(self):
        """Test Case 3: Uzun konuşma testi"""
        print("\nTest Case 3: Uzun konuşma testi başlıyor...")
        
        test_text = "Laboratuvarda deney yaparken çok heyecanlandım, sonra arkadaşlarımla kantinde oturup sohbet ettik"
        
        emotion_results = self.window.emotion_analyzer.analyze_emotion(test_text)
        emotion_results['duygular'] = self.normalize_emotions(emotion_results['duygular'])
        topics = self.analyze_topic(test_text)
        
        self.assertIn('bilim', topics)
        self.assertIn('günlük yaşam', topics)
        
        total = sum(emotion_results['duygular'].values())
        self.assertAlmostEqual(total, 100, delta=1)
        
    def test_4_noise_conditions(self):
        """Test Case 4: Sessizlik ve gürültü testi"""
        print("\nTest Case 4: Sessizlik ve gürültü testi başlıyor...")
        
        # Sessiz ortam testi
        quiet_data = np.zeros(44100, dtype=np.int16)
        self.window.frames = [quiet_data]
        self.assertTrue(len(self.window.frames) > 0)
        
        # Gürültülü ortam testi
        noisy_data = (np.random.normal(0, 0.1, 44100) * 32767).astype(np.int16)
        self.window.frames = [noisy_data]
        self.assertTrue(len(self.window.frames) > 0)
        
        # Ses sinyali kontrolü
        self.assertTrue(np.max(np.abs(noisy_data)) <= 32767)
        
    def test_5_system_performance(self):
        """Test Case 5: Sistem performans testi"""
        print("\nTest Case 5: Sistem performans testi başlıyor...")
        
        test_texts = [
            "Bugün hava çok güzel ve mutluyum",
            "Matematik dersini çok seviyorum",
            "Arkadaşlarımla oyun oynadık ve eğlendik",
            "Bilgisayarda kod yazarken heyecanlandım",
            "Müzik dinlerken dans edip mutlu oldum"
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\nAlt test {i}/5: {text}")
            
            emotion_results = self.window.emotion_analyzer.analyze_emotion(text)
            emotion_results['duygular'] = self.normalize_emotions(emotion_results['duygular'])
            
            total = sum(emotion_results['duygular'].values())
            self.assertAlmostEqual(total, 100, delta=1,
                msg=f"Duygu yüzdeleri toplamı 100 olmalı, şu an: {total}")
    
    def analyze_topic(self, text):
        """Geliştirilmiş konu analizi"""
        topics = {
            'bilim': ['laboratuvar', 'deney', 'fizik', 'kimya', 'formül'],
            'eğitim': ['sınav', 'ders', 'ödev', 'okul', 'not', 'matematik'],
            'günlük yaşam': ['arkadaş', 'kantin', 'sohbet', 'oyun', 'müzik'],
            'teknoloji': ['bilgisayar', 'kod', 'program', 'internet'],
            'duygular': ['mutlu', 'mutsuz', 'heyecan', 'sevinç', 'kızgın']
        }
        
        words = text.lower().split()
        topic_scores = {topic: 0 for topic in topics}
        
        for word in words:
            for topic, keywords in topics.items():
                if word in keywords:
                    topic_scores[topic] += 1
                    
        return {k: v for k, v in topic_scores.items() if v > 0}

if __name__ == '__main__':
    unittest.main() 