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
            ],
            "Jealous": [
                {"text":"Or do they envy people for what Allah has given them of His bounty?", "reference": "Surah An-Nisa 4:54"}
            ],
            "Arrogant": [
                {"text":"Worship Allah and associate nothing with Him, and to parents do good, and to relatives, orphans, the needy, the near neighbor, the neighbor farther away, the companion at your side, the traveler, and those whom your right hands possess. Indeed, Allah does not like those who are self-deluding and boastful.", "reference": "Surah An-Nisa 4:36"}
            ],
            "Restless": [
                {"text":"Those who have believed and whose hearts are assured by the remembrance of Allah. Unquestionably, by the remembrance of Allah hearts are assured.", "reference": "Surah Ar-Ra’d (13:28)"}
            ],
            "Depressed": [
                {"text":"O my sons, go and find out about Joseph and his brother and despair not of relief from Allah. Indeed, no one despairs of relief from Allah except the disbelieving people.", "reference": "Surah Yusuf (12:87)"}
            ]
        }
    def fetch_quote(self):
        if self.emotion in self.emotion_map:
            quote = random.choice(self.emotion_map[self.emotion])
            return f"{quote['text']}\n\nReference: Surah {quote['reference']}"
        else:
            return "Sorry, no quote found for this emotion."
