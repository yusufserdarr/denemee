class TopicAnalyzer:
    def __init__(self):
        # Konu kategorileri ve ilgili kelimeleri tanımla
        self.topic_dict = {
            "spor": ["futbol", "basketbol", "voleybol", "koşu", "maç", "gol", "antrenman", 
                    "takım", "oyun", "sahada", "top", "kaleci", "basket", "file"],
            
            "eğitim": ["okul", "ders", "ödev", "sınav", "matematik", "fizik", "kimya", 
                      "biyoloji", "tarih", "öğretmen", "öğrenci", "kitap", "not", "sınıf"],
            
            "teknoloji": ["bilgisayar", "telefon", "internet", "uygulama", "yazılım", 
                         "donanım", "program", "kod", "site", "oyun", "tablet", "şarj"],
            
            "sanat": ["müzik", "resim", "tiyatro", "sinema", "film", "konser", "sergi", 
                     "şarkı", "dans", "sahne", "aktör", "çizim", "boya", "heykel"],
            
            "sağlık": ["spor", "beslenme", "diyet", "vitamin", "hastane", "doktor", 
                      "ilaç", "tedavi", "sağlıklı", "hastalık", "ağrı", "kontrol"]
        }

    def analyze_topic(self, text):
        """Metindeki konuları analiz et"""
        if not text:
            return {"konular": {}, "baskın_konu": "belirsiz"}

        text = text.lower()
        words = text.split()
        
        # Her konu için eşleşme sayısını tut
        topic_matches = {topic: 0 for topic in self.topic_dict.keys()}
        topic_words = {topic: [] for topic in self.topic_dict.keys()}
        
        # Kelimeleri analiz et
        for word in words:
            for topic, word_list in self.topic_dict.items():
                if word in word_list:
                    topic_matches[topic] += 1
                    topic_words[topic].append(word)
        
        # Konu yüzdelerini hesapla
        total_matches = sum(topic_matches.values())
        topic_percentages = {}
        
        if total_matches > 0:
            for topic, count in topic_matches.items():
                percentage = (count / total_matches) * 100
                topic_percentages[topic] = {
                    'yüzde': round(percentage, 1),
                    'kelimeler': topic_words[topic]
                }
        else:
            return {
                "konular": {topic: {'yüzde': 0.0, 'kelimeler': []} for topic in self.topic_dict.keys()},
                "baskın_konu": "belirsiz"
            }
        
        # En yüksek yüzdeli konuyu bul
        baskın_konu = max(topic_percentages.items(), key=lambda x: x[1]['yüzde'])[0]
        
        return {
            "konular": topic_percentages,
            "baskın_konu": baskın_konu
        } 