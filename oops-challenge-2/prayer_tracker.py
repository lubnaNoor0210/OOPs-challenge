import json
from datetime import datetime

class PrayerJournal:
    def __init__(self, file_path="journal.json"):
        self.file_path = file_path
        try:
            with open(file_path, "r") as f:
                self.data = json.load(f)
        except:
            self.data = {}

    def save_entry(self, date, prayers, dhikr):
        day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
        self.data[date] = {
            "day": day_name,
            "prayers": prayers,
            "dhikr": dhikr
        }
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def get_entry(self, date):
        return self.data.get(date, {"day": "", "prayers": {}, "dhikr": ""})
