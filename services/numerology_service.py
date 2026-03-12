from datetime import datetime
from typing import Dict, List, Tuple
import random


# ============================================
# REAL NUMEROLOGY MAPPING - Pythagorean System
# ============================================

# Full Pythagorean numerology chart (comprehensive mapping)
NUMEROLOGY_CHART = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
    'i': 9, 'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7,
    'q': 8, 'r': 9, 's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6,
    'y': 7, 'z': 8
}

# Vowels for Soul Urge calculation
VOWELS = set('aeiou')

# Master numbers (not reduced in traditional numerology)
MASTER_NUMBERS = {11, 22, 33}


# ============================================
# DATE FORMAT UTILITY FUNCTIONS
# ============================================

def convert_date_format(date_str: str) -> str:
    """
    Convert date from DD-MM-YYYY to YYYY-MM-DD format
    Handles multiple input formats: DD-MM-YYYY, DD/MM/YYYY, YYYY-MM-DD
    """
    if not date_str:
        return None
    
    # Try different formats
    formats = ['%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%y', '%d/%m/%y']
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    # If already in YYYY-MM-DD format, return as-is
    return date_str


def parse_birth_date(birth_date: str) -> Tuple[int, int, int]:
    """
    Parse birth date and return (year, month, day)
    """
    # Convert to standard format first
    standard_date = convert_date_format(birth_date)
    if not standard_date:
        return (0, 0, 0)
    
    try:
        dt = datetime.strptime(standard_date, '%Y-%m-%d')
        return (dt.year, dt.month, dt.day)
    except ValueError:
        return (0, 0, 0)


# ============================================
# CORE NUMEROLOGY CALCULATION FUNCTIONS
# ============================================

def reduce_to_single_digit(number: int, include_master: bool = True) -> int:
    """
    Reduce a number to a single digit using the Pythagorean method.
    Master numbers (11, 22, 33) are preserved if include_master is True.
    """
    if number <= 0:
        return 0
    
    # If it's a master number and we want to keep it
    if include_master and number in MASTER_NUMBERS:
        return number
    
    while number > 9 and number not in MASTER_NUMBERS:
        number = sum(int(digit) for digit in str(number))
    
    return number


def calculate_name_number(name: str) -> int:
    """
    Calculate the Destiny Number from a name using Pythagorean system.
    """
    if not name:
        return 0
    
    name = name.lower().replace(" ", "").replace("-", "")
    total = 0
    
    for char in name:
        if char in NUMEROLOGY_CHART:
            total += NUMEROLOGY_CHART[char]
    
    return reduce_to_single_digit(total)


def calculate_life_path(birth_date: str) -> int:
    """
    Calculate Life Path Number from birth date using the Pythagorean method.
    This is the most important number in numerology.
    
    Method: Add all digits of birth date (day, month, year), then reduce
    """
    # Convert date format first
    standard_date = convert_date_format(birth_date)
    if not standard_date:
        return 0
    
    # Remove hyphens and sum all digits
    date_digits = standard_date.replace("-", "")
    
    try:
        total = sum(int(digit) for digit in date_digits)
        return reduce_to_single_digit(total)
    except:
        return 0


def calculate_destiny_number(name: str) -> int:
    """
    Calculate Destiny Number (Expression Number) from full name.
    Same as name number - represents talents and abilities.
    """
    return calculate_name_number(name)


def calculate_soul_urge_number(name: str) -> int:
    """
    Calculate Soul Urge Number (Heart's Desire) from vowels in name.
    Represents inner desires and motivations.
    """
    if not name:
        return 0
    
    name = name.lower()
    total = sum(NUMEROLOGY_CHART[char] for char in name 
                if char in VOWELS and char in NUMEROLOGY_CHART)
    
    return reduce_to_single_digit(total)


def calculate_personality_number(name: str) -> int:
    """
    Calculate Personality Number from consonants in name.
    Represents how others perceive you.
    """
    if not name:
        return 0
    
    name = name.lower()
    total = sum(NUMEROLOGY_CHART[char] for char in name 
                if char not in VOWELS and char in NUMEROLOGY_CHART)
    
    return reduce_to_single_digit(total)


