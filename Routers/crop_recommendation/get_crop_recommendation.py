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

# crop_recommendation_router.py Router
from .crop_recommendation_router import router

# AI Models
from Models.Crop_Recommendation_Models.crop_recommendation_models_loader import crop_recommendation_models, crop_recommendation_models_reverse_mappings


class Crop_Recommendation_Request(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

    class Config:
        from_attributes = True


class Crop_Recommendation_Response(BaseModel):
    catBoost_classification: str
    decision_tree_classification: str
    random_forest_classification: str
    xgboost_classification: str
    svm_classification: str

    class Config:
        from_attributes = True


class Custom_Crop_Recommendation_Response(BaseModel):
    status: str
    message: str
    data: list[Crop_Recommendation_Response]

    class Config:
        from_attributes = True


@router.post("/crop_recommendation/recommend",
             status_code=status.HTTP_200_OK,
             response_model=Custom_Crop_Recommendation_Response)
async def crop_recommendation(
    POST_request_body: Crop_Recommendation_Request,
    response: Response,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)):

    try:
        user_ID_status = await GF.check_Admin_User_Role_ID_Status(current_user)  # Check if the User ID is valid
        user_working_status = await GF.check_user_working_status(current_user)   # Check if the User is working

        if user_ID_status and user_working_status:
            # Create a DataFrame from the request features
            new_data = pd.DataFrame({
                "N": [POST_request_body.N],
                "P": [POST_request_body.P],
                "K": [POST_request_body.K],
                "temperature": [POST_request_body.temperature],
                "humidity": [POST_request_body.humidity],
                "ph": [POST_request_body.ph],
                "rainfall": [POST_request_body.rainfall]
            })

            predictions = {}

            ## Predict using each model

            # CatBoost
            catboost_model = crop_recommendation_models['catBoost_classification']
            catboost_mapping = crop_recommendation_models_reverse_mappings['catBoost_classification']
            catboost_prediction = catboost_model.predict(new_data).flatten()
            catboost_labels = [catboost_mapping[label] for label in catboost_prediction]
            predictions['catBoost_classification'] = catboost_labels[0]

            # Decision Tree
            decision_tree_model = crop_recommendation_models['decision_tree_classification']
            decision_tree_prediction = decision_tree_model.predict(new_data).flatten()
            predictions['decision_tree_classification'] = decision_tree_prediction[0]

            # Random Forest
            random_forest_model = crop_recommendation_models['random_forest_classification']
            random_forest_prediction = random_forest_model.predict(new_data).flatten()
            predictions['random_forest_classification'] = random_forest_prediction[0]

            # XGBoost
            xgboost_model = crop_recommendation_models['xgboost_classification']
            xgboost_mapping = crop_recommendation_models_reverse_mappings['xgboost_classification']
            xgboost_prediction = xgboost_model.predict(new_data).flatten()
            xgboost_labels = [xgboost_mapping[label] for label in xgboost_prediction]
            predictions['xgboost_classification'] = xgboost_labels[0]

            # SVM
            svm_model = crop_recommendation_models['svm_classification']
            svm_mapping = crop_recommendation_models_reverse_mappings['svm_classification']
            svm_prediction = svm_model.predict(new_data).flatten()
            svm_labels = [svm_mapping[label] for label in svm_prediction]
            predictions['svm_classification'] = svm_labels[0]

            
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
