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
    </style>
    """,
    unsafe_allow_html=True
)
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
    tabs = st.tabs(["☪️Salah Time🕜","📖 Quote Generator", "📅 Calendar Converter", "📔 Journal", "Asma-Ul-Husna🌟"])
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

# Tab 1: Quote Generator
with tabs[1]:
    st.subheader("Find a Quran Quote Based on Your Emotions")
    emotion = st.selectbox("Select your emotion:", ("Sad", "Anxious", "Grateful", "Hopeful", "Fearful", "Angry", "Guilty", "Impatient", "Insecure", "Lazy", "Happy" ))
    if st.button("Get Quote"):
        quote = QuranQuoteGenerator(emotion).fetch_quote()
        if quote:
            st.markdown(f'<div class="quote-box">{quote}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">Sorry, unable to fetch the quote. Please try again.</div>', unsafe_allow_html=True)
        
# Tab 2: Calendar Converter
with tabs[2]:
    st.subheader("Convert Dates Between Gregorian and Hijri")
    date = st.text_input("Enter date (DD-MM-YYYY):")
    direction = st.radio("Convert to:", ("Hijri", "Gregorian"))
    if st.button("Convert Date"):
        to_hijri = True if direction == "Hijri" else False
        converted = CalendarConverter(date, to_hijri).convert()
        st.info(f"Converted Date: {converted}")

# Tab 3: Journal
with tabs[3]:
    st.subheader("Track Your Prayers and Dhikr")
    journal = PrayerJournal()
    today = datetime.now().strftime("%Y-%m-%d")
    st.write(f"📅 Today's Date: {today}")
    
    prayers = {
        "Tahajjud": st.checkbox("Thajjud"),
        "Fajr": st.checkbox("Fajr"),
        "Dhuhr": st.checkbox("Dhuhr"),
        "Asr": st.checkbox("Asr"),
        "Maghrib": st.checkbox("Maghrib"),
        "Isha": st.checkbox("Isha")
    }
    
    dhikr = st.text_area("🧘‍♂️ Dhikr / Reflections:")
    if st.button("Save Journal"):
        journal.save_entry(today, prayers, dhikr)
        st.success("✅ Journal entry saved!")
    if st.button("View Today’s Entry"):
        entry = journal.get_entry(today)
        st.write("### 📝 Your Prayer & Dhikr Journal Entry:")
        prayed = [prayer for prayer, done in entry["prayers"].items() if done]
        if prayed:
            st.markdown("**🕌 Prayers you offered today:**")
            for p in prayed:
                st.markdown(f"- {p}")
        else:
            st.markdown("*No prayers were marked today.*")
        st.markdown("**🧎 Your Dhikr/Reflection:**")
        st.markdown(f"> {entry['dhikr']}" if entry["dhikr"] else "*No dhikr or reflections written.*")

# Tab 4: 99 Names of Allah
with tabs[4]:
    st.subheader("🕋 99 Names of Allah (Asma ul Husna)")
    response = requests.get("https://api.aladhan.com/v1/asmaAlHusna")
    if response.status_code == 200:
        names = response.json()["data"]
        columns = st.columns(4) 
        for i, name in enumerate(names):
            col = columns[(i + 3) % 4] 
            with col:
                st.markdown(f"### {name['name']}")
                st.markdown(f"*{name['en']['meaning']}*")
                st.markdown("---")
    else:
        st.error("Failed to fetch 99 Names of Allah. Please check the API.")