def calculate_birth_day_number(birth_date: str) -> int:
    """
    Calculate the Day Number (the day of month you were born).
    Represents natural talents and abilities.
    """
    year, month, day = parse_birth_date(birth_date)
    return reduce_to_single_digit(day)


def calculate_pinnacle_numbers(birth_date: str) -> Dict[int, int]:
    """
    Calculate the 4 Pinnacle numbers in numerology.
    These represent different life cycles.
    """
    year, month, day = parse_birth_date(birth_date)
    
    if year == 0:
        return {1: 0, 2: 0, 3: 0, 4: 0}
    
    # First Pinnacle: Age 0-35 (Month + Day)
    first = reduce_to_single_digit(month + day)
    
    # Second Pinnacle: Age 35-44 (Day + Year sum)
    year_sum = sum(int(d) for d in str(year))
    second = reduce_to_single_digit(day + year_sum)
    
    # Third Pinnacle: Age 45-53 (Month + Year sum)
    third = reduce_to_single_digit(month + year_sum)
    
    # Fourth Pinnacle: Age 54+ (All three combined)
    fourth = reduce_to_single_digit(first + second + third)
    
    return {
        1: first,
        2: second,
        3: third,
        4: fourth
    }


# ============================================
# ACTUAL COMPATIBILITY LOGIC BASED ON NUMEROLOGY
# ============================================

def calculate_life_path_compatibility(lp1: int, lp2: int) -> Tuple[int, str]:
    """
    Calculate Life Path compatibility based on actual numerological rules.
    
    Returns: (score, description)
    """
    # Best matches in numerology (traditional rules)
    life_path_harmony = {
        1: {1: 85, 3: 80, 5: 75, 7: 70, 9: 65, 2: 55, 4: 50, 6: 45, 8: 40},
        2: {2: 90, 4: 85, 8: 80, 6: 75, 1: 55, 3: 50, 5: 45, 7: 40, 9: 35},
        3: {3: 85, 1: 80, 5: 75, 7: 70, 9: 65, 2: 50, 4: 45, 6: 40, 8: 35},
        4: {4: 90, 2: 85, 8: 80, 6: 75, 1: 50, 3: 45, 5: 40, 7: 35, 9: 30},
        5: {5: 85, 1: 75, 3: 70, 7: 65, 9: 60, 2: 55, 4: 50, 6: 45, 8: 40},
        6: {6: 90, 2: 75, 4: 70, 8: 65, 9: 60, 1: 55, 3: 50, 5: 45, 7: 40},
        7: {7: 85, 1: 70, 3: 65, 5: 60, 9: 55, 2: 50, 4: 45, 6: 40, 8: 35},
        8: {8: 90, 4: 80, 6: 75, 2: 70, 1: 65, 3: 50, 5: 45, 7: 40, 9: 35},
        9: {9: 85, 1: 65, 3: 60, 5: 55, 7: 50, 2: 45, 4: 40, 6: 35, 8: 30}
    }
    
    # Add master number harmony
    for master in [11, 22, 33]:
        life_path_harmony[master] = {master: 95, 11: 90, 22: 85, 33: 85, 
                                      1: 70, 2: 70, 3: 70, 4: 70, 5: 70, 
                                      6: 70, 7: 70, 8: 70, 9: 70}
    
    # Handle master number base reduction for lookup
    lp1_base = lp1 if lp1 not in MASTER_NUMBERS else sum(int(d) for d in str(lp1))
    lp2_base = lp2 if lp2 not in MASTER_NUMBERS else sum(int(d) for d in str(lp2))
    
    # Get compatibility (default to 50 if not found)
    score = life_path_harmony.get(lp1_base, {}).get(lp2_base, 50)
    
    # Master number bonus
    if lp1 in MASTER_NUMBERS or lp2 in MASTER_NUMBERS:
        score = min(95, score + 10)
    
    # Get description based on compatibility
    if score >= 80:
        description = "Excellent harmony - You complement each other perfectly"
    elif score >= 65:
        description = "Good compatibility - You share strong potential together"
    elif score >= 50:
        description = "Moderate match - Requires understanding and compromise"
    else:
        description = "Challenging - Different approaches to life may cause friction"
    
    return score, description


