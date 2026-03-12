from fastapi import APIRouter, HTTPException
from models.request_models import NumerologyRequest, NumerologyResponse
from services.numerology_service import get_full_numerology
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Numerology"])


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


@router.post("/numerology", response_model=NumerologyResponse)
async def calculate_numerology(request: NumerologyRequest):
    """
    Calculate numerology numbers for a person
    
    - **name**: Person's full name
    - **birth_date**: Birth date in YYYY-MM-DD format
    """
    try:
        # Validate date before processing
        valid_birth_date = validate_date(request.birth_date)
        
        result = get_full_numerology(request.name, valid_birth_date)
        return NumerologyResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating numerology: {str(e)}")

