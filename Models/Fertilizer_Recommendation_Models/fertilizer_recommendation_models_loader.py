import joblib
from typing import Dict

fertilizer_recommendation_models: Dict[str, any] = {}
fertilizer_recommendation_models_ordinal_mappings: Dict[str, any] = {}
fertilizer_recommendation_models_reverse_mappings: Dict[str, dict] = {}

def load_fertilizer_recommendation_models():
    global fertilizer_recommendation_models, fertilizer_recommendation_models_ordinal_mappings, fertilizer_recommendation_models_reverse_mappings
    
    # Load the saved models
    fertilizer_recommendation_models['xgboost_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/xgboost_model_pipeline.joblib')
    fertilizer_recommendation_models['catBoost_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/catboost_model_pipeline.joblib')
    fertilizer_recommendation_models['random_forest_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/random_forest_model_pipeline.joblib')
    fertilizer_recommendation_models['knn_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/knn_model_pipeline.joblib')
    fertilizer_recommendation_models['decision_tree_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/decision_tree_model_pipeline.joblib')


    # Load the ordinal mappings
    fertilizer_recommendation_models_ordinal_mappings['xgboost_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/xgboost_model_ordinal_mappings.joblib')
    fertilizer_recommendation_models_ordinal_mappings['catBoost_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/catboost_model_ordinal_mappings.joblib')
    fertilizer_recommendation_models_ordinal_mappings['random_forest_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/random_forest_model_ordinal_mappings.joblib')
    fertilizer_recommendation_models_ordinal_mappings['knn_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/knn_model_ordinal_mappings.joblib')
    fertilizer_recommendation_models_ordinal_mappings['decision_tree_classification'] = joblib.load(r'Models/Fertilizer_Recommendation_Models/decision_tree_model_ordinal_mappings.joblib')

    # Create reverse mappings for ordinal mappings labels
    for key, mapping in fertilizer_recommendation_models_ordinal_mappings.items():
        fertilizer_recommendation_models_reverse_mappings[key] = {v: k for k, v in mapping['Fertilizer'].items()}