def calculate_destiny_compatibility(destiny1: int, destiny2: int) -> Tuple[int, str]:
    """
    Calculate Destiny Number compatibility.
    Determines how well two people complement each other's life purpose.
    """
    # Compatible destiny numbers based on numerological harmony
    destiny_harmony = {
        1: {1: 85, 3: 80, 5: 75, 7: 70, 6: 65, 2: 55, 4: 50, 8: 45, 9: 40},
        2: {2: 90, 4: 85, 8: 80, 6: 75, 1: 55, 3: 50, 5: 45, 7: 40, 9: 35},
        3: {3: 85, 1: 80, 5: 75, 7: 70, 9: 65, 2: 50, 4: 45, 6: 40, 8: 35},
        4: {4: 90, 2: 85, 8: 80, 6: 75, 1: 50, 3: 45, 5: 40, 7: 35, 9: 30},
        5: {5: 85, 1: 75, 3: 70, 7: 65, 9: 60, 2: 55, 4: 50, 6: 45, 8: 40},
        6: {6: 90, 2: 75, 4: 70, 8: 65, 3: 60, 1: 55, 5: 50, 7: 45, 9: 40},
        7: {7: 85, 1: 70, 5: 65, 3: 60, 9: 55, 2: 50, 4: 45, 6: 40, 8: 35},
        8: {8: 90, 4: 80, 6: 75, 2: 70, 1: 65, 3: 50, 5: 45, 7: 40, 9: 35},
        9: {9: 85, 3: 65, 1: 60, 5: 55, 7: 50, 2: 45, 4: 40, 6: 35, 8: 30}
    }
    
    d1_base = destiny1 if destiny1 not in MASTER_NUMBERS else sum(int(d) for d in str(destiny1))
    d2_base = destiny2 if destiny2 not in MASTER_NUMBERS else sum(int(d) for d in str(destiny2))
    
    score = destiny_harmony.get(d1_base, {}).get(d2_base, 50)
    
    # Determine description based on score
    if score >= 80:
        description = "Excellent destiny harmony - Your life purposes align well"
    elif score >= 65:
        description = "Good destiny compatibility - You share similar life goals"
    elif score >= 50:
        description = "Moderate destiny match - Some alignment but differences exist"
    else:
        description = "Challenging destiny compatibility - Different life purposes"
    
    return score, description


def calculate_soul_urge_compatibility(soul1: int, soul2: int) -> Tuple[int, str]:
    """
    Calculate Soul Urge compatibility.
    Measures emotional and inner desire harmony.
    """
    # Soul urge harmony
    soul_harmony = {
        1: {1: 90, 3: 80, 5: 75, 7: 70, 2: 65, 6: 60, 4: 50, 8: 45, 9: 40},
        2: {2: 90, 4: 85, 6: 80, 8: 75, 1: 65, 3: 55, 5: 50, 7: 45, 9: 40},
        3: {3: 90, 1: 80, 5: 75, 7: 70, 9: 65, 2: 55, 4: 50, 6: 45, 8: 40},
        4: {4: 90, 2: 85, 6: 80, 8: 75, 1: 50, 3: 45, 5: 40, 7: 35, 9: 30},
        5: {5: 90, 1: 75, 3: 70, 7: 65, 9: 60, 2: 55, 4: 50, 6: 45, 8: 40},
        6: {6: 90, 2: 80, 4: 75, 8: 70, 1: 60, 3: 55, 5: 50, 7: 45, 9: 40},
        7: {7: 90, 1: 70, 3: 65, 5: 60, 9: 55, 2: 50, 4: 45, 6: 40, 8: 35},
        8: {8: 90, 4: 80, 6: 75, 2: 70, 1: 60, 3: 50, 5: 45, 7: 40, 9: 35},
        9: {9: 90, 3: 70, 1: 65, 5: 60, 7: 55, 2: 50, 4: 45, 6: 40, 8: 35}
    }
    
    s1_base = soul1 if soul1 not in MASTER_NUMBERS else sum(int(d) for d in str(soul1))
    s2_base = soul2 if soul2 not in MASTER_NUMBERS else sum(int(d) for d in str(soul2))
    
    score = soul_harmony.get(s1_base, {}).get(s2_base, 50)
    
    # Determine description based on score
    if score >= 80:
        description = "Excellent soul urge harmony - Your inner desires align beautifully"
    elif score >= 65:
        description = "Good soul urge compatibility - You share similar inner motivations"
    elif score >= 50:
        description = "Moderate soul urge match - Some alignment but differences exist"
    else:
        description = "Challenging soul urge compatibility - Different inner desires"
    
    return score, description


