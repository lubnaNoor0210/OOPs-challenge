import random
class QuranQuoteGenerator:
    def __init__(self, emotion):
        self.emotion = emotion.lower()
        self.emotion_map = {
            "sad": [
                {"text": "Indeed, with hardship comes ease.", "reference":  "Ash-Sharh, Ayah: (6)" },
                {"text": "So verily, with the hardship, there is relief.", "reference": "Ash-Sharh, Ayah: (5)"}
            ],
            "hopeful": [
                {"text": "And whoever puts their trust in Allah, He will be enough for them.", "reference": "At-Talaq, Ayah: (3)"}
            ],
            "fearful": [
                {"text": "Whoever fears Allah, He will make a way out for them.", "reference": "At-Talaq, Ayah: (2)"}
            ],
            "grateful": [
                {"text": "If you are thankful, I will give you more."," reference": "Ibrahim, Ayah: (7)"}
            ],
            "anxious": [
                {"text": "Truly, in the remembrance of Allah hearts find peace.", "reference": "Ra'ad, Ayah: (28)"}
            ],
            "angry": [
                {"text": "Those who control anger and forgive others—Allah loves those who do good.", "reference": "Aal-E-Imran, Ayah: (134)"}
            ],
            "guilty": [
                {"text": "Say, 'O My servants who have harmed yourselves by your own hands, do not despair of Allah's mercy. Allah forgives all sins. He is truly the Most Forgiving, the Most Merciful", "reference": "Az-zumr, Ayah:(53)"}
            ],
            "impatient": [
                {"text": "TAnd if you are patient and fear Allah, their plot will not harm you at all.", "reference": " Al-Imran, Ayah: (120)"}
            ],
            "insecure": [
                {"text": "Indeed, Allah is with those who fear Him and those who are doers of good.", "reference": "Al-Nahl, Ayah: (28)"}
            ],
            "lazy": [
                {"text": "Do not give up and do not be sad. You will be superior if you are believers.”", "reference": "Al-Imran, Ayah: (139)"}
            ],
            "happy": [
                {"text": "Indeed, the believers are successful. They are those who humble themselves in their prayer.", "reference": "Al-Mu'minun, Ayah: (1-2)"}
            ]
        }

    def fetch_quote(self):
        if self.emotion in self.emotion_map:
            quote = random.choice(self.emotion_map[self.emotion])
            return f"{quote['text']}\n\nReference: Surah {quote['reference']}"
        else:
            return "Sorry, no quote found for this emotion."
