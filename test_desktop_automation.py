import unittest
import pyautogui
import time
from PyQt5.QtWidgets import QApplication
import sys

class TestDesktopAutomation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Fare hareketleri için güvenli mod
        pyautogui.FAILSAFE = True
        # Hareketler arası bekleme süresi
        pyautogui.PAUSE = 1.0
        
        # Uygulama penceresini bul
        print("Lütfen uygulama penceresini açın...")
        time.sleep(2)
        
        # Buton koordinatlarını kaydet
        print("\nButon koordinatlarını kaydetme işlemi başlıyor...")
        cls.button_coords = {}
        
        print("\nLütfen fare ile 'Kayıt Başlat' butonuna gidin (tıklamayın) ve 3 saniye bekleyin...")
        time.sleep(3)
        cls.button_coords['record'] = pyautogui.position()
        
        print("\nLütfen fare ile 'Kayıt Durdur' butonuna gidin (tıklamayın) ve 3 saniye bekleyin...")
        time.sleep(3)
        cls.button_coords['stop'] = pyautogui.position()
        
        print("\nLütfen fare ile 'Kayıt İşle' butonuna gidin (tıklamayın) ve 3 saniye bekleyin...")
        time.sleep(3)
        cls.button_coords['process'] = pyautogui.position()
        
        print("\nLütfen fare ile 'Duygu Analizi' butonuna gidin (tıklamayın) ve 3 saniye bekleyin...")
        time.sleep(3)
        cls.button_coords['emotion'] = pyautogui.position()
        
        print("\nLütfen fare ile 'Konu Analizi' butonuna gidin (tıklamayın) ve 3 saniye bekleyin...")
        time.sleep(3)
        cls.button_coords['topic'] = pyautogui.position()
        
        print("\nKoordinatlar kaydedildi!")
        
    def test_1_record_and_process(self):
        """Test Case 1: Kayıt ve İşleme Testi"""
        print("\nTest Case 1: Kayıt ve İşleme Testi başlıyor...")
        
        try:
            # Kayıt Başlat
            pyautogui.click(self.button_coords['record'])
            print("Kayıt başlatıldı...")
            time.sleep(3)
            
            # Kayıt Durdur
            pyautogui.click(self.button_coords['stop'])
            print("Kayıt durduruldu...")
            time.sleep(1)
            
            # Kayıt İşle
            pyautogui.click(self.button_coords['process'])
            print("Kayıt işleniyor...")
            time.sleep(2)
            
            # Sonuç kontrolü için kullanıcıya sor
            result = input("\nTranscript görüntülendi mi? (e/h): ")
            self.assertEqual(result.lower(), 'e', "Transcript görüntülenemedi!")
            
        except Exception as e:
            self.fail(f"Test başarısız: {str(e)}")
            
    def test_2_emotion_analysis(self):
        """Test Case 2: Duygu Analizi Testi"""
        print("\nTest Case 2: Duygu Analizi Testi başlıyor...")
        
        try:
            # Duygu Analizi butonuna tıkla
            pyautogui.click(self.button_coords['emotion'])
            print("Duygu analizi yapılıyor...")
            time.sleep(2)
            
            # Sonuç kontrolü için kullanıcıya sor
            result = input("\nDuygu analizi sonuçları görüntülendi mi? (e/h): ")
            self.assertEqual(result.lower(), 'e', "Duygu analizi sonuçları görüntülenemedi!")
            
        except Exception as e:
            self.fail(f"Test başarısız: {str(e)}")
            
    def test_3_topic_analysis(self):
        """Test Case 3: Konu Analizi Testi"""
        print("\nTest Case 3: Konu Analizi Testi başlıyor...")
        
        try:
            # Konu Analizi butonuna tıkla
            pyautogui.click(self.button_coords['topic'])
            print("Konu analizi yapılıyor...")
            time.sleep(2)
            
            # Sonuç kontrolü için kullanıcıya sor
            result = input("\nKonu analizi sonuçları görüntülendi mi? (e/h): ")
            self.assertEqual(result.lower(), 'e', "Konu analizi sonuçları görüntülenemedi!")
            
        except Exception as e:
            self.fail(f"Test başarısız: {str(e)}")

if __name__ == "__main__":
    unittest.main() 