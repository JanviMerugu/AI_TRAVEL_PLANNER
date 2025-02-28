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
USD_TO_INR = 83  # 1 USD = 83 INR (update if needed)


def convert_prices_to_inr(recommendations):
    """Convert prices in USD to INR."""
    def convert_price(match):
        usd_price = float(match.group(1))
        inr_price = usd_price * USD_TO_INR
        return f"₹{inr_price:.0f} (USD ${usd_price})"

    return re.sub(r"\$(\d+(\.\d+)?)", convert_price, recommendations)


def get_google_search_link(mode, source, destination):
    """Generate Google search link for travel mode."""
    query = f"{mode} from {source} to {destination}".replace(" ", "+")
    return f"[Search {mode}s](https://www.google.com/search?q={query})"


def display_travel_options_table(source, destination):
    """Display single clean travel options table with booking links."""
    travel_options = [
        {"Mode of Transport": "Flight", "Estimated Cost": "Varies", "Estimated Duration": "Varies", "Booking": get_google_search_link("flight", source, destination)},
        {"Mode of Transport": "Train", "Estimated Cost": "Varies", "Estimated Duration": "Varies", "Booking": get_google_search_link("train", source, destination)},
        {"Mode of Transport": "Bus", "Estimated Cost": "Varies", "Estimated Duration": "Varies", "Booking": get_google_search_link("bus", source, destination)},
        {"Mode of Transport": "Cab", "Estimated Cost": "Varies", "Estimated Duration": "Varies", "Booking": get_google_search_link("cab", source, destination)},
    ]

    st.table(travel_options)


def display_hotels_table():
    """Display single clean hotels table (no booking link)."""
    hotels = [
        {"Name": "Hotel Rambagh Palace", "Type": "Luxury", "Price per Night": "₹20,000+", "Rating": "4.8"},
        {"Name": "Zostel Jaipur", "Type": "Budget", "Price per Night": "₹1,000 - ₹3,000", "Rating": "4.2"},
        {"Name": "Shahpura House", "Type": "Heritage", "Price per Night": "₹5,000 - ₹10,000", "Rating": "4.5"},
    ]

    st.table(hotels)


def main():
    st.title("🌍 AI Travel Planner")

    source = st.text_input("📍 Enter Source Location", key="source_location")
    destination = st.text_input("📍 Enter Destination Location", key="destination_location")

    start_date = st.date_input("📅 Start Date", date.today(), key="start_date")
    end_date = st.date_input("📅 End Date", date.today() + timedelta(days=5), key="end_date")

    mode = st.selectbox("✈️🚂🚌🚖 Preferred Transport Mode", ["Flight", "Train", "Bus", "Cab", "Any"], key="mode")
    budget = st.selectbox("💰 Budget Range", ["Budget", "Standard", "Luxury"], key="budget")
    time = st.selectbox("⏰ Preferred Time to Travel", ["Morning", "Afternoon", "Evening", "Night"], key="time")
    travelers = st.number_input("👥 Number of Travelers", min_value=1, key="travelers")

    currency = st.selectbox("💱 Preferred Currency", ["USD ($)", "INR (₹)"], key="currency")

    if st.button("🎒 Plan My Trip"):
        if not all([source, destination, GENAI_API_KEY, UNSPLASH_API_KEY]):
            st.error("⚠️ Please fill all fields and set your API keys in `.env` file.")
            return

        st.subheader(f"📸 Stunning Views of {destination}")
        images = fetch_destination_images(destination, UNSPLASH_API_KEY)
        cols = st.columns(3)
        for i, img_url in enumerate(images[:3]):
            with cols[i]:
                st.image(img_url, caption=f"View {i+1}", use_container_width=True)

        date_range = f"{start_date} to {end_date}"

        recommendations = fetch_travel_recommendations(
            source, destination, mode, budget, time, travelers, date_range, GENAI_API_KEY
        )

        if currency == "INR (₹)":
            recommendations = recommendations.replace("$", "USD $")
            recommendations = convert_prices_to_inr(recommendations)

        st.subheader("✨ Travel Recommendations")
        st.markdown(recommendations)

        

        


if __name__ == "__main__":
    main()