def calculate_name_compatibility(name1: str, name2: str) -> Tuple[int, str]:
    """
    Calculate name compatibility based on numerological values.
    """
    num1 = calculate_name_number(name1)
    num2 = calculate_name_number(name2)
    
    # Calculate difference and determine harmony
    diff = abs(num1 - num2)
    
    # Numerologically, certain differences are more harmonious
    harmony_scores = {
        0: 95,  # Same number - very strong bond
        1: 75,
        2: 65,
        3: 70,
        4: 55,
        5: 80,
        6: 85,
        7: 60,
        8: 70,
    }
    
    score = harmony_scores.get(diff, 50)
    
    # Bonus for master numbers
    if num1 in MASTER_NUMBERS or num2 in MASTER_NUMBERS:
        score = min(95, score + 5)
    
    # Determine description based on score
    if score >= 80:
        description = "Excellent name harmony - Your names resonate well together"
    elif score >= 65:
        description = "Good name compatibility - There is positive energy between your names"
    elif score >= 50:
        description = "Moderate name match - Some harmony but may need work"
    else:
        description = "Challenging name compatibility - Different name energies"
    
    return score, description


def calculate_challenge_number(birth_date: str) -> int:
    """
    Calculate the main Challenge number (represents life's obstacles).
    Derived from birth date digits.
    """
    year, month, day = parse_birth_date(birth_date)
    
    if year == 0:
        return 0
    
    # Challenge: |month - day|, |day - year_sum|, |year_sum - month|, etc.
    year_sum = sum(int(d) for d in str(year))
    
    challenges = [
        abs(month - day),
        abs(day - year_sum),
        abs(year_sum - month),
    ]
    
    # Reduce each to single digit
    reduced = [reduce_to_single_digit(c) for c in challenges]
    
    # Final challenge is difference between first two
    final = abs(reduced[0] - reduced[1])
    
    return reduce_to_single_digit(final)


# ============================================
# LIFE PATH PREDICTIONS
# ============================================

LIFE_PATH_PREDICTIONS = {
    1: "You are a natural leader, independent and ambitious. You prefer to take initiative rather than follow others. Your path involves learning to balance independence with partnership.",
    2: "You are diplomatic, cooperative, and value harmony. You thrive in partnerships and seek balance in life. Your journey involves learning to assert yourself while maintaining peace.",
    3: "You are creative, expressive, and social. You bring joy to others through communication and creativity. Your path involves channeling your creative energy constructively.",
    4: "You are practical, hardworking, and reliable. You build stable foundations and value security. Your journey involves learning to embrace change while maintaining stability.",
    5: "You crave freedom, adventure, and variety. You adapt easily to change and embrace new experiences. Your path involves finding freedom within structure.",
    6: "You are responsible, caring, and family-oriented. You find fulfillment in nurturing relationships. Your journey involves balancing family responsibilities with self-care.",
    7: "You are introspective, analytical, and seek wisdom. You value truth and spiritual understanding. Your path involves integrating your inner wisdom with worldly engagement.",
    8: "You are ambitious, driven, and seek material success. You have strong organizational abilities. Your journey involves learning to balance material and spiritual pursuits.",
    9: "You are compassionate, idealistic, and humanitarian. You seek to make the world a better place. Your path involves learning to let go while remaining connected.",
    11: "You are an intuitive visionary with spiritual insight. You balance between dreams and practicality. Your path involves embracing your sensitivity while staying grounded.",
    22: "You are a master builder with exceptional capability. You turn ambitious dreams into reality. Your journey involves balancing grand visions with practical execution.",
    33: "You are a spiritual teacher focused on healing others. You embody unconditional love and compassion. Your path involves transcending personal concerns for universal service."
}


