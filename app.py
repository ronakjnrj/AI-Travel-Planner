import streamlit as st
from utils import generate_itinerary

st.set_page_config(page_title="AI Travel Planner")
st.title("AI Travel Itinerary Planner")

with st.form("travel_form"):
    destination = st.text_input("Destination", placeholder="Tokyo, Japan")
    num_days = st.slider("Number of Days", 1, 14, 5)
    travel_style = st.selectbox("Travel Style",["Relaxed", "Adventure", "Cultural", "Foodie", "Budget Backpacker"])
    budget = st.selectbox("Budget", ["Budget", "Mid-Range", "Luxury"])
    interests = st.text_input("Interests",placeholder="street food, temples, nature, nightlife")
    special_requirements = st.text_area("Special Requirements",placeholder="Vegetarian meals, wheelchair accessible, traveling with kids...")
    submitted = st.form_submit_button("Generate Itinerary 🗺️")

if submitted and destination:
    with st.spinner("Researching and planning your trip..."):
        user_input = {
            "destination": destination,
            "num_days": str(num_days),
            "travel_style": travel_style,
            "budget": budget,
            "interests": interests,
            "special_requirements": special_requirements or "None"
        }
        result = generate_itinerary(user_input)
    st.markdown("---")
    st.markdown(result)