class EmotionAnalyzer:
    def __init__(self):
        self.emotion_keywords = {
            'mutlu': ['mutlu', 'sevinç', 'güzel', 'harika', 'süper', 'seviyorum', 'aşk'],
            'üzgün': ['üzgün', 'kötü', 'mutsuz', 'ağla', 'kırık', 'acı'],
            'kızgın': ['kızgın', 'öfke', 'sinir', 'nefret', 'bıktım'],
            'nötr': ['normal', 'idare', 'fena değil', 'şöyle böyle'],
            'şaşkın': ['şaşkın', 'inanamıyorum', 'vay', 'oha']
        }

    def analyze_emotion(self, text):
        text = text.lower()
        words = text.split()
        
        # Duygu skorlarını hesapla
        emotion_scores = {emotion: 0 for emotion in self.emotion_keywords}
        
        # Her kelime için sadece en iyi eşleşmeyi al
        for word in words:
            best_emotion = None
            for emotion, keywords in self.emotion_keywords.items():
                if word in keywords:
                    best_emotion = emotion
                    break
            if best_emotion:
                emotion_scores[best_emotion] += 1
        
        # Toplam skoru hesapla
        total_score = sum(emotion_scores.values())
        
        # Sonuçları hazırla
        results = {
            'baskın_duygu': 'belirsiz',
            'güven_skoru': 0,
            'duygular': {}
        }
        
        # Duygu yüzdelerini hesapla
        if total_score > 0:
            # En yüksek skora sahip duyguyu bul
            max_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            results['baskın_duygu'] = max_emotion[0]
            results['güven_skoru'] = max_emotion[1] / total_score
            
            # Yüzdeleri hesapla
            for emotion, score in emotion_scores.items():
                results['duygular'][emotion] = round((score / total_score) * 100, 1)
        else:
            # Hiç eşleşme yoksa tüm duygular 0
            for emotion in self.emotion_keywords:
                results['duygular'][emotion] = 0.0
        
        return results 