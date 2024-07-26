from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

## Routers
from Routers.auth import auth_router
from Routers.crop_recommendation import crop_recommendation_router
from Routers.fertilizer_recommendation import fertilizer_recommendation_router
from Routers.yield_prediction import yield_prediction_router

## Load AI Models
from Models.Crop_Recommendation_Models.crop_recommendation_models_loader import load_crop_recommendation_models
from Models.Fertilizer_Recommendation_Models.fertilizer_recommendation_models_loader import load_fertilizer_recommendation_models
from Models.Yield_Prediction_Models.yield_prediction_models_loader import load_yield_prediction_models


### Lifespan context manager ### 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    load_crop_recommendation_models()
    load_fertilizer_recommendation_models()
    load_yield_prediction_models()
    yield
    

### FastAPI App ### 
app = FastAPI(lifespan=lifespan)
  

### CORS Middleware ### 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### Default Route ###
@app.get("/")
def read_root():
    return {"message": "Project AgroAI API"} 


# Authentication Router
app.include_router(auth_router.router)

# Yield Prediction Router
app.include_router(yield_prediction_router.router)

# Crop Recommendation Router
app.include_router(crop_recommendation_router.router)

# Fertilizer Recommendation Router
app.include_router(fertilizer_recommendation_router.router)
