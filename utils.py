def calculate_trip_cost(distance_km: float, num_days: int, family_size: int, travel_mode: str) -> dict:
    """
    Estimates the trip cost based on basic heuristics.
    """
    # Heuristics for cost estimation
    fuel_cost_per_km = 8 if travel_mode.lower() == 'car' else 3
    hotel_cost_per_night_per_room = 2500
    food_cost_per_person_per_day = 800
    misc_tickets_per_person = 500

    rooms_needed = (family_size + 1) // 2 # 2 persons per room
    
    fuel_total = distance_km * 2 * fuel_cost_per_km # round trip
    hotel_total = hotel_cost_per_night_per_room * rooms_needed * (num_days - 1)
    food_total = food_cost_per_person_per_day * family_size * num_days
    tickets_total = misc_tickets_per_person * family_size

    total_cost = fuel_total + hotel_total + food_total + tickets_total

    return {
        "fuel": fuel_total,
        "hotel": hotel_total,
        "food": food_total,
        "tickets": tickets_total,
        "total": total_cost
    }

def format_distance(distance_meters: int) -> float:
    """Convert meters to kilometers"""
    return round(distance_meters / 1000, 2)