def get_prediction(life_path: int) -> str:
    """Get prediction text based on Life Path Number"""
    return LIFE_PATH_PREDICTIONS.get(life_path, "Your path is unique and awaits your discovery.")


# ============================================
# DYNAMIC LETTER/NAME GENERATION
# ============================================

def get_letter_for_number(target_num: int, prefer_vowel: bool = False) -> str:
    """
    Get a letter that reduces to the target number.
    Optionally prefer vowels or consonants.
    """
    matching_letters = []
    
    for letter, value in NUMEROLOGY_CHART.items():
        if value == target_num:
            is_vowel = letter in VOWELS
            if prefer_vowel and is_vowel:
                matching_letters.insert(0, letter)
            elif prefer_vowel and not is_vowel:
                continue
            else:
                matching_letters.append(letter)
    
    if not matching_letters:
        # Default to common letters
        return 'a' if target_num == 1 else 'k' if target_num == 2 else 's'
    
    return random.choice(matching_letters)


def generate_name_for_life_path(target_life_path: int, gender: str, length: int = 3) -> str:
    """
    Dynamically generate a name that harmonizes with a target Life Path number.
    
    The name is generated to create good numerological compatibility.
    """
    name_parts = []
    
    # First letter - most important (determines initial impression)
    first_letter = get_letter_for_number(reduce_to_single_digit(target_life_path))
    name_parts.append(first_letter.upper())
    
    # Additional letters to create a harmonious name number
    # We want the full name to have a destiny number compatible with the life path
    
    # Common name syllables that work well
    name_syllables = {
        1: ['an', 'ar', 'aj', 'av', 'ak', 'ad'],
        2: ['an', 'ai', 'am', 'as', 'ap', 'ad'],
        3: ['as', 'an', 'av', 'ar', 'a', 'ri'],
        4: ['an', 'ar', 'ak', 'an', 'as', 'ri'],
        5: ['ra', 'ak', 'an', 'ar', 'i', 'va'],
        6: ['an', 'aa', 'ak', 'ad', 'ar', 'ma'],
        7: ['an', 'av', 'as', 'ah', 'si', 'ha'],
        8: ['ra', 'av', 'ad', 'ar', 'ka', 'da'],
        9: ['an', 'av', 'ar', 'ah', 'ra', 'va'],
    }
    
    # Get syllables for the life path
    syllables = name_syllables.get(target_life_path, ['a', 'na', 'ra'])
    
    # Build remaining part of name
    remaining = length - 1
    for i in range(remaining):
        syllable = random.choice(syllables)
        name_parts.append(syllable)
    
    return ''.join(name_parts).title()


