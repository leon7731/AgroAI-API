import joblib
from typing import Dict

crop_recommendation_models: Dict[str, any] = {}
crop_recommendation_models_ordinal_mappings: Dict[str, any] = {}
crop_recommendation_models_reverse_mappings: Dict[str, dict] = {}

def load_crop_recommendation_models():
    global crop_recommendation_models, crop_recommendation_models_ordinal_mappings, crop_recommendation_models_reverse_mappings
    
    # Load the saved models
    crop_recommendation_models['catBoost_classification'] = joblib.load(r'Models/Crop_Recommendation_Models/catboost_model_pipeline.joblib')
    crop_recommendation_models['decision_tree_classification'] = joblib.load(r'Models/Crop_Recommendation_Models/decision_tree_model_pipeline.joblib')
    crop_recommendation_models['random_forest_classification'] = joblib.load(r'Models/Crop_Recommendation_Models/random_forest_model_pipeline.joblib')
    crop_recommendation_models['xgboost_classification'] = joblib.load(r'Models/Crop_Recommendation_Models/xgboost_model_pipeline.joblib')
    crop_recommendation_models['svm_classification'] = joblib.load(r'Models/Crop_Recommendation_Models/svm_model_pipeline.joblib')

    # Load the ordinal mappings
    crop_recommendation_models_ordinal_mappings['catBoost_classification'] = joblib.load(r'Models/Crop_Recommendation_Models/catboost_model_ordinal_mappings.joblib')
    crop_recommendation_models_ordinal_mappings['xgboost_classification'] = joblib.load(r'Models/Crop_Recommendation_Models/xgboost_model_ordinal_mappings.joblib')
    crop_recommendation_models_ordinal_mappings['svm_classification'] = joblib.load(r'Models/Crop_Recommendation_Models/svm_model_ordinal_mappings.joblib')
    
    # Create reverse mappings for ordinal mappings labels
    for key, mapping in crop_recommendation_models_ordinal_mappings.items():
        crop_recommendation_models_reverse_mappings[key] = {v: k for k, v in mapping['label'].items()}