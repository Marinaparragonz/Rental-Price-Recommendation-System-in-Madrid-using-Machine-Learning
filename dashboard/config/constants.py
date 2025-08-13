"""
Configuration constants for the Madrid Housing Dashboard
"""
import os

# Base directory configuration - going up two levels from config folder to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = BASE_DIR

# Data file paths
DATA_FILES = {
    'clean_data': os.path.join(DATA_DIR, 'data_clean.csv'),
    'geojson': os.path.join(DATA_DIR, 'madrid-districts.geojson'),
    'model': os.path.join(DATA_DIR, 'random_forest_model.pkl')
}

# Map configuration
MADRID_CENTER = [40.4168, -3.7038]
DEFAULT_ZOOM = 12
GEOJSON_FILE = os.path.join(DATA_DIR, "madrid-districts.geojson")

# Amenities mapping
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

# Amenities options for multiselect
AMENITIES_OPTIONS = [
    " Lift", " Air Conditioning", " Parking Space", " Built-in Wardrobe",
    " Storage Room", " Terrace", " Swimming Pool", " Doorman", " Garden"
]

# Color schemes
COLOR_SCHEMES = {
    'success': ('#28a745', '#155724'),
    'error': ('#dc3545', '#c82333'),
    'warning': ('#ffc107', '#fd7e14'),
    'primary': ('#667eea', '#764ba2')
}

# User-friendly amenity names
AMENITY_NAMES = {
    'HASTERRACE': 'Terrace',
    'HASLIFT': 'Lift',
    'HASAIRCONDITIONING': 'Air Conditioning',
    'HASGARDEN': 'Garden',
    'HASPARKINGSPACE': 'Parking Space',
    'HASBOXROOM': 'Storage Room',
    'HASWARDROBE': 'Built-in Wardrobe',
    'HASDOORMAN': 'Doorman',
    'HASSWIMMINGPOOL': 'Swimming Pool'
}

# Model file paths
MODEL_FILES = {
    'model': os.path.join(DATA_DIR, 'random_forest_model.pkl'),
    'district_mapping': os.path.join(DATA_DIR, 'district_mapping.pkl'),
    'model_features': os.path.join(DATA_DIR, 'model_features.pkl'),
    'model_info': os.path.join(DATA_DIR, 'model_info.pkl')
}

# Debug: Print paths for verification (remove in production)
if __name__ == "__main__":
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"Data clean file: {DATA_FILES['clean_data']}")
    print(f"File exists: {os.path.exists(DATA_FILES['clean_data'])}")