from pydantic import BaseModel, Field
from typing import Optional


class PersonDetails(BaseModel):
    name: str = Field(..., description="Person's full name")
    gender: str = Field(..., description="Gender: Male or Female")
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD or DD-MM-YYYY format")
    birth_time: str = Field(..., description="Birth time in HH:MM AM/PM format")
    birth_place: str = Field(..., description="Birth place location")


class MatchRequest(BaseModel):
    male: PersonDetails
    female: PersonDetails


class NumerologyRequest(BaseModel):
    name: str = Field(..., description="Person's full name")
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD or DD-MM-YYYY format")


class MatchResponse(BaseModel):
    couple: str
    score: int
    category: str
    summary: str
    details: dict


class NumerologyResponse(BaseModel):
    name: str
    life_path: int
    destiny_number: int
    soul_urge: int
    personality_number: int
    birth_day_number: int
    challenge_number: int
    pinnacles: dict
    prediction: str


class PartnerRecommendationRequest(BaseModel):
    name: str = Field(..., description="Person's full name")
    birth_date: str = Field(..., description="Birth date in YYYY-MM-DD or DD-MM-YYYY format")
    gender: str = Field(..., description="Gender: Male or Female")


class CompatiblePartner(BaseModel):
    life_path_number: int
    compatibility_score: int
    description: str
    partner_type: str


class LetterSuggestion(BaseModel):
    suggested_name: str
    meaning: str
    name_number: int


class FullNameSuggestion(BaseModel):
    suggested_name: str
    meaning: str
    name_number: int
    life_path_compatibility: int
    soul_urge: int


class PartnerRecommendationResponse(BaseModel):
    user_name: str
    user_gender: str
    user_life_path: int
    user_destiny_number: int
    user_soul_urge: int
    user_prediction: str
    compatible_partners: list[CompatiblePartner]
    letter_suggestions: list[LetterSuggestion]
    full_name_suggestions: list[FullNameSuggestion]

