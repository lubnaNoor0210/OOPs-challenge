import streamlit as st
import requests
from datetime import datetime
from hijri_convertor import CalendarConverter
from Emotional_quote import QuranQuoteGenerator
from prayer_tracker import PrayerJournal

st.set_page_config(page_title="Quran Guide", layout="wide")
st.markdown(
    """
     <style>
        .stApp{
            background: linear-gradient(to bottom, #F1F1F1, #D97A48); 
            height: 100vh;
            margin: 0;
            padding: 0;}
            .center {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .quote-box {
            background-color: #F1F1F1;  
            border: 6px solid  #D56B6B;
            padding: 15px;
            border-radius: 5px;
            color: #000000;
            font-size: 22px; 
        }
        .prayer-box {
            background-color: #F1F1F1;
            border: 6px solid #D56B6B;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            font-size: 18px;
        }
         .convertor-box {
            background-color: #F1F1F1;  
            border: 6px solid  #D56B6B;
            padding: 15px;
            border-radius: 5px;
            color: #000000;
            font-size: 22px; 
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Q uran verse
@st.cache_data
def fetch_surah_list():
    response = requests.get("https://api.alquran.cloud/v1/surah")
    if response.status_code == 200:
        data = response.json()["data"]
        # Create a dict like: {"Al-Fatiha (1)": 1, "Al-Baqarah (2)": 2, ...}
        return {f"{surah['englishName']} ({surah['number']})": surah["number"] for surah in data}
    else:
        return {}
def fetch_prayer_times(city):
    response = requests.get(f'http://api.aladhan.com/v1/timingsByCity?city={city}&country=&method=1&school=1')
    if response.status_code == 200:
        return response.json()['data']['timings']
    return None
def format_time(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.strftime("%I:%M %p")

#  Streamlit UI 
st.markdown("<div class='center'><h1>🕌 Quran-Guide</h1></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    tabs = st.tabs(["☪️Salah Time🕜","📖 Quote Generator", "📅 Calendar Converter", "📔 Journal", "Asma-Ul-Husna🌟", "Surah Translation"])
# Tab No 1: PRAYER TIME
with tabs[0]:
    st.subheader('Today\'s Prayer Times')
    city = st.text_input('Enter your city:', 'Makkah')

    if st.button('Get Prayer Times'):
        prayer_times = fetch_prayer_times(city)

        if prayer_times:
            for prayer, time in prayer_times.items():
                formatted_time = format_time(time)
                st.markdown(f'<div class="prayer-box">{prayer}: {formatted_time}</div>', unsafe_allow_html=True)
        else:
            st.error('Failed to fetch prayer times. Please try again.')

# Quote Generator
with tabs[1]:
    st.subheader("Find a Quran Quote Based on Your Emotions")
    emotion = st.selectbox("Select your emotion:", ("Sad", "Anxious", "Grateful", "Hopeful", "Fearful", "Angry", "Guilty", "Impatient", "Insecure", "Lazy", "Happy" ))
    if st.button("Get Quote"):
        quote = QuranQuoteGenerator(emotion).fetch_quote()
        if quote:
            st.markdown(f'<div class="quote-box">{quote}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">Sorry, unable to fetch the quote. Please try again.</div>', unsafe_allow_html=True)
        
# Calendar Converter
with tabs[2]:
    st.subheader("Convert Dates Between Gregorian and Hijri")
    date = st.text_input("Enter date (DD-MM-YYYY):")
    direction = st.radio("Convert to:", ("Hijri", "Gregorian"))
    if st.button("Convert Date"):
        to_hijri = True if direction == "Hijri" else False
        converted = CalendarConverter(date, to_hijri).convert()
        st.markdown(f'<div class= "convertor-box">{converted}</div>', unsafe_allow_html=True)

#Journal
with tabs[3]:
    st.subheader("Track Your Prayers and Dhikr")
    journal = PrayerJournal()
    today = datetime.now().strftime("%Y-%m-%d")
    day_name = datetime.now().strftime("%A")
    st.write(f"📅 Today's Date: {today} ({day_name})")

    entry = journal.get_entry(today)
    prev_prayers = entry.get("prayers", {})
    prev_dhikr = entry.get("dhikr", "")

    st.markdown("### 🙏 Prayers")
    prayers = {
        "Tahajjud": st.checkbox("Tahajjud", value=prev_prayers.get("Tahajjud", False)),
        "Fajr": st.checkbox("Fajr", value=prev_prayers.get("Fajr", False)),
        "Dhuhr": st.checkbox("Dhuhr", value=prev_prayers.get("Dhuhr", False)),
        "Asr": st.checkbox("Asr", value=prev_prayers.get("Asr", False)),
        "Maghrib": st.checkbox("Maghrib", value=prev_prayers.get("Maghrib", False)),
        "Isha": st.checkbox("Isha", value=prev_prayers.get("Isha", False)),
    }

    st.markdown("### 🧘‍♂️ Dhikr / Reflections")
    dhikr = st.text_area("Write here:", value=prev_dhikr)

    if st.button("💾 Save Today’s Journal"):
        journal.save_entry(today, prayers, dhikr)
        st.success("✅ Journal entry saved successfully!")

    st.markdown("---")
    st.markdown(f"### 📖 Journal Summary for {today} ({entry.get('day', day_name)})")
    prayed = [prayer for prayer, done in prayers.items() if done]
    if prayed:
        st.markdown("**🕌 Prayers offered today:**")
        for p in prayed:
            st.markdown(f"- {p}")
    else:
        st.markdown("*No prayers marked yet today.*")

    st.markdown("**🧎 Dhikr/Reflection:**")
    st.markdown(f"> {dhikr}" if dhikr else "*No dhikr written yet today.*")
# 99 names
with tabs[4]:
    st.subheader("🕋 99 Names of Allah (Asma ul Husna)")
    response = requests.get("https://api.aladhan.com/v1/asmaAlHusna")
    
    if response.status_code == 200:
        names = response.json()["data"]
        for i in range(0, len(names), 3):
            row = st.columns(3)[::-1]
            for j in range(3):
                if i + j < len(names):
                    name = names[i + j]
                    with row[j]:
                        st.markdown(f"### {name['name']}")
                        st.markdown(f"*{name['en']['meaning']}*")
                        st.markdown("---")
                    
    else:
        st.error("Failed to fetch 99 Names of Allah. Please check the API.")


#  Quran Verse 
with tabs[5]:
    st.subheader("🔍 View a Quran Verse")

    surah_dict = fetch_surah_list()
    surah_name = st.selectbox("Select Surah:", list(surah_dict.keys()))
    surah_number = surah_dict[surah_name]

    verse_number = st.number_input("Enter Verse number:", min_value=1, step=1)

    if st.button("Get Verse"):
        # Arabic & English using AlQuran Cloud
        arabic_url = f"https://api.alquran.cloud/v1/ayah/{surah_number}:{verse_number}/ar"
        english_url = f"https://api.alquran.cloud/v1/ayah/{surah_number}:{verse_number}/en.asad"

        try:
            arabic_res = requests.get(arabic_url).json()
            english_res = requests.get(english_url).json()

            arabic = arabic_res["data"]["text"]
            english = english_res["data"]["text"]

            st.markdown(f"**🕋 Arabic:** {arabic}")
            st.markdown(f"**🌍 Translation:** {english}")
        except:
            st.error("❌ Invalid Surah or Verse. Please try again.")
