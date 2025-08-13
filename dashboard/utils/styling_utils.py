"""
Styling utilities and CSS components for the dashboard
"""
import streamlit as st
from config.constants import COLOR_SCHEMES

def apply_custom_css():
    """Apply all custom CSS styles to the dashboard"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Main application background with gradient */
        html, body, .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Inter', sans-serif;
            height: 100vh;
            margin: 0;
            padding: 0;
        }

        /* Main content container with glass morphism effect */
        .block-container {
            padding: 2rem 2rem 3rem 2rem;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            margin: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }

        /* Sidebar styling with enhanced transparency and blur effects */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: #2c3e50;
            border-top-right-radius: 25px;
            border-bottom-right-radius: 25px;
            padding: 25px;
            box-shadow: 4px 0 20px rgba(102, 126, 234, 0.15);
        }

        /* Sidebar text styling for better readability */
        section[data-testid="stSidebar"] .stMarkdown {
            color: #2c3e50;
        }
        
        section[data-testid="stSidebar"] h2 {
            color: #2c3e50 !important;
            font-weight: 700;
        }
        
        section[data-testid="stSidebar"] h3 {
            color: #34495e !important;
            font-weight: 600;
        }
        
        section[data-testid="stSidebar"] p {
            color: #34495e !important;
        }

        /* Main heading styling with text shadow effects */
        h1 {
            color: white;
            font-size: 3.5rem;
            font-weight: 700;
            text-align: center;
            margin: 1rem 0 2rem 0;
            text-shadow: 0 4px 15px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(0, 0, 0, 0.3);
            filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.3));
        }

        /* Secondary headings styling */
        h2, .stSubheader {
            color: white;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        h3 {
            color: #e0e6ff;
            font-size: 1.2rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }

        /* Interactive button styling with hover effects */
        div.stButton > button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            font-weight: 600;
            border-radius: 15px;
            border: none;
            padding: 12px 30px;
            margin-top: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            font-size: 1rem;
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            background: linear-gradient(45deg, #764ba2, #667eea);
        }

        /* Form elements styling (sliders, multiselect) */
        .stSlider > div {
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.6);
            color: #2c3e50;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .stMultiSelect > div {
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 25px;
            border: 1px solid rgba(255, 255, 255, 0.6);
            color: #2c3e50;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Enhanced label styling for form elements */
        section[data-testid="stSidebar"] .stSlider label,
        section[data-testid="stSidebar"] .stMultiSelect label {
            color: #2c3e50 !important;
            font-weight: 900 !important;
            font-size: 1.5rem !important;
            margin-bottom: 12px !important;
            display: block !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.15) !important;
            letter-spacing: 0.5px !important;
            line-height: 1.3 !important;
            text-transform: capitalize !important;
        }
        
        /* Enhanced sidebar button styling */
        section[data-testid="stSidebar"] div.stButton > button {
            background: linear-gradient(45deg, #667eea, #764ba2) !important;
            color: white !important;
            font-weight: 700 !important;
            border-radius: 15px !important;
            border: none !important;
            padding: 15px 25px !important;
            margin-top: 100px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
            font-size: 1.1rem !important;
            width: 100% !important;
            cursor: pointer !important;
        }

        section[data-testid="stSidebar"] div.stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
            background: linear-gradient(45deg, #764ba2, #667eea) !important;
        }

        /* Expandable sections styling */
        .stExpander {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin: 1rem 0;
        }

        .stExpander > div > div {
            background: transparent;
        }
        
        .stExpander summary {
            color: white !important;
            font-weight: 600 !important;
        }

        /* General markdown text styling */
        .stMarkdown {
            color: white;
        }

        /* Metric cards styling with hover effects */
        .metric-container {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(255, 255, 255, 0.4);
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .metric-container:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(102, 126, 234, 0.6);
            background: rgba(255, 255, 255, 0.25);
        }

        /* Map popup removal */
        .folium-map .leaflet-popup-pane {
            display: none !important;
        }
        
        .folium-map .leaflet-popup {
            display: none !important;
        }
        
        .folium-map .leaflet-tooltip {
            display: block !important;
            pointer-events: none !important;
        }

        /* Metric value and label styling */
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            margin-bottom: 5px;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }

        .metric-label {
            font-size: 1rem;
            color: white;
            font-weight: 600;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        }

        /* Map container styling */
        .map-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            width: 100%;
            overflow: hidden;
        }
        
        iframe[title="streamlit_folium.st_folium"] {
            width: 100% !important;
            height: 600px !important;
            border-radius: 15px;
        }
        
        /* Information cards styling */
        .info-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 25px;
            margin: 15px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            transition: all 0.3s ease;
        }
        
        .info-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(102, 126, 234, 0.4);
        }

        /* Selected tags/chips styling in multiselect */
        section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] {
            background: linear-gradient(45deg, #667eea, #764ba2) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 4px 8px !important;
            margin: 2px !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(value, label, icon=""):
    """Create a metric card with consistent styling"""
    return f"""
    <div class='metric-container'>
        <div class='metric-value'>{icon} {value}</div>
        <div class='metric-label'>{label}</div>
    </div>
    """

def create_status_card(title, subtitle, card_type="info", icon=""):
    """Create a status card with different color schemes"""
    colors = COLOR_SCHEMES.get(card_type, COLOR_SCHEMES['primary'])
    
    return f"""
    <div style='background: linear-gradient(135deg, {colors[0]} 0%, {colors[1]} 100%); 
                padding: 2rem; 
                border-radius: 20px; 
                text-align: center; 
                margin: 1.5rem 0; 
                box-shadow: 0 15px 35px rgba({_hex_to_rgba(colors[0])}, 0.4), 0 5px 15px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(20px);'>
        <h2 style='color: white; margin: 0 0 0.5rem 0; font-size: 2rem; font-weight: 800; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);'>{icon} {title}</h2>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.1rem; font-weight: 600;'>{subtitle}</p>
    </div>
    """

def create_info_card_container(content):
    """Create an info card container with consistent styling"""
    return f"""
    <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.2);'>
        {content}
    </div>
    """

def _hex_to_rgba(hex_color):
    """Convert hex color to rgba values"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"{r}, {g}, {b}"

def add_map_cleanup_script():
    """Add JavaScript to remove unwanted map elements"""
    st.markdown("""
    <script>
    function removeUnwantedMapElements() {
        const popups = document.querySelectorAll('.leaflet-popup, .leaflet-popup-pane, .leaflet-popup-content-wrapper, .leaflet-popup-tip');
        popups.forEach(popup => {
            popup.style.display = 'none';
            popup.style.visibility = 'hidden';
            popup.style.opacity = '0';
            popup.remove();
        });
        
        const overlays = document.querySelectorAll('.leaflet-overlay-pane .leaflet-interactive');
        overlays.forEach(overlay => {
            overlay.style.outline = 'none';
            overlay.style.boxShadow = 'none';
        });
    }
    
    removeUnwantedMapElements();
    const observer = new MutationObserver(removeUnwantedMapElements);
    const mapContainer = document.querySelector('.folium-map');
    if (mapContainer) {
        observer.observe(mapContainer, { childList: true, subtree: true });
    }
    
    setInterval(removeUnwantedMapElements, 1000);
    </script>
    """, unsafe_allow_html=True)