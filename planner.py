import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from api_services import get_nearby_places, get_distance_and_time, get_weather
from utils import calculate_trip_cost
from prompts import TRIP_PLANNER_PROMPT
from dotenv import load_dotenv

load_dotenv()

def generate_travel_plan(source_location: str, num_days: int, family_size: int, budget: float, interests: str, travel_mode: str) -> str:
    # 1. Fetch data from APIs (using mock/real services)
    places = get_nearby_places(source_location, interests)
    
    destinations_data = ""
    if places:
        for p in places[:3]: # Provide up to 3 options
            dest_name = p['name']
            dist_info = get_distance_and_time(source_location, dest_name)
            weather_info = get_weather(dest_name)
            
            destinations_data += f"""
            Candidate Destination: {dest_name}
            Rating: {p.get('rating')}
            Distance: {dist_info['distance_text']} ({dist_info['duration_text']})
            Weather: {weather_info['temp']}°C, {weather_info['description']}
            """
    else:
        destinations_data = f"""
        No live API data available for destinations.
        CRITICAL INSTRUCTION: You MUST use your own deep knowledge of the world to suggest 3 REAL, specific, existing destinations near {source_location} that match the interests: '{interests}'. 
        DO NOT invent fake places or use placeholder names. Give accurate distances, real attractions, and realistic weather/cost estimates.
        """

    # 3. Call AI Model
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0.7
    )
    
    prompt = PromptTemplate(
        input_variables=["source_location", "num_days", "family_size", "budget", "interests", "travel_mode", "destinations_data"],
        template=TRIP_PLANNER_PROMPT
    )
    
    chain = prompt | llm
    
    response = chain.invoke({
        "source_location": source_location,
        "num_days": num_days,
        "family_size": family_size,
        "budget": budget,
        "interests": interests,
        "travel_mode": travel_mode,
        "destinations_data": destinations_data
    })
    
    return response.content
