import google.generativeai as genai

def fetch_travel_recommendations(source, destination, mode, budget, time, travelers, date_range, genai_api_key):
    genai.configure(api_key=genai_api_key)

    prompt = f"""
Act as a smart travel assistant. Plan a trip from {source} to {destination}.
- Preferred Mode of Travel: {mode}
- Budget: {budget}
- Preferred Time: {time}
- Number of Travelers: {travelers}
- Date Range: {date_range}

1. Create a table comparing travel options (Flight, Train, Bus, Cab) with:
    - Cost per person
    - Total cost (for {travelers} people)
    - Duration
    - Booking link (real Google search link like: "flights from {source} to {destination}").

2. Create a table of Top 3 Nearby Hotels with:
    - Name
    - Type (Luxury, Budget, Resort, etc.)
    - Price per night
    - Rating


3. Create a table of Top 3 Restaurants/Cafes with:
    - Name
    - Type (Cafe, Seafood, Fine Dining, etc.)
    - Specialty Dish

4. End with a simple 1-line Weather Forecast for {destination}.

Format everything neatly in Markdown tables.
"""

    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text