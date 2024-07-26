
# FastAPI
from fastapi import APIRouter


### Fertilizer Recommendation Router ###
router = APIRouter(tags=["Fertilizer Recommendation"])


# Import the routes from get_fertilizer_recommendation.py
from .get_fertilizer_recommendation import *