def generate_partner_name_suggestions(
    user_life_path: int, 
    user_destiny: int, 
    user_soul_urge: int,
    gender: str,
    count: int = 10
) -> List[Dict]:
    """
    Generate partner name suggestions based on user's numerology profile.
    
    Creates names that are numerically compatible with the user's numbers.
    """
    suggestions = []
    
    # Calculate what life path numbers would be most compatible
    # Based on actual numerological rules
    best_life_paths = {
        1: [1, 3, 5, 7, 9],
        2: [2, 4, 6, 8],
        3: [1, 3, 5, 7, 9],
        4: [2, 4, 6, 8],
        5: [1, 3, 5, 7, 9],
        6: [2, 4, 6, 8],
        7: [1, 3, 5, 7, 9],
        8: [2, 4, 6, 8],
        9: [1, 3, 5, 7, 9],
    }
    
    # Get compatible life paths
    compatible_lps = best_life_paths.get(user_life_path, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    # Generate names for compatible life paths
    used_names = set()
    
    for lp in compatible_lps:
        # Generate multiple names for each compatible life path
        for _ in range(3):
            # Generate name with appropriate length based on gender
            name_len = random.choice([3, 4, 5])
            name = generate_name_for_life_path(lp, gender, name_len)
            
            # Avoid duplicates
            if name in used_names:
                continue
            used_names.add(name)
            
            # Calculate the name's numerology
            name_number = calculate_name_number(name)
            soul_urge = calculate_soul_urge_number(name)
            
            suggestions.append({
                "suggested_name": name,
                "meaning": get_name_meaning(name, name_number),
                "name_number": name_number,
                "life_path_compatibility": lp,
                "soul_urge": soul_urge
            })
            
            if len(suggestions) >= count:
                break
        
        if len(suggestions) >= count:
            break
    
    # Sort by compatibility
    suggestions.sort(key=lambda x: x['life_path_compatibility'], reverse=True)
    
    return suggestions[:count]


def get_name_meaning(name: str, name_number: int) -> str:
    """Get the numerological meaning of a name based on its number."""
    meanings = {
        1: "Leadership, independence, pioneering spirit",
        2: "Diplomacy, cooperation, partnership",
        3: "Creativity, expression, joy",
        4: "Stability, practicality, foundation",
        5: "Freedom, adventure, versatility",
        6: "Harmony, family, responsibility",
        7: "Wisdom, spirituality, introspection",
        8: "Power, achievement, material success",
        9: "Compassion, humanitarianism, completion",
        11: "Intuition, vision, spiritual insight",
        22: "Master builder, practical vision",
        33: "Spiritual teacher, healing"
    }
    
    base_number = reduce_to_single_digit(name_number)
    return meanings.get(base_number, "Unique energy")


def get_first_letter_suggestions(user_life_path: int, count: int = 5) -> List[Dict]:
    """
    Generate first letter suggestions for partner names.
    Based on user's life path compatibility.
    """
    # Best first letters for each life path (dynamically calculated)
    letter_compatibility = {
        1: ['A', 'J', 'R'],      # 1: Leadership
        2: ['B', 'K', 'T'],      # 2: Partnership
        3: ['F', 'L', 'Y'],      # 3: Creativity
        4: ['C', 'M', 'V'],      # 4: Stability
        5: ['E', 'N', 'W'],      # 5: Freedom
        6: ['D', 'H', 'O'],      # 6: Harmony
        7: ['G', 'P', 'U'],      # 7: Wisdom
        8: ['A', 'I', 'Q'],      # 8: Power
        9: ['A', 'I', 'S'],      # 9: Compassion
        11: ['K', 'R', 'Y'],     # 11: Vision
        22: ['M', 'V', 'D'],     # 22: Builder
        33: ['M', 'S', 'H'],     # 33: Healing
    }
    
    letters = letter_compatibility.get(user_life_path, ['A', 'K', 'R', 'S', 'V'])
    
    letter_meanings = {
        'A': "New beginnings, leadership, independence",
        'B': "Sensitivity, cooperation, duality",
        'C': "Expression, creativity, communication",
        'D': "Stability, practicality, determination",
        'E': "Freedom, adventure, change",
        'F': "Family, responsibility, service",
        'G': "Spiritual, introspective, healing",
        'H': "Success, authority, material achievement",
        'I': "Intuition, spirituality, completeness",
        'J': "Wisdom, leadership, completion",
        'K': "Analysis, knowledge, enlightenment",
        'L': "Life path, balance, harmony",
        'M': "Emotion, sensitivity, nurturing",
        'N': "Intelligence, communication, adaptability",
        'O': "Love, responsibility, completeness",
        'P': "Spiritual, philosophical, humanitarian",
        'Q': "Originality, independence, achievement",
        'R': "Royalty, prosperity, leadership",
        'S': "Spirituality, intuition, sensitivity",
        'T': "Trust, faith, truth",
        'U': "Humanitarianism, independence",
        'V': "Victory, determination, practicality",
        'W': "Versatility, freedom, adventure",
        'X': "Romance, magnetism, spirituality",
        'Y': "Adventure, independence, creativity",
        'Z': "Spirituality, completion, idealism"
    }
    
    suggestions = []
    for letter in letters[:count]:
        suggestions.append({
            "suggested_name": letter,
            "meaning": letter_meanings.get(letter, "Positive energy"),
            "name_number": NUMEROLOGY_CHART.get(letter.lower(), 0)
        })
    
    return suggestions


# ============================================
# PARTNER RECOMMENDATION SYSTEM
# ============================================

LIFE_PATH_DESCRIPTIONS = {
    1: "Natural Leader - Independent, ambitious, and pioneering",
    2: "Diplomat - Cooperative, harmonious, and supportive",
    3: "Creative - Expressive, social, and joyful",
    4: "Stability Builder - Practical, reliable, and hardworking",
    5: "Freedom Seeker - Adventurous, adaptable, and versatile",
    6: "Nurturer - Responsible, caring, and family-focused",
    7: "Seeker - Introspective, analytical, and wise",
    8: "Achiever - Ambitious, powerful, and material-focused",
    9: "Humanitarian - Compassionate, idealistic, and generous",
    11: "Visionary - Intuitive, spiritual, and inspirational",
    22: "Master Builder - Practical visionary who turns dreams into reality",
    33: "Master Teacher - Healer who embodies unconditional love"
}


LIFE_PATH_COMPATIBILITY = {
    1: {
        "best": [1, 3, 5, 7, 9],
        "description": "You are a natural leader who values independence. Partners who are creative, adventurous, and self-motivated complement your ambitious nature."
    },
    2: {
        "best": [2, 4, 6, 8],
        "description": "You thrive in partnerships and seek harmony. Partners who are stable, supportive, and family-oriented create the best balance with your diplomatic nature."
    },
    3: {
        "best": [1, 3, 5, 7, 9],
        "description": "Your creative and social nature flourishes with partners who appreciate joy, expression, and variety in life."
    },
    4: {
        "best": [2, 4, 6, 8],
        "description": "Your practical and grounded nature pairs well with partners who value stability, loyalty, and long-term commitment."
    },
    5: {
        "best": [1, 3, 5, 7, 9],
        "description": "Your love for freedom and adventure is best complemented by partners who embrace change and new experiences."
    },
    6: {
        "best": [2, 4, 6, 8],
        "description": "Your nurturing and family-oriented nature seeks partners who appreciate responsibility and domestic harmony."
    },
    7: {
        "best": [1, 3, 5, 7, 9],
        "description": "Your introspective and wisdom-seeking nature is complemented by partners who value truth and spiritual understanding."
    },
    8: {
        "best": [2, 4, 6, 8],
        "description": "Your ambitious and achievement-oriented nature pairs well with partners who understand your drive for material success."
    },
    9: {
        "best": [1, 3, 5, 7, 9],
        "description": "Your compassionate and humanitarian nature is best matched with partners who share your idealism and desire to make a difference."
    },
    11: {
        "best": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33],
        "description": "As an intuitive visionary, you have broad compatibility. Your spiritual insight resonates best with those who appreciate your dual nature."
    },
    22: {
        "best": [2, 4, 6, 8, 11, 22],
        "description": "Your master builder energy pairs best with partners who support your ambitious dreams and appreciate your practical wisdom."
    },
    33: {
        "best": [3, 6, 9, 11, 33],
        "description": "Your spiritual teaching energy is most harmonious with partners who embody compassion and unconditional love."
    }
}


