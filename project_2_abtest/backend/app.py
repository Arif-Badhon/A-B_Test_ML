from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
import models
import routes.experiments as experiments_route
import routes.results as results_route
import routes.power_analysis as power_route
from config import settings

# Create database tables
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A complete A/B testing platform with statistical services and power analysis."
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(experiments_route.router, prefix=settings.API_V1_STR)
app.include_router(results_route.router, prefix=settings.API_V1_STR)
app.include_router(power_route.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
