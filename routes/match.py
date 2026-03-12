from fastapi import APIRouter, HTTPException
from models.request_models import MatchRequest, MatchResponse
from services.astrology_service import calculate_match_compatibility

router = APIRouter(prefix="/api", tags=["Match"])


def validate_date(date_str: str, field_name: str) -> str:
    """Validate and parse date string"""
    from datetime import datetime
    from services.numerology_service import convert_date_format
    
    if not date_str:
        raise HTTPException(status_code=400, detail=f"Invalid {field_name}: Date cannot be empty")
    
    # Try to convert the date
    converted = convert_date_format(date_str)
    if not converted:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid {field_name}: Please use format DD-MM-YYYY (e.g., 15-03-1990) or YYYY-MM-DD (e.g., 1990-03-15)"
        )
    
    # Try to parse the converted date
    try:
        datetime.strptime(converted, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {field_name}: Please enter a valid date"
        )
    
    return converted


@router.post("/match-check", response_model=MatchResponse)
async def check_match(request: MatchRequest):
    """
    Check compatibility between two people
    
    - **male**: Male person's details (name, gender, birth_date, birth_time, birth_place)
    - **female**: Female person's details (name, gender, birth_date, birth_time, birth_place)
    """
    try:
        # Validate dates before processing
        male_birth_date = validate_date(request.male.birth_date, "male birth date")
        female_birth_date = validate_date(request.female.birth_date, "female birth date")
        
        male_data = {
            "name": request.male.name,
            "gender": request.male.gender,
            "birth_date": male_birth_date,
            "birth_time": request.male.birth_time,
            "birth_place": request.male.birth_place
        }
        
        female_data = {
            "name": request.female.name,
            "gender": request.female.gender,
            "birth_date": female_birth_date,
            "birth_time": request.female.birth_time,
            "birth_place": request.female.birth_place
        }
        
        result = calculate_match_compatibility(male_data, female_data)
        return MatchResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating match: {str(e)}")

