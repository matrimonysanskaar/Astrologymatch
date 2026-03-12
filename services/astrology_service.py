from typing import Dict, Tuple
from utils.zodiac import get_zodiac_sign_from_date, calculate_zodiac_compatibility
from services.numerology_service import (
    calculate_life_path,
    calculate_destiny_number,
    calculate_name_number,
    calculate_match_compatibility_details,
    convert_date_format
)


def calculate_match_compatibility(male_data: Dict, female_data: Dict) -> Dict:
    """
    Calculate match compatibility between two people using ACTUAL numerology.
    
    Weighted scoring based on numerological principles:
    - Zodiac Compatibility: 30% (astro)
    - Life Path Match: 35% (most important in numerology)
    - Destiny Number: 20%
    - Name Compatibility: 15%
    """
    
    # Extract and convert dates
    male_birth_date = convert_date_format(male_data["birth_date"])
    female_birth_date = convert_date_format(female_data["birth_date"])
    
    male_name = male_data["name"]
    female_name = female_data["name"]
    
    # 1. Zodiac Compatibility (30%)
    male_zodiac = get_zodiac_sign_from_date(male_birth_date)
    female_zodiac = get_zodiac_sign_from_date(female_birth_date)
    zodiac_score = calculate_zodiac_compatibility(male_zodiac, female_zodiac)
    
    # 2. Numerology Compatibility using actual calculations (70%)
    numerology_details = calculate_match_compatibility_details(
        male_name, male_birth_date,
        female_name, female_birth_date
    )
    
    # Get individual scores
    life_path_score = numerology_details["life_path"]["score"]
    destiny_score = numerology_details["destiny"]["score"]
    name_score = numerology_details["name"]["score"]
    
    # Calculate weighted final score
    # Zodiac: 30%, Life Path: 35%, Destiny: 20%, Name: 15%
    final_score = int(
        (zodiac_score * 0.30) + 
        (numerology_details["overall_score"] * 0.70)
    )
    
    # Determine category
    category, summary = get_category_and_summary(final_score)
    
    # Create couple name
    couple_name = f"{male_name} ❤️ {female_name}"
    
    # Prepare detailed results
    details = {
        "zodiac_match": zodiac_score,
        "life_path_match": life_path_score,
        "destiny_match": destiny_score,
        "name_compatibility": name_score,
        "male_zodiac": male_zodiac,
        "female_zodiac": female_zodiac,
        "male_life_path": numerology_details["life_path"]["person1"],
        "female_life_path": numerology_details["life_path"]["person2"],
        "male_destiny": numerology_details["destiny"]["person1"],
        "female_destiny": numerology_details["destiny"]["person2"],
        "male_soul_urge": numerology_details["soul_urge"]["person1"],
        "female_soul_urge": numerology_details["soul_urge"]["person2"]
    }
    
    return {
        "couple": couple_name,
        "score": final_score,
        "category": category,
        "summary": summary,
        "details": details
    }


def get_category_and_summary(score: int) -> Tuple[str, str]:
    """Determine category and summary based on score"""
    if score >= 85:
        return "Excellent Match", "You have excellent compatibility! A wonderful cosmic connection that transcends ordinary relationships."
    elif score >= 70:
        return "Very Good Match", "You have strong compatibility with great potential for a lasting partnership."
    elif score >= 55:
        return "Good Match", "You have good compatibility. With understanding and effort, this relationship can flourish beautifully."
    elif score >= 40:
        return "Average Match", "Better than most but requires work. Communication and patience are key to success."
    elif score >= 25:
        return "Challenging Match", "There are significant differences to overcome. Both partners need to be patient and understanding."
    else:
        return "Difficult Match", "This relationship faces many challenges. Extra effort and compromise will be required."

