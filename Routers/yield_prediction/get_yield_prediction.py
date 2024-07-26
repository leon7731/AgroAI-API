
import pandas as pd

# FastAPI
from fastapi import Depends, status, Response
from pydantic import BaseModel

# OAuth2
from Functions import oauth2

# Database
from sqlalchemy.orm import Session
from Database.Database_Engine import get_db
from Database import roles_database

# My Functions
from Functions import General_Func as GF

# yield_prediction_router.py Router
from .yield_prediction_router import router

# AI Models
from Models.Yield_Prediction_Models.yield_prediction_models_loader import yield_prediction_models


class Yield_Prediction_Request(BaseModel):
    Soil_Quality: float
    Seed_Variety: float
    Fertilizer_Amount_kg_per_hectare: float
    Sunny_Days: float
    Rainfall_mm: float
    Irrigation_Schedule: float

    class Config:
        from_attributes = True
        

class Yield_Prediction_Response(BaseModel):
    elastic_net_regression: float
    lasso_regression: float
    linear_regression: float
    polynomial_regression: float
    ridge_regression: float
 

    class Config:
        from_attributes = True


class Custom_Yield_Prediction_Response(BaseModel):
    status: str
    message: str
    data: list[Yield_Prediction_Response]

    class Config:
        from_attributes = True


@router.post("/yield_prediction/predict", 
             status_code=status.HTTP_200_OK,
             response_model=Custom_Yield_Prediction_Response, 
            )
async def predict_yield(
    POST_request_body: Yield_Prediction_Request,
    response: Response,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)):
    
    try:
        user_ID_status = await GF.check_Admin_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = await GF.check_user_working_status(current_user) # Check if the User is working

        if (user_ID_status == True) and (user_working_status == True):
            # List of models to use
            model_keys = [
                'elastic_net_regression', 
                'lasso_regression', 
                'linear_regression',
                'polynomial_regression',
                'ridge_regression'
            ]  
            
            predictions = {}
            
            # Create a DataFrame from the request features
            new_data = pd.DataFrame({
                "Soil_Quality": [POST_request_body.Soil_Quality],
                "Seed_Variety": [POST_request_body.Seed_Variety],
                "Fertilizer_Amount_kg_per_hectare": [POST_request_body.Fertilizer_Amount_kg_per_hectare],
                "Sunny_Days": [POST_request_body.Sunny_Days],
                "Rainfall_mm": [POST_request_body.Rainfall_mm],
                "Irrigation_Schedule": [POST_request_body.Irrigation_Schedule]
            })
            
            # Predict using each model
            for key in model_keys:
                model = yield_prediction_models.get(key)
                if model:
                    prediction = round(model.predict(new_data)[0], 2)
                    predictions[key] = prediction
                else:
                    predictions[key] = "Model not found"
                    
                                       
            return {'status': 'success',
                    'message': 'Yield prediction successful',
                    'data': [predictions]}
                    
            
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'status': 'error',
                    'message': 'Unauthorized Access',
                    'data': []}
                    
        
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
        return {'status': 'error',
                'message': 'An error occurred while processing the request',
                'data': []}
    
