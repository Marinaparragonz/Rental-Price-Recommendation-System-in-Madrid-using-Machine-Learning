"""
Machine learning model utilities
"""
import streamlit as st
import os
import pickle
import joblib
import pandas as pd
from config.constants import AMENITY_MAPPING, MODEL_FILES

# Check for library availability
try:
    from sklearn.ensemble import RandomForestRegressor
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

@st.cache_resource
def load_trained_model():
    """Load the trained Random Forest model and its components"""
    try:
        if SKLEARN_AVAILABLE and os.path.exists(MODEL_FILES['model']):
            model = joblib.load(MODEL_FILES['model'])
            
            with open(MODEL_FILES['district_mapping'], 'rb') as f:
                district_mapping = pickle.load(f)
            
            with open(MODEL_FILES['model_features'], 'rb') as f:
                model_features = pickle.load(f)
                
            with open(MODEL_FILES['model_info'], 'rb') as f:
                model_info = pickle.load(f)
            
            return model, district_mapping, model_features, model_info
        else:
            return None, None, None, None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None

def predict_with_model(model, district_mapping, model_features, model_info, input_params):
    """Make prediction using the Random Forest model"""
    try:
        # Create input dictionary with default values
        model_input = {
            'CONSTRUCTEDAREA': input_params['area'],
            'ROOMNUMBER': input_params['rooms'],
            'BATHNUMBER': input_params['bathrooms'],
            'HASTERRACE': 0,
            'HASLIFT': 0,
            'HASAIRCONDITIONING': 0,
            'HASGARDEN': 0,
            'HASPARKINGSPACE': 0,
            'HASBOXROOM': 0,
            'HASWARDROBE': 0,
            'HASDOORMAN': 0,
            'HASSWIMMINGPOOL': 0,
            'DISTANCE_TO_CITY_CENTER': 5.0,
            'DISTANCE_TO_METRO': 0.5,
            'DISTANCE_TO_CASTELLANA': 3.0,
            'CADCONSTRUCTIONYEAR': 1980,
            'CADMAXBUILDINGFLOOR': 5,
            'CADDWELLINGCOUNT': 20,
            'BUILTTYPEID_2': 1,
        }
        
        # Map selected district to DISTRICT_CODE
        selected_district = input_params.get('district', 'Centro')
        if selected_district in district_mapping:
            model_input['DISTRICT_CODE'] = district_mapping[selected_district]
        else:
            model_input['DISTRICT_CODE'] = 1
            st.warning(f"District '{selected_district}' not found in mapping. Using Centro as default.")
        
        # Activate selected amenities
        for amenity in input_params.get('amenities', []):
            if amenity in AMENITY_MAPPING:
                model_input[AMENITY_MAPPING[amenity]] = 1
        
        # Create DataFrame and make prediction
        df_input = pd.DataFrame([model_input])
        df_input = df_input.reindex(columns=model_features, fill_value=0)
        prediction = model.predict(df_input)[0]
        
        return max(50000, int(prediction))
        
    except Exception as e:
        st.error(f"Error in prediction: {e}")
        return None

def is_model_available():
    """Check if the ML model is available"""
    return SKLEARN_AVAILABLE and os.path.exists(MODEL_FILES['model'])

def get_model_status():
    """Get model status for display"""
    if is_model_available():
        return " AI Model Ready", "#105921"
    else:
        return "📊 Formula Mode", "#ffc107"