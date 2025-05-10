import requests

class CalendarConverter:
    def __init__(self, date, to_hijri=True):
        self.date = date
        self.to_hijri = to_hijri

    def convert(self):
        base_url = "https://api.aladhan.com/v1/"
        endpoint = "gToH" if self.to_hijri else "hToG"
        params = {"date": self.date}
        response = requests.get(base_url + endpoint, params=params)

        if response.status_code == 200:
            data = response.json()["data"]

            if self.to_hijri:
                hijri = data["hijri"]
                day = hijri["day"]
                month = hijri["month"]["en"]
                year = hijri["year"]

                # Ensure weekday is in English; fallback to parsing if necessary
                weekday = hijri.get("weekday", {}).get("en")
                if not weekday or not weekday.isalpha():
                    weekday = self.get_english_weekday(data["gregorian"]["date"])  # fallback
                
                return f"{day} {month} {year} ({weekday})"

            else:
                gregorian = data["gregorian"]
                day = gregorian["day"]
                month = gregorian["month"]["en"]
                year = gregorian["year"]
                weekday = gregorian.get("weekday", {}).get("en", "")
                return f"{day} {month} {year} ({weekday})"

        return "Conversion failed. Check the date format."

    def get_english_weekday(self, greg_date):
        """
        Fallback method: convert a date string like '12-04-2025' to English weekday.
        """
        from datetime import datetime
        try:
            dt = datetime.strptime(greg_date, "%d-%m-%Y")
        except:
            try:
                dt = datetime.strptime(greg_date, "%Y-%m-%d")
            except:
                return ""
        return dt.strftime("%A")