def calculate_compatibility_score(user_life_path: int, partner_life_path: int) -> int:
    """Calculate compatibility score between two life path numbers using actual numerology."""
    score, _ = calculate_life_path_compatibility(user_life_path, partner_life_path)
    return score


def get_full_numerology(name: str, birth_date: str) -> Dict:
    """Calculate all numerology numbers for a person"""
    life_path = calculate_life_path(birth_date)
    destiny = calculate_destiny_number(name)
    soul_urge = calculate_soul_urge_number(name)
    personality = calculate_personality_number(name)
    birth_day = calculate_birth_day_number(birth_date)
    challenge = calculate_challenge_number(birth_date)
    pinnacles = calculate_pinnacle_numbers(birth_date)
    prediction = get_prediction(life_path)
    
    return {
        "name": name,
        "life_path": life_path,
        "destiny_number": destiny,
        "soul_urge": soul_urge,
        "personality_number": personality,
        "birth_day_number": birth_day,
        "challenge_number": challenge,
        "pinnacles": pinnacles,
        "prediction": prediction
    }


def get_partner_recommendations(name: str, birth_date: str, gender: str) -> Dict:
    """Generate partner recommendations based on numerology with dynamic name generation"""
    # Calculate user's numerology
    life_path = calculate_life_path(birth_date)
    destiny = calculate_destiny_number(name)
    soul_urge = calculate_soul_urge_number(name)
    prediction = get_prediction(life_path)
    
    # Get compatible life path numbers using actual compatibility
    compatibility_info = LIFE_PATH_COMPATIBILITY.get(life_path, {
        "best": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "description": "Your unique path awaits discovery."
    })
    
    compatible_partners = []
    for partner_life_path in compatibility_info["best"]:
        score = calculate_compatibility_score(life_path, partner_life_path)
        partner_desc = LIFE_PATH_DESCRIPTIONS.get(partner_life_path, "Unknown")
        compatible_partners.append({
            "life_path_number": partner_life_path,
            "compatibility_score": score,
            "description": partner_desc,
            "partner_type": "Best Match" if score >= 80 else "Good Match"
        })
    
    # Sort by compatibility score
    compatible_partners.sort(key=lambda x: x["compatibility_score"], reverse=True)
    
    # Generate dynamic partner name suggestions
    letter_suggestions = get_first_letter_suggestions(life_path)
    
    # Generate full name suggestions
    full_name_suggestions = generate_partner_name_suggestions(
        life_path, destiny, soul_urge, gender, count=10
    )
    
    return {
        "user_name": name,
        "user_gender": gender,
        "user_life_path": life_path,
        "user_destiny_number": destiny,
        "user_soul_urge": soul_urge,
        "user_prediction": prediction,
        "compatible_partners": compatible_partners,
        "letter_suggestions": letter_suggestions,
        "full_name_suggestions": full_name_suggestions
    }


