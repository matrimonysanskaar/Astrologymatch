from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import match, numerology, partner_recommendation

app = FastAPI(
    title="Astrology Match & Numerology API",
    description="API for Match Compatibility and Numerology Calculations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(match.router)
app.include_router(numerology.router)
app.include_router(partner_recommendation.router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")


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


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)

