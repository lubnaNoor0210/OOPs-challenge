import streamlit as st
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
            return response.json()["data"]["hijri"]["date"] if self.to_hijri else response.json()["data"]["gregorian"]["date"]
        return "Conversion failed. Check the date format."
    
