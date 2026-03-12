from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import match, numerology, partner_recommendation

app = FastAPI(
    title="Astrology Match & Numerology API",
    description="API for Match Compatibility and Numerology Calculations",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(match.router)
app.include_router(numerology.router)
app.include_router(partner_recommendation.router)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {
        "message": "Welcome to Astrology Match & Numerology API",
        "endpoints": {
            "match_check": "POST /api/match-check",
            "numerology": "POST /api/numerology",
            "partner_recommendation": "POST /api/partner-recommendation"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

