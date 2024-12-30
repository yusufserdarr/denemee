from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pyaudio
import wave
import numpy as np
import speech_recognition as sr
from your_main_file import EmotionAnalyzer
from topic_analyzer import TopicAnalyzer

class UiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speaker Recognition")
        
        # Ses kayıt parametreleri
        self.CHUNK = 4096
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.recognizer = sr.Recognizer()
        self.emotion_analyzer = EmotionAnalyzer()
        self.topic_analyzer = TopicAnalyzer()
        
        # Konuşmacı verileri
        self.speakers_data = {
            "Efe": 0,
            "Yusuf": 0,
            "Kaan": 0,
            "Diğer": 0
        }
        self.total_speaking_time = 0
        
        # UI kurulumu
        self.setup_ui()
        
    def setup_ui(self):
        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Info layout (konuşmacı, transcript ve kelime sayısı için)
        self.info_layout = QVBoxLayout()
        self.speaker_label = QLabel("Konuşmacı: --")
        self.transcript_label = QLabel("Transcript: --")
        self.word_count_label = QLabel("Kelime Sayısı: 0")
        
        self.info_layout.addWidget(self.speaker_label)
        self.info_layout.addWidget(self.transcript_label)
        self.info_layout.addWidget(self.word_count_label)
        self.main_layout.addLayout(self.info_layout)
        
        # Grafik alanları
        self.setup_plots()
        self.setup_speaker_plot()
        
        # Buton layout'u
        self.button_layout = QHBoxLayout()
        
        # Butonları oluştur
        self.kayit_baslat = QPushButton("⏺")  # Başlangıçta kayıt ikonu
        self.kayit_durdur = QPushButton("⏹")
        self.kayit_isle = QPushButton("⚙️")
        self.duygu_analiz = QPushButton("💭")
        self.konu_analiz = QPushButton("📊")
        
        # Temel buton stili
        base_style = """
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #d0d0d0;
            }
        """
        
        # Kayıt butonu için özel başlangıç stili (yeşilimsi)
        record_button_initial = """
            QPushButton {
                background-color: #ffffff;
                color: #28a745;
                border: 2px solid #28a745;
                border-radius: 25px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #28a745;
                color: white;
            }
        """
        
        # Kayıt butonu için kayıt durumu stili (kırmızı)
        self.record_button_recording = """
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: 2px solid #dc3545;
                border-radius: 25px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
                border-color: #bd2130;
            }
        """
        
        # Başlangıç stillerini uygula
        self.kayit_baslat.setStyleSheet(record_button_initial)
        self.kayit_durdur.setStyleSheet(base_style)
        self.kayit_isle.setStyleSheet(base_style)
        self.duygu_analiz.setStyleSheet(base_style)
        self.konu_analiz.setStyleSheet(base_style)
        
        # Tooltip'leri ekle
        self.kayit_baslat.setToolTip("Kayıt Başlat")
        self.kayit_durdur.setToolTip("Kayıt Durdur")
        self.kayit_isle.setToolTip("Kayıt İşle")
        self.duygu_analiz.setToolTip("Duygu Analizi")
        self.konu_analiz.setToolTip("Konu Analizi")
        
        # Butonları layout'a ekle
        self.button_layout.addWidget(self.kayit_baslat)
        self.button_layout.addWidget(self.kayit_durdur)
        self.button_layout.addWidget(self.kayit_isle)
        self.button_layout.addWidget(self.duygu_analiz)
        self.button_layout.addWidget(self.konu_analiz)
        
        # Buton layout'u ana layout'a ekle
        self.main_layout.addLayout(self.button_layout)
        
        # Buton bağlantıları
        self.kayit_baslat.clicked.connect(self.start_recording)
        self.kayit_durdur.clicked.connect(self.stop_recording)
        self.kayit_isle.clicked.connect(self.process_audio)
        self.duygu_analiz.clicked.connect(self.show_emotion_analysis)
        self.konu_analiz.clicked.connect(self.show_topic_analysis)
        
        # Başlangıç durumu
        self.kayit_durdur.setEnabled(False)
        self.kayit_isle.setEnabled(False)
        self.duygu_analiz.setEnabled(False)
        self.konu_analiz.setEnabled(False)
        
    def setup_speaker_plot(self):
        """Konuşmacı pasta grafiği için setup"""
        # Grafik için frame
        self.speaker_frame = QFrame()
        self.speaker_frame.setFrameStyle(QFrame.StyledPanel)
        self.speaker_layout = QVBoxLayout(self.speaker_frame)
        
        # Başlık etiketi
        self.speaker_title = QLabel("Konuşmacı Dağılımı")
        self.speaker_title.setAlignment(Qt.AlignCenter)
        self.speaker_layout.addWidget(self.speaker_title)
        
        # Pasta grafik için figure
        self.speaker_figure = Figure(figsize=(6, 4))
        self.speaker_canvas = FigureCanvas(self.speaker_figure)
        self.speaker_ax = self.speaker_figure.add_subplot(111)
        
        # Grafiği layout'a ekle
        self.speaker_layout.addWidget(self.speaker_canvas)
        
        # Ana layout'a ekle
        self.main_layout.addWidget(self.speaker_frame)
        
        # İlk pasta grafiği çiz
        self.update_speaker_plot()
        
    def update_speaker_plot(self):
        """Pasta grafiğini güncelle"""
        self.speaker_ax.clear()
        
        # Sıfır olmayan değerleri filtrele
        non_zero_speakers = {k: v for k, v in self.speakers_data.items() if v > 0}
        
        if sum(non_zero_speakers.values()) > 0:
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
            wedges, texts, autotexts = self.speaker_ax.pie(
                non_zero_speakers.values(),
                labels=non_zero_speakers.keys(),
                colors=colors,
                autopct='%1.1f%%',
                startangle=90
            )
            plt.setp(autotexts, size=8, weight="bold")
            plt.setp(texts, size=8)
        else:
            self.speaker_ax.text(
                0.5, 0.5,
                'Henüz konuşma verisi yok',
                horizontalalignment='center',
                verticalalignment='center'
            )
        
        self.speaker_canvas.draw()
        
    def identify_speaker(self, audio_data):
        """Konuşmacı tanıma fonksiyonu"""
        try:
            # Simüle edilmiş konuşmacı tanıma
            import random
            confidence = random.random()
            
            if confidence > 0.7:
                speaker = "Efe"
            elif confidence > 0.4:
                speaker = "Yusuf"
            elif confidence > 0.2:
                speaker = "Kaan"
            else:
                speaker = "Diğer"
            
            # Konuşma süresini hesapla
            speaking_time = len(audio_data) / self.RATE
            
            # Konuşmacı verilerini güncelle
            self.speakers_data[speaker] += speaking_time
            self.total_speaking_time += speaking_time
            
            # Yüzdeleri güncelle
            if self.total_speaking_time > 0:
                for spk in self.speakers_data:
                    self.speakers_data[spk] = (self.speakers_data[spk] / self.total_speaking_time) * 100
            
            # Grafiği güncelle
            self.update_speaker_plot()
            
            # Konuşmacı etiketini güncelle
            self.speaker_label.setText(f"Konuşmacı: {speaker}")
            print(f"Konuşmacı tespit edildi: {speaker}")
            
        except Exception as e:
            print(f"Konuşmacı tanıma hatası: {str(e)}")
            self.speaker_label.setText("Konuşmacı: Bilinmiyor")

    def setup_plots(self):
        """Ses sinyali ve dağılım grafikleri için setup"""
        # Figure oluştur
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        
        # İki subplot oluştur
        self.ax1 = self.figure.add_subplot(211)  # Ses sinyali için
        self.ax2 = self.figure.add_subplot(212)  # Dağılım için
        
        # Grafik başlıkları
        self.ax1.set_title("Ses Sinyali")
        self.ax2.set_title("Ses Verisi Dağılımı")
        
        # Boş grafikleri çiz
        self.line1, = self.ax1.plot([], [])
        self.line2, = self.ax2.plot([], [])
        
        # Grafikleri sıkıştır
        self.figure.tight_layout()
        
        # Canvas'ı layout'a ekle
        self.main_layout.addWidget(self.canvas)
        
        # İlk çizimi yap
        self.canvas.draw() 

    def start_recording(self):
        """Ses kaydını başlat"""
        self.frames = []
        self.is_recording = True
        
        # Stream'i başlat
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.audio_callback
        )
        
        # Buton durumlarını güncelle
        self.kayit_baslat.setEnabled(False)
        self.kayit_durdur.setEnabled(True)
        self.kayit_isle.setEnabled(False)
        
        # Kayıt butonunun stilini değiştir (kırmızı)
        self.kayit_baslat.setStyleSheet(self.record_button_recording)
        print("Kayıt başladı...")

    def stop_recording(self):
        """Ses kaydını durdur"""
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        # Buton durumlarını güncelle
        self.kayit_baslat.setEnabled(True)
        self.kayit_durdur.setEnabled(False)
        self.kayit_isle.setEnabled(True)
        
        # Kayıt butonunu başlangıç stiline döndür (yeşil)
        self.kayit_baslat.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #28a745;
                border: 2px solid #28a745;
                border-radius: 25px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #28a745;
                color: white;
            }
        """)
        
        # Ses verisini kaydet
        self.save_audio()

    def audio_callback(self, in_data, frame_count, time_info, status):
        """Ses verisi geldiğinde çağrılır"""
        if self.is_recording:
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            self.frames.append(audio_data)
            # Grafik güncelleme
            self.update_plots(np.concatenate(self.frames), np.histogram(audio_data, bins=50)[0])
        return (in_data, pyaudio.paContinue)

    def update_plots(self, signal_data, distribution_data):
        """Grafikleri güncelle"""
        # Ses sinyali grafiği
        self.ax1.clear()
        self.ax1.plot(signal_data)
        self.ax1.set_title("Ses Sinyali")
        
        # Dağılım grafiği
        self.ax2.clear()
        self.ax2.plot(distribution_data)
        self.ax2.set_title("Ses Verisi Dağılımı")
        
        # Grafikleri yenile
        self.figure.tight_layout()
        self.canvas.draw()

    def save_audio(self):
        """Ses verisini WAV formatında kaydet"""
        if self.frames:
            try:
                wf = wave.open('recorded_audio.wav', 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(np.concatenate(self.frames).tobytes())
                wf.close()
                print("Ses dosyası kaydedildi")
            except Exception as e:
                print(f"Ses kaydetme hatası: {str(e)}")

    def process_audio(self):
        """Ses kaydını işle ve metne çevir"""
        try:
            print("Ses işleme başlıyor...")
            
            with sr.AudioFile('recorded_audio.wav') as source:
                print("Gürültü ayarlaması yapılıyor...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                print("Ses dosyası okunuyor...")
                audio = self.recognizer.record(source)
                
                print("Google Speech Recognition ile çevriliyor...")
                try:
                    text = self.recognizer.recognize_google(
                        audio,
                        language='tr-TR',
                        show_all=False
                    )
                    print(f"Algılanan metin: {text}")
                    
                    # Metin ve kelime sayısını güncelle
                    self.transcript_label.setText(f"Transcript: {text}")
                    self.word_count_label.setText(f"Kelime Sayısı: {len(text.split())}")
                    
                    # Konuşmacı tanıma
                    if self.frames:
                        audio_data = np.concatenate(self.frames)
                        self.identify_speaker(audio_data)
                    
                    # Analiz butonlarını aktif et
                    self.duygu_analiz.setEnabled(True)
                    self.konu_analiz.setEnabled(True)
                    
                except sr.UnknownValueError:
                    print("Google Speech Recognition metni anlayamadı")
                    self.transcript_label.setText("Transcript: Ses anlaşılamadı")
                    self.word_count_label.setText("Kelime Sayısı: 0")
                    self.speaker_label.setText("Konuşmacı: --")
                    
        except Exception as e:
            print(f"Genel hata: {str(e)}")
            self.transcript_label.setText("Transcript: Bir hata oluştu")
            self.word_count_label.setText("Kelime Sayısı: 0")
            self.speaker_label.setText("Konuşmacı: --")

    def show_emotion_analysis(self):
        """Duygu analizi sonuçlarını göster"""
        try:
            text = self.transcript_label.text().replace("Transcript: ", "")
            if text and text != "Ses anlaşılamadı":
                results = self.emotion_analyzer.analyze_emotion(text)
                
                # Sonuç metni oluştur
                result_text = f"Baskın Duygu: {results['baskın_duygu']}\n"
                result_text += f"Güven Skoru: {results['güven_skoru']:.2f}\n\n"
                result_text += "Duygu Dağılımı:\n"
                
                for emotion, percentage in results['duygular'].items():
                    result_text += f"{emotion}: %{percentage:.1f}\n"
                
                # MessageBox yerine label'a yazdır
                if not hasattr(self, 'emotion_result_label'):
                    self.emotion_result_label = QLabel()
                    self.main_layout.addWidget(self.emotion_result_label)
                
                self.emotion_result_label.setText(result_text)
                self.emotion_result_label.show()
                
        except Exception as e:
            print(f"Duygu analizi hatası: {str(e)}")

    def show_topic_analysis(self):
        """Konu analizi sonuçlarını göster"""
        try:
            text = self.transcript_label.text().replace("Transcript: ", "")
            if text and text != "Ses anlaşılamadı":
                # Genişletilmiş konu anahtar kelimeleri
                topics = {
                    'spor': ['futbol', 'basketbol', 'voleybol', 'maç', 'oyun', 'antrenman', 'koşu', 
                            'takım', 'spor', 'fitness', 'yüzme', 'tenis', 'gol'],
                    
                    'eğitim': ['okul', 'ders', 'ödev', 'sınav', 'öğretmen', 'öğrenci', 'kitap', 
                              'eğitim', 'öğrenmek', 'çalışmak', 'not', 'başarı', 'sınıf'],
                    
                    'teknoloji': ['bilgisayar', 'telefon', 'internet', 'uygulama', 'program', 'yazılım',
                                 'teknoloji', 'tablet', 'oyun', 'web', 'site', 'sosyal medya'],
                    
                    'bilim': ['fizik', 'kimya', 'biyoloji', 'matematik', 'deney', 'formül', 'bilim',
                             'araştırma', 'laboratuvar', 'teori', 'element', 'atom', 'hücre', 'uzay'],
                    
                    'sanat': ['müzik', 'resim', 'dans', 'şarkı', 'film', 'tiyatro', 'konser', 'sanat',
                             'sergi', 'çizim', 'fotoğraf', 'sinema', 'sahne', 'roman'],
                    
                    'aile': ['anne', 'baba', 'kardeş', 'aile', 'ev', 'dede', 'nine', 'akraba', 
                            'kuzen', 'teyze', 'dayı', 'amca', 'çocuk'],
                    
                    'günlük yaşam': ['yemek', 'uyku', 'kahvaltı', 'alışveriş', 'market', 'ev', 'iş',
                                    'arkadaş', 'sohbet', 'gezi', 'tatil', 'park', 'cafe', 'restoran'],
                    
                    'sağlık': ['hastane', 'doktor', 'ilaç', 'sağlık', 'hastalık', 'tedavi', 'spor',
                              'beslenme', 'diyet', 'vitamin', 'ağrı', 'kontrol', 'muayene'],
                    
                    
                }
                
                words = text.lower().split()
                topic_scores = {topic: 0 for topic in topics}
                matched_words = set()  # Eşleşen kelimeleri takip et
                
                # Her kelime için sadece bir konuya puan ver
                for word in words:
                    for topic, keywords in topics.items():
                        if word in keywords and word not in matched_words:
                            topic_scores[topic] += 1
                            matched_words.add(word)
                            break
                
                total_score = sum(topic_scores.values())
                
                # Sonuç metni oluştur
                result_text = "Konu Analizi:\n\n"
                
                if total_score > 0:
                    # Yüzdeleri hesapla ve sadece 0'dan büyük olanları göster
                    topic_percentages = {
                        topic: round((score / total_score) * 100, 1)
                        for topic, score in topic_scores.items()
                    }
                    
                    # Yüzdeleri büyükten küçüğe sırala
                    sorted_topics = sorted(
                        topic_percentages.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )
                    
                    # Sadece 0'dan büyük yüzdeleri göster
                    for topic, percentage in sorted_topics:
                        if percentage > 0:
                            result_text += f"{topic}: %{percentage}\n"
                else:
                    result_text += "Belirli bir konu tespit edilemedi."
                
                # Sonuçları göster
                if not hasattr(self, 'topic_result_label'):
                    self.topic_result_label = QLabel()
                    self.main_layout.addWidget(self.topic_result_label)
                
                self.topic_result_label.setText(result_text)
                self.topic_result_label.show()
                
        except Exception as e:
            print(f"Konu analizi hatası: {str(e)}")

    def update_speaker_label(self):
        """Konuşmacı etiketini güncelle"""
        if hasattr(self, 'speaker_label'):
            self.speaker_label.setText(f"Konuşmacı: {self.current_speaker}") 