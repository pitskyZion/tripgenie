import streamlit as st
import openai
from datetime import datetime, timedelta
import os

# --- Set OpenAI API key safely (free Streamlit accounts use fallback) ---
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-your_actual_key_here")  # replace with your key
if not openai.api_key:
    st.error("❌ OpenAI API key not found. Please set it in environment variables.")
    st.stop()

st.title("🧳 TripGenie AI – Smart Travel Planner from TikTok")

# --- Input section ---
tiktok_url = st.text_input("Paste TikTok travel video URL")
traveler_type = st.selectbox("Who's traveling?", ["Solo", "Couple", "Family with infant", "Traveling with elder"])
arrival_time = st.time_input("Flight arrival time", value=datetime.now().time())
departure_time = st.time_input("Flight departure time", value=(datetime.now() + timedelta(days=7)).time())
days = st.slider("Trip length (days)", 3, 14, 7)

# --- Placeholder function to extract locations from TikTok (mocked) ---
def extract_locations_from_tiktok(url):
    # In real version, you'd parse video or captions
    return ["Tokyo Tower", "Shibuya Crossing", "Asakusa Temple", "TeamLab Planets"]

# --- Build itinerary prompt ---
def generate_itinerary(locations, traveler_type, arrival, departure, days):
    base_prompt = f"""
    You are a smart travel assistant. Given these places: {', '.join(locations)}, create a detailed {days}-day travel itinerary in Tokyo.

    Adjust the plan based on:
    - Arrival time: {arrival}
    - Departure time: {departure}
    - Traveler type: {traveler_type}

    Include suggested time blocks and nearby food spots. Keep travel between places efficient.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": base_prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content

# --- Generate Itinerary ---
if st.button("Generate Itinerary"):
    with st.spinner("Analyzing TikTok and building your itinerary..."):
        locations = extract_locations_from_tiktok(tiktok_url)
        result = generate_itinerary(locations, traveler_type, arrival_time, departure_time, days)

        st.markdown("---")
        st.subheader("📅 Your Smart AI Itinerary")
        st.markdown(result)

        # ✅ Show booking links only after generating itinerary
        st.markdown("---")
        st.markdown("### 🔗 Booking Links (Mock)")
        for place in locations:
            st.markdown(f"- [Search hotels near {place}](https://www.booking.com/searchresults.html?ss={place.replace(' ', '+')})")
            st.markdown(f"- [Find tours for {place}](https://www.getyourguide.com/s/?q={place.replace(' ', '+')})")

    st.caption("This is a demo MVP. In the full version, we’ll auto-parse TikTok videos and add real-time APIs for booking, weather, and maps.")
