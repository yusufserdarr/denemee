from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class TestSpeakerRecognitionWeb(unittest.TestCase):
    def setUp(self):
        # Chrome WebDriver'ı başlat
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")  # Web uygulamasının adresi
        self.wait = WebDriverWait(self.driver, 10)
        
    def tearDown(self):
        # Browser'ı kapat
        self.driver.quit()
        
    def test_1_record_and_process(self):
        """Test Case 1: Kayıt ve İşleme Testi"""
        print("\nTest Case 1: Kayıt ve İşleme Testi başlıyor...")
        
        try:
            # Kayıt başlat butonunu bul ve tıkla
            record_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "recordButton"))
            )
            record_button.click()
            
            # 3 saniye bekle
            time.sleep(3)
            
            # Kaydı durdur
            stop_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "stopButton"))
            )
            stop_button.click()
            
            # Kayıt işle butonuna tıkla
            process_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "processButton"))
            )
            process_button.click()
            
            # Sonuçları kontrol et
            transcript = self.wait.until(
                EC.presence_of_element_located((By.ID, "transcriptLabel"))
            )
            speaker = self.wait.until(
                EC.presence_of_element_located((By.ID, "speakerLabel"))
            )
            
            # Assertions
            self.assertIsNotNone(transcript.text)
            self.assertIsNotNone(speaker.text)
            self.assertNotEqual(transcript.text, "")
            self.assertNotEqual(speaker.text, "")
            
        except Exception as e:
            self.fail(f"Test başarısız: {str(e)}")
            
    def test_2_emotion_analysis(self):
        """Test Case 2: Duygu Analizi Testi"""
        print("\nTest Case 2: Duygu Analizi Testi başlıyor...")
        
        try:
            # Önce ses kaydı yap
            record_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "recordButton"))
            )
            record_button.click()
            time.sleep(3)
            
            stop_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "stopButton"))
            )
            stop_button.click()
            
            # Kayıt işle
            process_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "processButton"))
            )
            process_button.click()
            
            # Duygu analizi butonuna tıkla
            emotion_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "emotionButton"))
            )
            emotion_button.click()
            
            # Duygu analizi sonuçlarını kontrol et
            emotion_results = self.wait.until(
                EC.presence_of_element_located((By.ID, "emotionResults"))
            )
            
            # Assertions
            self.assertIsNotNone(emotion_results.text)
            self.assertIn("Duygu Dağılımı:", emotion_results.text)
            
            # Yüzdelerin toplamını kontrol et
            percentages = [float(x.strip('%')) for x in 
                         emotion_results.text.split('\n') if '%' in x]
            total = sum(percentages)
            self.assertAlmostEqual(total, 100, delta=1)
            
        except Exception as e:
            self.fail(f"Test başarısız: {str(e)}")
            
    def test_3_topic_analysis(self):
        """Test Case 3: Konu Analizi Testi"""
        print("\nTest Case 3: Konu Analizi Testi başlıyor...")
        
        try:
            # Önce ses kaydı yap
            record_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "recordButton"))
            )
            record_button.click()
            time.sleep(3)
            
            stop_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "stopButton"))
            )
            stop_button.click()
            
            # Kayıt işle
            process_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "processButton"))
            )
            process_button.click()
            
            # Konu analizi butonuna tıkla
            topic_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "topicButton"))
            )
            topic_button.click()
            
            # Konu analizi sonuçlarını kontrol et
            topic_results = self.wait.until(
                EC.presence_of_element_located((By.ID, "topicResults"))
            )
            
            # Assertions
            self.assertIsNotNone(topic_results.text)
            self.assertIn("Konu Analizi:", topic_results.text)
            
            # En az bir konu tespit edilmiş olmalı
            topics = [x for x in topic_results.text.split('\n') 
                     if ':' in x and '%' in x]
            self.assertTrue(len(topics) > 0)
            
        except Exception as e:
            self.fail(f"Test başarısız: {str(e)}")

if __name__ == "__main__":
    unittest.main() 