import pandas as pd
from fastapi import Depends, status, Response, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

# OAuth2
from Functions import oauth2

# Database
from Database.Database_Engine import get_db
from Database import roles_database

# My Functions
from Functions import General_Func as GF

# fertilizer_recommendation_router.py Router
from .fertilizer_recommendation_router import router

# AI Models
from Models.Fertilizer_Recommendation_Models.fertilizer_recommendation_models_loader import fertilizer_recommendation_models, fertilizer_recommendation_models_reverse_mappings


class Fertilizer_Recommendation_Request(BaseModel):
    Soil_color: int
    Nitrogen: float
    Phosphorus: float
    Potassium: float
    pH: float
    Rainfall: float
    Temperature: float
    Crop: int

    class Config:
        from_attributes = True


class Fertilizer_Recommendation_Response(BaseModel):
    xgboost_classification: str
    catBoost_classification: str
    random_forest_classification: str
    knn_classification: str
    decision_tree_classification: str

    class Config:
        from_attributes = True


class Custom_Fertilizer_Recommendation_Response(BaseModel):
    status: str
    message: str
    data: list[Fertilizer_Recommendation_Response]

    class Config:
        from_attributes = True
        
        

@router.post("/fertilizer_recommendation/recommend",
             status_code=status.HTTP_200_OK,
             response_model=Custom_Fertilizer_Recommendation_Response)
async def fertilizer_recommendation(
    POST_request_body: Fertilizer_Recommendation_Request,
    response: Response,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)):

    try:
        user_ID_status = await GF.check_Admin_User_Role_ID_Status(current_user)  # Check if the User ID is valid
        user_working_status = await GF.check_user_working_status(current_user)   # Check if the User is working

        if user_ID_status and user_working_status:
            # Create a DataFrame from the request features
            new_data = pd.DataFrame({
                "Soil_color": [POST_request_body.Soil_color],
                "Nitrogen": [POST_request_body.Nitrogen],
                "Phosphorus": [POST_request_body.Phosphorus],
                "Potassium": [POST_request_body.Potassium],
                "pH": [POST_request_body.pH],
                "Rainfall": [POST_request_body.Rainfall],
                "Temperature": [POST_request_body.Temperature],
                "Crop": [POST_request_body.Crop]    
            })

            predictions = {}

            ## Predict using each model
            # XGBoost
            xgboost_model = fertilizer_recommendation_models['xgboost_classification']
            xgboost_mapping = fertilizer_recommendation_models_reverse_mappings['xgboost_classification']
            xgboost_prediction = xgboost_model.predict(new_data).flatten()
            xgboost_labels = [xgboost_mapping[label] for label in xgboost_prediction]
            predictions['xgboost_classification'] = xgboost_labels[0]
            
            # CatBoost
            catboost_model = fertilizer_recommendation_models['catBoost_classification']
            catboost_mapping = fertilizer_recommendation_models_reverse_mappings['catBoost_classification']
            catboost_prediction = catboost_model.predict(new_data).flatten()
            catboost_labels = [catboost_mapping[label] for label in catboost_prediction]
            predictions['catBoost_classification'] = catboost_labels[0]
            
            # Random Forest
            random_forest_model = fertilizer_recommendation_models['random_forest_classification']
            random_forest_mapping = fertilizer_recommendation_models_reverse_mappings['random_forest_classification']
            random_forest_prediction = random_forest_model.predict(new_data).flatten()
            random_forest_labels = [random_forest_mapping[label] for label in random_forest_prediction]
            predictions['random_forest_classification'] = random_forest_labels[0]
            
            # KNN
            knn_model = fertilizer_recommendation_models['knn_classification']
            knn_mapping = fertilizer_recommendation_models_reverse_mappings['knn_classification']
            knn_prediction = knn_model.predict(new_data).flatten()
            knn_labels = [knn_mapping[label] for label in knn_prediction]
            predictions['knn_classification'] = knn_labels[0]
            
            
            # Decision Tree
            decision_tree_model = fertilizer_recommendation_models['decision_tree_classification']
            decision_tree_mapping = fertilizer_recommendation_models_reverse_mappings['decision_tree_classification']
            decision_tree_prediction = decision_tree_model.predict(new_data).flatten()
            predictions['decision_tree_classification'] = decision_tree_prediction[0]
            decision_tree_labels = [decision_tree_mapping[label] for label in decision_tree_prediction]
            predictions['decision_tree_classification'] = decision_tree_labels[0]
            
            return {'status': 'success',
                    'message': 'Crop recommendation successful',
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
