
# FastAPI
from fastapi import APIRouter


### Yield Prediction Router ###
router = APIRouter(tags=["Yield Prediction"])



# Import the routes from get_yield_prediction
from .get_yield_prediction import *


