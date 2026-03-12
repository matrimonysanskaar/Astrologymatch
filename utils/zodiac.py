from datetime import datetime
from typing import Tuple


# Zodiac signs with their date ranges and elements
ZODIAC_SIGNS = {
    "Aries": {"start": (3, 21), "end": (4, 19), "element": "Fire", "ruling_planet": "Mars"},
    "Taurus": {"start": (4, 20), "end": (5, 20), "element": "Earth", "ruling_planet": "Venus"},
    "Gemini": {"start": (5, 21), "end": (6, 20), "element": "Air", "ruling_planet": "Mercury"},
    "Cancer": {"start": (6, 21), "end": (7, 22), "element": "Water", "ruling_planet": "Moon"},
    "Leo": {"start": (7, 23), "end": (8, 22), "element": "Fire", "ruling_planet": "Sun"},
    "Virgo": {"start": (8, 23), "end": (9, 22), "element": "Earth", "ruling_planet": "Mercury"},
    "Libra": {"start": (9, 23), "end": (10, 22), "element": "Air", "ruling_planet": "Venus"},
    "Scorpio": {"start": (10, 23), "end": (11, 21), "element": "Water", "ruling_planet": "Pluto"},
    "Sagittarius": {"start": (11, 22), "end": (12, 21), "element": "Fire", "ruling_planet": "Jupiter"},
    "Capricorn": {"start": (12, 22), "end": (1, 19), "element": "Earth", "ruling_planet": "Saturn"},
    "Aquarius": {"start": (1, 20), "end": (2, 18), "element": "Air", "ruling_planet": "Uranus"},
    "Pisces": {"start": (2, 19), "end": (3, 20), "element": "Water", "ruling_planet": "Neptune"},
}

# Element compatibility scores
ELEMENT_COMPATIBILITY = {
    "Fire": {"Fire": 80, "Earth": 40, "Air": 90, "Water": 30},
    "Earth": {"Fire": 40, "Earth": 80, "Air": 50, "Water": 90},
    "Air": {"Fire": 90, "Earth": 50, "Air": 80, "Water": 40},
    "Water": {"Fire": 30, "Earth": 90, "Air": 40, "Water": 80},
}


def get_zodiac_sign(month: int, day: int) -> str:
    """Get zodiac sign based on month and day"""
    for sign, info in ZODIAC_SIGNS.items():
        start_month, start_day = info["start"]
        end_month, end_day = info["end"]
        
        if sign == "Capricorn":
            # Capricorn spans across year boundary
            if (month == 12 and day >= start_day) or (month == 1 and day <= end_day):
                return sign
        else:
            if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
                return sign
    return "Capricorn"  # Default fallback


def get_zodiac_element(sign: str) -> str:
    """Get the element of a zodiac sign"""
    return ZODIAC_SIGNS.get(sign, {}).get("element", "Unknown")


def calculate_zodiac_compatibility(sign1: str, sign2: str) -> int:
    """Calculate zodiac compatibility score (0-100)"""
    element1 = get_zodiac_element(sign1)
    element2 = get_zodiac_element(sign2)
    
    # Get base compatibility from elements
    base_score = ELEMENT_COMPATIBILITY.get(element1, {}).get(element2, 50)
    
    # Sign-specific adjustments
    sign_adjustments = {
        ("Aries", "Leo"): 20,
        ("Leo", "Aries"): 20,
        ("Taurus", "Virgo"): 15,
        ("Virgo", "Taurus"): 15,
        ("Cancer", "Scorpio"): 20,
        ("Scorpio", "Cancer"): 20,
        ("Libra", "Aquarius"): 15,
        ("Aquarius", "Libra"): 15,
        ("Pisces", "Scorpio"): 15,
        ("Scorpio", "Pisces"): 15,
    }
    
    adjustment = sign_adjustments.get((sign1, sign2), 0)
    final_score = min(100, base_score + adjustment)
    
    return final_score


def parse_date(date_str: str) -> Tuple[int, int, int]:
    """Parse date string in YYYY-MM-DD or DD-MM-YYYY format"""
    try:
        # Try YYYY-MM-DD format first
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.year, date_obj.month, date_obj.day
    except ValueError:
        try:
            # Try DD-MM-YYYY format
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            return date_obj.year, date_obj.month, date_obj.day
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD or DD-MM-YYYY")


def parse_time(time_str: str) -> Tuple[int, int]:
    """Parse time string in HH:MM AM/PM format"""
    try:
        time_obj = datetime.strptime(time_str.strip(), "%I:%M %p")
        return time_obj.hour, time_obj.minute
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}. Use HH:MM AM/PM")


def get_zodiac_sign_from_date(birth_date: str) -> str:
    """Get zodiac sign from birth date string"""
    year, month, day = parse_date(birth_date)
    return get_zodiac_sign(month, day)

