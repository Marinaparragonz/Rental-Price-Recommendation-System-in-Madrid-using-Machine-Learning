"""
Madrid Housing Dashboard - Main Application
AI-powered property price predictions for Madrid using Random Forest ML
"""

# =============================================================================
# IMPORTS AND SETUP
# =============================================================================
import streamlit as st
import sys
import os

# Add current directory to Python path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all components and utilities
from utils.styling_utils import apply_custom_css, add_map_cleanup_script
from components.header import render_header
from components.sidebar import render_sidebar
from components.map_component import render_map
from components.prediction_display import render_prediction_display, render_filters_summary, render_prediction_breakdown 
from components.market_insights import render_market_insights
from components.footer import render_footer

# =============================================================================
# STREAMLIT PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Madrid Housing Dashboard", 
    layout="wide", 
    page_icon="🏠",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': "https://github.com/your-repo/issues",
        'About': "# Madrid Housing Dashboard\nAI-powered property price predictions using Random Forest ML"
    }
)

# =============================================================================
# APPLY CUSTOM STYLING
# =============================================================================
apply_custom_css()

# =============================================================================
# INITIALIZE SESSION STATE
# =============================================================================
# Initialize session state variables if they don't exist
if 'last_selected_district' not in st.session_state:
    st.session_state.last_selected_district = None

if 'estimated_price' not in st.session_state:
    st.session_state.estimated_price = None

if 'prediction_method' not in st.session_state:
    st.session_state.prediction_method = None

if 'price_breakdown' not in st.session_state:
    st.session_state.price_breakdown = None

if 'rooms' not in st.session_state:
    st.session_state.rooms = 3

if 'bathrooms' not in st.session_state:
    st.session_state.bathrooms = 2

if 'area' not in st.session_state:
    st.session_state.area = 80

# =============================================================================
# MAIN DASHBOARD LAYOUT
# =============================================================================

def main():
    """Main function to render the complete dashboard"""
    
    # 1. HEADER SECTION
    render_header()
    
    # 2. SIDEBAR WITH FILTERS AND CONTROLS
    selected_amenities = render_sidebar()
    
    # 3. MAIN CONTENT AREA
    with st.container():
        
        # 3.1 PREDICTION DISPLAY SECTION (PRIMERO AHORA)
        st.markdown("---")
        render_prediction_display()

        # 3.1.1 PREDICTION BREAKDOWN SECTION
        render_prediction_breakdown()

        # 3.2 INTERACTIVE MAP SECTION (SEGUNDO AHORA)
        st.markdown("---")
        render_map()

        # 3.3 FILTERS SUMMARY SECTION
        render_filters_summary(selected_amenities)
        
        # Add map cleanup script to remove unwanted elements
        add_map_cleanup_script()
        
        # 3.4 MARKET INSIGHTS SECTION
        render_market_insights()

    
    # 4. FOOTER SECTION
    render_footer()

# =============================================================================
# EXCEPTION HANDLING
# =============================================================================

def safe_main():
    """Main function with exception handling"""
    try:
        main()
        
    except ImportError as e:
        st.error(f"Import Error: {str(e)}")
        st.info("Please ensure all required packages are installed and all component files are present.")
        st.code("""
        # Install required packages:
        pip install streamlit geopandas folium streamlit-folium pandas numpy scikit-learn joblib shapely
        """)
        
    except FileNotFoundError as e:
        st.error(f"File Not Found: {str(e)}")
        st.info("Please ensure all required data files are in the correct directory:")
        st.markdown("""
        **Required files:**
        - `madrid-districts.geojson` (for map)
        - `data_clean.csv` (for market insights)
        - `random_forest_model.pkl` (for AI predictions - optional)
        - `district_mapping.pkl` (for AI predictions - optional)
        - `model_features.pkl` (for AI predictions - optional)
        - `model_info.pkl` (for AI predictions - optional)
        """)
        
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
        st.info("Please check the console for detailed error information.")
        
        # Show error details in expander
        with st.expander("Error Details", expanded=False):
            st.code(f"""
            Error Type: {type(e).__name__}
            Error Message: {str(e)}
            
            Please check:
            1. All component files are present
            2. All required packages are installed
            3. Data files are in the correct location
            4. File permissions are correct
            """)

# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Run the dashboard with error handling
    safe_main()
    
    # Add some final styling touches
    st.markdown("""
    <style>
    /* Hide Streamlit's default elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar for webkit browsers */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    </style>
    """, unsafe_allow_html=True)