def calculate_match_compatibility_details(name1: str, birth_date1: str, name2: str, birth_date2: str) -> Dict:
    """
    Calculate detailed compatibility between two people using actual numerology.
    """
    # Life Path numbers
    lp1 = calculate_life_path(birth_date1)
    lp2 = calculate_life_path(birth_date2)
    life_path_score = calculate_life_path_compatibility(lp1, lp2)[0]
    
    # Destiny numbers
    dest1 = calculate_destiny_number(name1)
    dest2 = calculate_destiny_number(name2)
    destiny_score = calculate_destiny_compatibility(dest1, dest2)[0]
    
    # Soul Urge numbers
    soul1 = calculate_soul_urge_number(name1)
    soul2 = calculate_soul_urge_number(name2)
    soul_score = calculate_soul_urge_compatibility(soul1, soul2)[0]
    
    # Name compatibility
    name_score = calculate_name_compatibility(name1, name2)[0]
    
    # Calculate weighted final score
    # Life Path is most important (40%), Destiny (25%), Soul Urge (20%), Name (15%)
    final_score = int(
        (life_path_score * 0.40) + 
        (destiny_score * 0.25) + 
        (soul_score * 0.20) + 
        (name_score * 0.15)
    )
    
    return {
        "life_path": {
            "person1": lp1,
            "person2": lp2,
            "score": life_path_score,
            "description": LIFE_PATH_DESCRIPTIONS.get(lp1, "")[:50]
        },
        "destiny": {
            "person1": dest1,
            "person2": dest2,
            "score": destiny_score
        },
        "soul_urge": {
            "person1": soul1,
            "person2": soul2,
            "score": soul_score
        },
        "name": {
            "score": name_score
        },
        "overall_score": final_score
    }

