import joblib
from typing import Dict

yield_prediction_models: Dict[str, any] = {}

def load_yield_prediction_models():
    global yield_prediction_models
    yield_prediction_models['elastic_net_regression'] = joblib.load(r'Models/Yield_Prediction_Models/ElasticNet_regression_model_pipeline.joblib')
    yield_prediction_models['lasso_regression'] = joblib.load(r'Models/Yield_Prediction_Models/Lasso_regression_model_pipeline.joblib')
    yield_prediction_models['linear_regression'] = joblib.load(r'Models/Yield_Prediction_Models/linear_regression_model_pipeline.joblib')
    yield_prediction_models['polynomial_regression'] = joblib.load(r'Models/Yield_Prediction_Models/polynomial_regression_model_pipeline.joblib')
    yield_prediction_models['ridge_regression'] = joblib.load(r'Models/Yield_Prediction_Models/ridge_regression_model_pipeline.joblib')
