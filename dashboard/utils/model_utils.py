"""
Machine learning model utilities for Madrid housing price prediction
"""
import streamlit as st
import os
import pickle
import joblib
import pandas as pd
from config.constants import AMENITY_MAPPING, MODEL_FILES

# Default values for model features (based on Random Forest training)
DEFAULT_MODEL_VALUES = {
    # Building characteristics (typical Madrid values)
    'CADCONSTRUCTIONYEAR': 1980,     # Typical construction year
    'CADDWELLINGCOUNT': 20,          # Average dwellings per building
    'CADMAXBUILDINGFLOOR': 5,        # Typical floors in Madrid
    'BUILTTYPEID_2': 1,              # Most common building type
    
    # Amenities (default: not available)
    'HASLIFT': 0, 'HASAIRCONDITIONING': 0, 'HASPARKINGSPACE': 0,
    'HASWARDROBE': 0, 'HASBOXROOM': 0, 'HASTERRACE': 0,
    'HASSWIMMINGPOOL': 0, 'HASDOORMAN': 0, 'HASGARDEN': 0,
}

# Distance mapping for all Madrid districts (in km) - cached once
DISTRICT_DISTANCES = {
    'Centro': (0.5, 0.2, 0.3), 'Arganzuela': (1.5, 0.7, 0.4),
    'Retiro': (2.0, 1.5, 0.5), 'Salamanca': (2.5, 0.3, 0.4),
    'Chamartín': (3.0, 0.5, 0.6), 'Tetuán': (4.0, 1.0, 0.6),
    'Chamberí': (3.5, 1.2, 0.5), 'Fuencarral-El Pardo': (5.0, 1.8, 0.7),
    'Moncloa-Aravaca': (4.0, 1.5, 0.6), 'Latina': (6.0, 3.5, 0.8),
    'Carabanchel': (6.5, 4.0, 0.9), 'Usera': (5.5, 3.8, 0.7),
    'Puente de Vallecas': (7.0, 5.0, 0.8), 'Moratalaz': (6.0, 4.5, 0.7),
    'Ciudad Lineal': (6.5, 2.5, 0.7), 'Hortaleza': (7.5, 3.0, 0.8),
    'Villaverde': (8.0, 6.0, 1.0), 'Villa de Vallecas': (8.5, 5.5, 0.9),
    'Vicálvaro': (9.0, 6.5, 1.0), 'San Blas-Canillejas': (7.0, 4.0, 0.8),
    'Barajas': (9.5, 7.0, 1.1)
}

@st.cache_resource
def load_trained_model():
    """Load Random Forest model and components"""
    if not is_model_available():
        return None, None, None, None
    
    try:
        # Load model
        model = joblib.load(MODEL_FILES['model'])
        
        # Load components
        components = {}
        for key, file_path in [
            ('district_mapping', MODEL_FILES['district_mapping']),
            ('model_features', MODEL_FILES['model_features']),
            ('model_info', MODEL_FILES['model_info'])
        ]:
            with open(file_path, 'rb') as f:
                components[key] = pickle.load(f)
        
        return model, components['district_mapping'], components['model_features'], components['model_info']
        
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None

def predict_with_model(model, district_mapping, model_features, model_info, input_params):
    """Generate price prediction using Random Forest model"""
    try:
        # model_info parameter not used but kept for compatibility
        
        # Build complete model input
        model_input = _build_model_input(input_params, district_mapping, model_features)
        
        # Make prediction
        df_input = pd.DataFrame([model_input])
        df_input = df_input.reindex(columns=model_features, fill_value=0)
        prediction = model.predict(df_input)[0]
        
        return max(50000, int(prediction))  # Minimum price threshold
        
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

def _build_model_input(input_params, district_mapping, model_features):
    """Build complete input for model prediction"""
    # Start with default values
    model_input = DEFAULT_MODEL_VALUES.copy()
    
    # Add user inputs
    model_input.update({
        'CONSTRUCTEDAREA': input_params['area'],
        'ROOMNUMBER': input_params['rooms'],
        'BATHNUMBER': input_params['bathrooms'],
        'DISTRICT_CODE': _get_district_code(input_params.get('district'), district_mapping)
    })
    
    # Add district-specific distances
    distances = DISTRICT_DISTANCES.get(input_params.get('district'), (5.0, 3.0, 0.6))
    model_input.update({
        'DISTANCE_TO_CITY_CENTER': distances[0],
        'DISTANCE_TO_CASTELLANA': distances[1],
        'DISTANCE_TO_METRO': distances[2]
    })
    
    # Activate selected amenities
    for amenity in input_params.get('amenities', []):
        if amenity in AMENITY_MAPPING:
            amenity_code = AMENITY_MAPPING[amenity]
            if amenity_code in model_input:
                model_input[amenity_code] = 1
    
    # Ensure all model features are present
    for feature in model_features:
        if feature not in model_input:
            model_input[feature] = 0
    
    return model_input

def _get_district_code(district_name, district_mapping):
    """Convert district name to numeric code"""
    return district_mapping.get(district_name, 1)  # Centro default

def is_model_available():
    """Check if ML model is available and ready"""
    try:
        from sklearn.ensemble import RandomForestRegressor
        return os.path.exists(MODEL_FILES['model'])
    except ImportError:
        return False

def get_model_status():
    """Get model status for display"""
    if is_model_available():
        return " AI Model Ready", "#42E067"

