
# FastAPI
from fastapi import APIRouter


### Crop Recommendation Router ###
router = APIRouter(tags=["Crop Recommendation"])


# Import the routes from get_crop_recommendation
from .get_crop_recommendation import *


