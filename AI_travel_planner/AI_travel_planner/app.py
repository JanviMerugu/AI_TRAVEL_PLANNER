import streamlit as st
from datetime import date, timedelta
from dotenv import load_dotenv
import os
import re
from integrations.google_genai_integration import fetch_travel_recommendations
from utils.images_helper import fetch_destination_images

# Load environment variables
load_dotenv()

# Load API keys from .env
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")

# Currency Exchange Rate (Static - can be fetched via API if needed)
USD_TO_INR = 83  # 1 USD = 83 INR (update this if needed)


def convert_prices_to_inr(recommendations):
    """Convert prices in USD ($120) to INR (₹9960) in the AI recommendations text."""
    def convert_price(match):
        usd_price = float(match.group(1))
        inr_price = usd_price * USD_TO_INR
        return f"₹{inr_price:.0f} (USD ${usd_price})"

    return re.sub(r"\$(\d+(\.\d+)?)", convert_price, recommendations)


def main():
    # App Title with Globe Emoji 🌍
    st.title("🌍 AI Travel Planner")

    # Inputs with Emojis and Unique Keys
    source = st.text_input("📍 Enter Source Location", key="source_location")
    destination = st.text_input("📍 Enter Destination Location", key="destination_location")

    # Date Range Picker with Calendar Emoji 📅
    start_date = st.date_input("📅 Start Date", date.today(), key="start_date")
    end_date = st.date_input("📅 End Date", date.today() + timedelta(days=5), key="end_date")
    date_range = f"{start_date} to {end_date}"

    # Transport, Budget, Time, Travelers with Related Emojis
    mode = st.selectbox("✈️🚂🚌🚖 Preferred Mode of Transport", ["Flight", "Train", "Bus", "Cab", "Any"], key="mode")
    budget = st.selectbox("💰 Budget Range", ["Budget", "Standard", "Luxury"], key="budget")
    time = st.selectbox("⏰ Preferred Time to Travel", ["Morning", "Afternoon", "Evening", "Night"], key="time")
    travelers = st.number_input("👥 Number of Travelers", min_value=1, step=1, key="travelers")

    # Currency Choice 💱
    currency = st.selectbox("💱 Preferred Currency", ["USD ($)", "INR (₹)"], key="currency")

    # Plan Button with Luggage Emoji 🎒
    if st.button("🎒 Plan My Trip", key="plan_trip"):
        if not all([source, destination, GENAI_API_KEY, UNSPLASH_API_KEY]):
            st.error("⚠️ Please fill all fields and set API keys in your .env file.")
        else:
            # Fetch destination images
            st.subheader(f"📸 Beautiful Views of {destination}")
            images = fetch_destination_images(destination, UNSPLASH_API_KEY)

            cols = st.columns(3)
            for i, img_url in enumerate(images[:3]):
                with cols[i]:
                    st.image(img_url, caption=f"View {i+1}", use_container_width=True)

            # Fetch AI Recommendations
            recommendations = fetch_travel_recommendations(
                source, destination, mode, budget, time, travelers, date_range, GENAI_API_KEY
            )

            # Convert prices if INR selected
            if currency == "INR (₹)":
                recommendations = recommendations.replace("$", "USD $")  # To make sure user knows original price
                recommendations = convert_prices_to_inr(recommendations)

            # Display Recommendations (from Gemini AI)
            st.subheader("✨ Travel Recommendations")
            st.markdown(recommendations)


if __name__ == "__main__":
    main()
