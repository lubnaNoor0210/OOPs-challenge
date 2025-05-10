import requests
class AllahNames:
    def __init__(self):
        self.api_url = "https://api.aladhan.com/v1/asmaAlHusna"
    def fetch_names(self):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                return response.json()["data"]
            else:
                return []
        except:
            return []