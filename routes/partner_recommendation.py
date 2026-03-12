from fastapi import APIRouter, HTTPException
from models.request_models import PartnerRecommendationRequest, PartnerRecommendationResponse
from services.numerology_service import get_partner_recommendations
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Partner Recommendation"])


def validate_date(date_str: str) -> str:
    """Validate and parse date string"""
    from services.numerology_service import convert_date_format
    
    if not date_str:
        raise HTTPException(status_code=400, detail="Invalid birth date: Date cannot be empty")
    
    # Try to convert the date
    converted = convert_date_format(date_str)
    if not converted:
        raise HTTPException(
            status_code=400, 
            detail="Invalid birth date: Please use format DD-MM-YYYY (e.g., 15-03-1990) or YYYY-MM-DD (e.g., 1990-03-15)"
        )
    
    # Try to parse the converted date
    try:
        datetime.strptime(converted, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid birth date: Please enter a valid date"
        )
    
    return converted


@router.post("/partner-recommendation", response_model=PartnerRecommendationResponse)
async def get_partner_recommendation(request: PartnerRecommendationRequest):
    """
    Generate partner recommendations based on numerology
    
    - **name**: Person's full name
    - **birth_date**: Birth date in YYYY-MM-DD format
    - **gender**: Gender: Male or Female
    """
    try:
        # Validate date before processing
        valid_birth_date = validate_date(request.birth_date)
        
        result = get_partner_recommendations(
            request.name, 
            valid_birth_date, 
            request.gender
        )
        return PartnerRecommendationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating partner recommendations: {str(e)}")

