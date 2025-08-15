"""
Configuration constants for the Madrid Housing Dashboard
"""
import os

# Base directory configuration 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Core amenity mapping (single source of truth)
AMENITY_MAPPING = {
    ' Terrace': 'HASTERRACE',
    ' Lift': 'HASLIFT', 
    ' Air Conditioning': 'HASAIRCONDITIONING',
    ' Garden': 'HASGARDEN',
    ' Parking Space': 'HASPARKINGSPACE',
    ' Storage Room': 'HASBOXROOM',
    ' Built-in Wardrobe': 'HASWARDROBE',
    ' Doorman': 'HASDOORMAN',
    ' Swimming Pool': 'HASSWIMMINGPOOL'
}


AMENITY_NAMES = {v: k.strip() for k, v in AMENITY_MAPPING.items()}
AMENITIES_OPTIONS = sorted(AMENITY_MAPPING.keys())

# Data file paths
DATA_FILES = {
    'clean_data': os.path.join(DATA_DIR, 'data_clean.csv'),
    'geojson': os.path.join(DATA_DIR, 'madrid-districts.geojson'),
}

# Model file paths
MODEL_FILES = {
    'model': os.path.join(MODELS_DIR, 'random_forest_model.pkl'),
    'district_mapping': os.path.join(MODELS_DIR, 'district_mapping.pkl'),
    'model_features': os.path.join(MODELS_DIR, 'model_features.pkl'),
    'model_info': os.path.join(MODELS_DIR, 'model_info.pkl')
}

# Map configuration
MADRID_CENTER = [40.4168, -3.7038]
DEFAULT_ZOOM = 12

COLOR_SCHEMES = {
    'success': ('#28a745', '#155724'),
    'error': ('#dc3545', '#c82333'),
    'warning': ('#ffc107', '#fd7e14'),
    'primary': ('#667eea', '#764ba2')
}
