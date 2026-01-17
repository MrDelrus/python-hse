def compute_target_water_ml(
    weight_kg: float,
    activity_time_m: float,
    temperature: float | None,
) -> float:
    """Estimate daily water intake."""
    result = weight_kg * 30 + 500 * (activity_time_m // 30)
    if temperature and temperature > 25:
        result += 750

    return result
 

def compute_target_calorie(
    weight_kg: float,
    height_cm: float,
    age: float,
    activity_time_m: float
) -> float:
    """Estimate daily calorie intake."""
    result = 10 * weight_kg + 6.25 * height_cm - 5 * age
    if activity_time_m > 30:
        result += 200
    
    return result
