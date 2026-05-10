import streamlit as st
from planner import generate_travel_plan

st.set_page_config(page_title="AI Weekend Tour Planner", page_icon="🌍", layout="wide")

st.title("🌍 AI Weekend Tour Planner")
st.markdown("Plan your perfect family weekend getaway powered by AI and real-world data!")

with st.sidebar:
    st.header("Travel Preferences")
    source_location = st.text_input("Source Location", value="Pune")
    num_days = st.number_input("Number of Days", min_value=1, max_value=7, value=2)
    family_size = st.number_input("Family Size", min_value=1, max_value=15, value=4)
    budget = st.number_input("Budget (₹)", min_value=1000, max_value=500000, value=15000)
    interests = st.text_input("Interests/Preferences", value="Nature, Kids Friendly")
    travel_mode = st.selectbox("Travel Mode", ["Car", "Bus", "Train"])
    
    plan_button = st.button("Generate Travel Plan 🚀", type="primary")

if plan_button:
    with st.spinner("Analyzing destinations, checking weather, and creating your perfect itinerary..."):
        try:
            itinerary = generate_travel_plan(
                source_location=source_location,
                num_days=num_days,
                family_size=family_size,
                budget=budget,
                interests=interests,
                travel_mode=travel_mode
            )
            
            st.success("Your Travel Plan is Ready!")
            st.markdown(itinerary)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown("### Transparent Sources")
st.markdown("""
- **Places & Attractions**: Google Places API (Mocked in MVP)
- **Distance & Route**: Google Distance Matrix API (Mocked in MVP)
- **Weather**: OpenWeatherMap API
- **AI Agent**: Groq (Llama 3.3)
""")
