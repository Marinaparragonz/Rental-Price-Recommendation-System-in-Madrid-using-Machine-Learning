import streamlit as st 
import geopandas as gpd
from streamlit_folium import st_folium
import folium
import pandas as pd
import numpy as np
import os
import pickle

try:
    from shapely.geometry import Point
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False

try:
    import joblib
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# --- Funciones para el modelo Random Forest ---

@st.cache_resource
def load_trained_model():
    """Carga el modelo Random Forest entrenado y sus componentes asociados"""
    try:
        if SKLEARN_AVAILABLE and os.path.exists('random_forest_model.pkl'):
            # Cargar modelo
            model = joblib.load('random_forest_model.pkl')
            
            # Cargar mapping de distrito nombre -> DISTRICT_CODE
            with open('district_mapping.pkl', 'rb') as f:
                district_mapping = pickle.load(f)
            
            # Cargar features que usa el modelo
            with open('model_features.pkl', 'rb') as f:
                model_features = pickle.load(f)
                
            # Cargar información del modelo (opcional)
            with open('model_info.pkl', 'rb') as f:
                model_info = pickle.load(f)
            
            return model, district_mapping, model_features, model_info
        else:
            return None, None, None, None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None


def predict_with_model(model, district_mapping, model_features, model_info, input_params):
    """Realiza predicción usando el modelo Random Forest"""
    try:
        # Mapear amenidades a las features booleanas del modelo
        amenity_mapping = {
            '🌿 Terrace': 'HASTERRACE',
            '🏗️ Lift': 'HASLIFT', 
            '❄️ Air Conditioning': 'HASAIRCONDITIONING',
            '🌺 Garden': 'HASGARDEN',
            '🚗 Parking Space': 'HASPARKINGSPACE',
            '📦 Storage Room': 'HASBOXROOM',
            '👔 Built-in Wardrobe': 'HASWARDROBE',
            '🛡️ Doorman': 'HASDOORMAN',
            '🏊 Swimming Pool': 'HASSWIMMINGPOOL'
        }
        
        # Crear diccionario con valores por defecto
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
            'DISTANCE_TO_CITY_CENTER': 5.0,  # Valor promedio en km
            'DISTANCE_TO_METRO': 0.5,  # Valor promedio en km
            'DISTANCE_TO_CASTELLANA': 3.0,  # Valor promedio en km
            'CADCONSTRUCTIONYEAR': 1980,  # Año promedio
            'CADMAXBUILDINGFLOOR': 5,  # Plantas promedio
            'CADDWELLINGCOUNT': 20,  # Viviendas promedio por edificio
            'BUILTTYPEID_2': 1,  # Tipo de edificio más común
        }
        
        # Mapear distrito seleccionado a DISTRICT_CODE
        selected_district = input_params.get('district', 'Centro')
        if selected_district in district_mapping:
            model_input['DISTRICT_CODE'] = district_mapping[selected_district]
        else:
            # Valor por defecto si no encontramos el distrito
            model_input['DISTRICT_CODE'] = 1  # Código del Centro por defecto
            st.warning(f"Distrito '{selected_district}' no encontrado en el mapping. Usando Centro como valor por defecto.")
        
        # Activar amenidades seleccionadas
        for amenity in input_params.get('amenities', []):
            if amenity in amenity_mapping:
                model_input[amenity_mapping[amenity]] = 1
        
        # Crear DataFrame con la entrada
        df_input = pd.DataFrame([model_input])
        
        # Asegurar que las columnas estén en el orden correcto según model_features
        df_input = df_input.reindex(columns=model_features, fill_value=0)
        
        # Realizar predicción
        prediction = model.predict(df_input)[0]
        
        return max(50000, int(prediction))  # Mínimo de 50k€
        
    except Exception as e:
        st.error(f"Error in prediction: {e}")
        return None

# Configuración general
st.set_page_config(page_title="Madrid Housing Dashboard", layout="wide", page_icon="🏠")

# --- Estilos personalizados mejorados ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
        height: 100vh;
        margin: 0;
        padding: 0;
    }

    .block-container {
        padding: 2rem 2rem 3rem 2rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

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

    h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0 2rem 0;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(0, 0, 0, 0.3);
        filter: drop-shadow(0 2px 10px rgba(0, 0, 0, 0.3));
    }

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
    
    /* Asegurar que los labels de sliders y multiselect tengan el mismo estilo - TAMAÑO GRANDE */
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
    
    /* Estilos específicos para elementos del sidebar */
    section[data-testid="stSidebar"] .stSlider > div > div > div > div {
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect > div > div > div {
        color: #1a202c !important;
        font-weight: 600 !important;
    }
    
    /* Mejorar el contraste de los valores de los sliders */
    section[data-testid="stSidebar"] .stSlider div[data-testid="stSliderThumbValue"] {
        color: #1a202c !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    
    /* Mejorar el contraste del texto en general del sidebar */
    section[data-testid="stSidebar"] .stSlider > div > div {
        color: #1a202c !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect > div > div {
        color: #1a202c !important;
    }
    
    /* Mejorar también las etiquetas de otros elementos del sidebar - TAMAÑO GRANDE */
    section[data-testid="stSidebar"] .stSelectbox label {
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
    
    section[data-testid="stSidebar"] .stCheckbox label {
        color: #2c3e50 !important;
        font-weight: 900 !important;
        font-size: 1.4rem !important;
        margin-bottom: 12px !important;
        display: block !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.15) !important;
        letter-spacing: 0.4px !important;
        line-height: 1.3 !important;
        text-transform: capitalize !important;
    }
    
    /* Asegurar que todos los labels tengan buen tamaño - VERSIÓN MUY GRANDE */
    section[data-testid="stSidebar"] label {
        color: #2c3e50 !important;
        font-weight: 900 !important;
        font-size: 1.5rem !important;
        margin-bottom: 12px !important;
        line-height: 1.3 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.15) !important;
        letter-spacing: 0.5px !important;
        display: block !important;
        text-transform: capitalize !important;
    }
    
    /* Mejorar la apariencia de los controles de entrada */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Asegurar que el texto de los valores seleccionados sea visible */
    section[data-testid="stSidebar"] .stSelectbox span,
    section[data-testid="stSidebar"] .stMultiSelect span {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* FORZAR TAMAÑOS DE LABELS - REGLAS MÁS ESPECÍFICAS */
    section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] > label,
    section[data-testid="stSidebar"] div[data-testid="stSlider"] > label,
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > label {
        color: #2c3e50 !important;
        font-weight: 900 !important;
        font-size: 1.5rem !important;
        margin-bottom: 12px !important;
        line-height: 1.3 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.15) !important;
        letter-spacing: 0.5px !important;
        display: block !important;
        text-transform: capitalize !important;
    }
    
    /* Sobrescribir cualquier inline style de Streamlit */
    section[data-testid="stSidebar"] label[style] {
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        color: #2c3e50 !important;
    }
    
    /* Botón del sidebar mejorado */
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
    
    /* Eliminar cualquier estilo rojo del botón primary */
    section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        border-color: transparent !important;
    }
    
    section[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(45deg, #764ba2, #667eea) !important;
        border-color: transparent !important;
    }

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
    
    /* Estilos para el título del expander */
    .stExpander summary {
        color: white !important;
        font-weight: 600 !important;
    }
    
    .stExpander > div > div > div > summary {
        color: white !important;
        font-weight: 600 !important;
    }
    
    .stExpander > div > div > div > summary > span {
        color: white !important;
    }

    .stMarkdown {
        color: white;
    }

    /* Estilos para métricas */
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

    /* Estilos para el mapa - Eliminar elementos visuales no deseados */
    .folium-map .leaflet-popup-pane {
        display: none !important;
    }
    
    .folium-map .leaflet-popup {
        display: none !important;
    }
    
    .folium-map .leaflet-popup-content {
        display: none !important;
    }
    
    .folium-map .leaflet-popup-content-wrapper {
        display: none !important;
    }
    
    .folium-map .leaflet-popup-tip {
        display: none !important;
    }
    
    /* Ocultar cualquier overlay que pueda aparecer al hacer clic */
    .folium-map .leaflet-overlay-pane .leaflet-clickable {
        pointer-events: auto;
    }
    
    /* Asegurar que solo se muestre el tooltip */
    .folium-map .leaflet-tooltip {
        display: block !important;
        pointer-events: none !important;
    }

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

    /* Animaciones suaves */
    .stSlider, .stMultiSelect, .stButton, .stExpander {
        transition: all 0.3s ease;
    }

    .stSlider:hover, .stMultiSelect:hover {
        transform: translateY(-1px);
    }
    
    /* Estilo para el mapa */
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
    
    /* Ajustar el mapa para que ocupe todo el espacio */
    .stApp > div > div > div > div > div:has(iframe) {
        width: 100% !important;
        height: 100% !important;
    }
    
    iframe[title="streamlit_folium.st_folium"] {
        width: 100% !important;
        height: 600px !important;
        border-radius: 15px;
    }
    
    /* Tarjetas de información */
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
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        display: block;
        text-align: center;
    }
    
    /* Gradientes para los iconos */
    .price-gradient {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Sidebar styling */
    .stSidebar > div:first-child {
        background: transparent;
    }
    
    /* Mejorar contraste en inputs del sidebar */
    section[data-testid="stSidebar"] .stSlider > div > div > div > div > div {
        background-color: transparent !important;
        color: #2c3e50 !important;
    }
    
    section[data-testid="stSidebar"] .stSlider > div > div > div > div {
        background-color: rgba(44, 62, 80, 0.1) !important;
        border-radius: 8px !important;
    }
    /* Estilos para el multiselect del sidebar */
    section[data-testid="stSidebar"] .stMultiSelect > div > div > div > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #2c3e50 !important;
    }
    
    /* Estilos para los tags/chips seleccionados en multiselect */
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
    
    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] span {
        color: white !important;
    }
    
    /* Botón X para eliminar el tag */
    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] button {
        color: rgba(255, 255, 255, 0.8) !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-left: 4px !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="tag"] button:hover {
        color: white !important;
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 50% !important;
    }
    
    section[data-testid="stSidebar"] .stAlert {
        background: rgba(40, 167, 69, 0.15) !important;
        border: 1px solid rgba(40, 167, 69, 0.3) !important;
        color: #155724 !important;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# --- Título del Dashboard con subtítulo ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("Madrid Housing Dashboard")
    st.markdown("""
    <div style='text-align: center; color: rgba(255, 255, 255, 0.8); font-size: 1.2rem; margin-bottom: 2rem;'>
        Discover the perfect property in Madrid with AI-powered price predictions
    </div>
    """, unsafe_allow_html=True)

# --- Verificar estado del modelo ---
model_status = "🤖 AI Model Ready" if (SKLEARN_AVAILABLE and os.path.exists('random_forest_model.pkl')) else "📊 Formula Mode"
model_color = "#28a745" if (SKLEARN_AVAILABLE and os.path.exists('random_forest_model.pkl')) else "#ffc107"

st.markdown(f"""
<div style='text-align: center; margin-bottom: 1rem;'>
    <span style='background: rgba(255, 255, 255, 0.15); color: {model_color}; padding: 8px 16px; border-radius: 20px; font-weight: 600; font-size: 0.9rem; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);'>
        {model_status}
    </span>
</div>
""", unsafe_allow_html=True)

# --- Filtros en barra lateral con mejor diseño ---
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 2rem; padding: 1rem 0; border-bottom: 2px solid rgba(102, 126, 234, 0.2);'>
    <h1 style='color: #2c3e50; font-size: 1.8rem; margin-bottom: 0.8rem; font-weight: 800; text-align: center; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);'>Filter Properties</h1>
    <p style='color: #34495e; font-size: 1rem; font-weight: 500; text-align: center; margin: 0;'>Customize your search criteria</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='margin: 30px 0 20px 0; padding: 0 0 15px 0; border-bottom: 2px solid rgba(102, 126, 234, 0.4);'>
    <h3 style='color: #2c3e50; font-weight: 700; margin: 0; font-size: 1.15rem; display: flex; align-items: center; text-transform: capitalize;'>
        <span style='background: linear-gradient(45deg, #667eea, #764ba2); width: 4px; height: 20px; border-radius: 2px; margin-right: 12px; display: block;'></span>
        Property Specifications
    </h3>
</div>
""", unsafe_allow_html=True)
rooms = st.sidebar.slider("🛏️ Number of Rooms", min_value=1, max_value=7, value=3, help="Select the number of bedrooms")
bathrooms = st.sidebar.slider("🚿 Number of Bathrooms", min_value=1, max_value=4, value=2, help="Select the number of bathrooms")
area = st.sidebar.slider("📐 Constructed Area (m²)", min_value=30, max_value=300, value=80, help="Select the total area of the property")

# --- Cargar datos GeoJSON y obtener distrito seleccionado ---
try:
    gdf_districts = gpd.read_file("madrid-districts.geojson")
    gdf_districts = gdf_districts.to_crs(epsg=4326)  # Asegurar formato lat/lon
except FileNotFoundError:
    st.error("❌ GeoJSON file not found. Please ensure 'madrid-districts.geojson' is in the working directory.")
    st.stop()

# --- Inicializar distrito seleccionado desde session_state ---
selected_district = st.session_state.get("last_selected_district", None)

# --- Crear el mapa ---
madrid_center = [40.4168, -3.7038]
m = folium.Map(
    location=madrid_center, 
    zoom_start=12, 
    tiles="CartoDB positron",
    # Desactivar controles que pueden generar elementos visuales no deseados
    control_scale=False,
    prefer_canvas=True
)

# --- Añadir polígonos de distritos con eventos ---
for idx, row in gdf_districts.iterrows():
    district_name = row["name"]
    
    # Determinar si este distrito está seleccionado
    is_selected = (selected_district == district_name)
    
    # Colores según el estado de selección
    if is_selected:
        # Distrito seleccionado: color verde atractivo
        fill_color = "#28a745"  # Verde bonito
        border_color = "#ffffff"
        fill_opacity = 0.8
        border_weight = 4
    else:
        # Distrito no seleccionado: colores normales
        fill_color = "#667eea"
        border_color = "white"
        fill_opacity = 0.4
        border_weight = 2
    
    # Crear el polígono con configuración mejorada para capturar clics
    geojson_layer = folium.GeoJson(
        data=row["geometry"],
        style_function=lambda feature, name=district_name, selected=is_selected: {
            'fillColor': "#28a745" if selected else "#667eea",
            'color': '#ffffff' if selected else 'white',
            'weight': 4 if selected else 2,
            'fillOpacity': 0.8 if selected else 0.4,
        },
        highlight_function=lambda feature: {
            'fillColor': "#764ba2",
            'color': '#ffffff',
            'weight': 3,
            'fillOpacity': 0.7,
        },
        # Agregar tooltip con el nombre del distrito (aparece al hacer hover)
        tooltip=folium.Tooltip(
            text=f"{'✓ ' if is_selected else ''}{district_name}",
            permanent=False,
            sticky=True,
            style=f"""
                background: linear-gradient(135deg, {'rgba(40, 167, 69, 0.95)' if is_selected else 'rgba(255, 255, 255, 0.95)'} 0%, {'rgba(34, 139, 34, 0.98)' if is_selected else 'rgba(248, 250, 252, 0.98)'} 100%);
                border: 1px solid {'rgba(255, 255, 255, 0.6)' if is_selected else 'rgba(102, 126, 234, 0.3)'};
                border-radius: 8px;
                color: {'white' if is_selected else '#2c3e50'};
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-weight: 600;
                font-size: 13px;
                padding: 8px 14px;
                box-shadow: 0 8px 25px {'rgba(40, 167, 69, 0.4)' if is_selected else 'rgba(102, 126, 234, 0.2)'}, 0 3px 10px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(20px);
                text-align: center;
                white-space: nowrap;
                letter-spacing: 0.3px;
                opacity: 0.96;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                transform: translateY(-2px);
            """
        )
        # No popup para evitar recuadros molestos al hacer clic
    )
    
    # Añadir el polígono al mapa
    geojson_layer.add_to(m)

# --- Mostrar mapa e interactuar ---
st.markdown("""
<div class='map-container'>
    <h2 style='color: white; text-align: center; margin-bottom: 20px;'>🗺️ Select District by Clicking on the Map</h2>
</div>
""", unsafe_allow_html=True)

map_data = st_folium(
    m, 
    width="100%", 
    height=600, 
    returned_objects=["last_object_clicked_tooltip", "last_object_clicked"],
    key="madrid_map",
    # Desactivar funcionalidades que pueden causar elementos visuales no deseados
    feature_group_to_add=None,
    zoom=None,
    # Configuraciones adicionales para evitar popups
    use_container_width=True
)

# Añadir CSS adicional para eliminar completamente cualquier popup o elemento visual no deseado
st.markdown("""
<style>
/* Eliminar popups y overlays completamente */
.leaflet-popup-pane {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

.leaflet-popup {
    display: none !important;
    visibility: hidden !important;
}

.leaflet-popup-content-wrapper,
.leaflet-popup-tip {
    display: none !important;
    visibility: hidden !important;
}

/* Eliminar overlays de selección molestos */
.leaflet-overlay-pane .leaflet-interactive:focus {
    outline: none !important;
    box-shadow: none !important;
}

.leaflet-interactive:active,
.leaflet-interactive:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* Asegurar que no hay bordes negros o elementos visuales molestos */
.leaflet-clickable {
    outline: none !important;
}

.leaflet-container a.leaflet-popup-close-button {
    display: none !important;
}

/* Mejorar la apariencia del tooltip */
.leaflet-tooltip {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.98) 100%) !important;
    border: 1px solid rgba(102, 126, 234, 0.3) !important;
    border-radius: 8px !important;
    color: #2c3e50 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 14px !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2), 0 3px 10px rgba(0, 0, 0, 0.1) !important;
    backdrop-filter: blur(20px) !important;
}

.leaflet-tooltip-top:before {
    border-top-color: rgba(255, 255, 255, 0.95) !important;
}

.leaflet-tooltip-bottom:before {
    border-bottom-color: rgba(255, 255, 255, 0.95) !important;
}

.leaflet-tooltip-left:before {
    border-left-color: rgba(255, 255, 255, 0.95) !important;
}

.leaflet-tooltip-right:before {
    border-right-color: rgba(255, 255, 255, 0.95) !important;
}
</style>
""", unsafe_allow_html=True)

# Añadir JavaScript mejorado para eliminar cualquier popup o elemento visual no deseado
st.markdown("""
<script>
// Función para eliminar popups y elementos visuales no deseados de manera más agresiva
function removeUnwantedMapElements() {
    // Eliminar todos los popups
    const popups = document.querySelectorAll('.leaflet-popup, .leaflet-popup-pane, .leaflet-popup-content-wrapper, .leaflet-popup-tip');
    popups.forEach(popup => {
        popup.style.display = 'none';
        popup.style.visibility = 'hidden';
        popup.style.opacity = '0';
        popup.remove();
    });
    
    // Eliminar contenedores de popup
    const popupPanes = document.querySelectorAll('.leaflet-popup-pane');
    popupPanes.forEach(pane => {
        pane.style.display = 'none';
        pane.innerHTML = '';
    });
    
    // Asegurar que no hay overlays molestos
    const overlays = document.querySelectorAll('.leaflet-overlay-pane .leaflet-interactive');
    overlays.forEach(overlay => {
        overlay.style.outline = 'none';
        overlay.style.boxShadow = 'none';
        // Eliminar cualquier listener de click que pueda generar popups
        overlay.removeEventListener('click', null);
    });
    
    // Eliminar cualquier elemento con recuadros negros
    const interactiveElements = document.querySelectorAll('.leaflet-interactive');
    interactiveElements.forEach(el => {
        el.style.outline = 'none';
        el.style.border = 'none';
        el.style.boxShadow = 'none';
    });
}

// Ejecutar la función inmediatamente
removeUnwantedMapElements();

// Ejecutar la función cada vez que se detecte un cambio en el mapa
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
            removeUnwantedMapElements();
        }
    });
});

const mapContainer = document.querySelector('.folium-map');
if (mapContainer) {
    observer.observe(mapContainer, { 
        childList: true, 
        subtree: true,
        attributes: true,
        attributeOldValue: true 
    });
}

// También ejecutar cuando se hace clic en el mapa o cuando se carga
document.addEventListener('click', function(e) {
    if (e.target.closest('.folium-map')) {
        setTimeout(removeUnwantedMapElements, 10);
        setTimeout(removeUnwantedMapElements, 50);
        setTimeout(removeUnwantedMapElements, 200);
    }
});

// Ejecutar periódicamente para asegurar que no aparezcan elementos no deseados
setInterval(removeUnwantedMapElements, 1000);

// Ejecutar cuando la página esté completamente cargada
window.addEventListener('load', function() {
    setTimeout(removeUnwantedMapElements, 500);
});
</script>
""", unsafe_allow_html=True)

# --- Obtener el distrito seleccionado y actualizar si hay cambios ---
new_selected_district = None
district_changed = False

# Verificar diferentes formas de obtener el distrito seleccionado
if map_data:
    # Método 1: Usando last_object_clicked_tooltip
    if map_data.get("last_object_clicked_tooltip"):
        tooltip_text = map_data["last_object_clicked_tooltip"]
        # Remover el checkmark si existe
        new_district = tooltip_text.replace("✓ ", "") if tooltip_text.startswith("✓ ") else tooltip_text
        if new_district != st.session_state.get("last_selected_district"):
            new_selected_district = new_district
            district_changed = True
    
    # Método 2: Usando coordenadas del clic para encontrar el distrito
    elif map_data.get("last_object_clicked") and isinstance(map_data["last_object_clicked"], dict):
        clicked_coords = map_data["last_object_clicked"]
        if "lat" in clicked_coords and "lng" in clicked_coords and SHAPELY_AVAILABLE:
            lat = clicked_coords["lat"]
            lng = clicked_coords["lng"]
            
            # Crear un punto con las coordenadas del clic
            clicked_point = Point(lng, lat)  # Nota: shapely usa (lng, lat)
            
            # Buscar en qué distrito está el punto
            for _, district_row in gdf_districts.iterrows():
                try:
                    if district_row["geometry"].contains(clicked_point):
                        new_district = district_row["name"]
                        if new_district != st.session_state.get("last_selected_district"):
                            new_selected_district = new_district
                            district_changed = True
                        break
                except Exception:
                    continue
    
    # Método 3: Otros métodos de fallback
    elif map_data.get("last_clicked") and map_data["last_clicked"].get("tooltip"):
        tooltip_text = map_data["last_clicked"]["tooltip"]
        new_district = tooltip_text.replace("✓ ", "") if tooltip_text.startswith("✓ ") else tooltip_text
        if new_district != st.session_state.get("last_selected_district"):
            new_selected_district = new_district
            district_changed = True
    
    elif map_data.get("objects_clicked") and len(map_data["objects_clicked"]) > 0:
        last_clicked = map_data["objects_clicked"][-1]
        if "tooltip" in last_clicked:
            tooltip_text = last_clicked["tooltip"]
            new_district = tooltip_text.replace("✓ ", "") if tooltip_text.startswith("✓ ") else tooltip_text
            if new_district != st.session_state.get("last_selected_district"):
                new_selected_district = new_district
                district_changed = True

# Actualizar el distrito seleccionado
if new_selected_district:
    selected_district = new_selected_district
    st.session_state["last_selected_district"] = selected_district
elif "last_selected_district" in st.session_state:
    selected_district = st.session_state["last_selected_district"]
    
# Si el distrito cambió, forzar recarga para actualizar la interfaz y el mapa
if district_changed:
    st.rerun()

# --- Sección de amenidades en sidebar ---
st.sidebar.markdown("""
<div style='margin: 30px 0 20px 0; padding: 0 0 15px 0; border-bottom: 2px solid rgba(102, 126, 234, 0.4);'>
    <h3 style='color: #2c3e50; font-weight: 700; margin: 0; font-size: 1.6rem !important; display: flex; align-items: center; text-transform: capitalize;'>
        <span style='background: linear-gradient(45deg, #667eea, #764ba2); width: 4px; height: 20px; border-radius: 2px; margin-right: 12px; display: block;'></span>
        Select Amenities
    </h3>
</div>
""", unsafe_allow_html=True)
amenities_options = [
    "🏗️ Lift", "❄️ Air Conditioning", "🚗 Parking Space", "👔 Built-in Wardrobe",
    "📦 Storage Room", "🌿 Terrace", "🏊 Swimming Pool", "🛡️ Doorman", "🌺 Garden"
]
selected_amenities = st.sidebar.multiselect("✨ Property Amenities", options=amenities_options, help="Select all desired amenities for your property")

# --- Mostrar distrito seleccionado en sidebar (al final) ---
st.sidebar.markdown("""
<div style='margin: 30px 0 20px 0; padding: 0 0 15px 0; border-bottom: 2px solid rgba(102, 126, 234, 0.4);'>
    <h3 style='color: #2c3e50; font-weight: 700; margin: 0; font-size: 1.15rem; display: flex; align-items: center; text-transform: capitalize;'>
        <span style='background: linear-gradient(45deg, #667eea, #764ba2); width: 4px; height: 20px; border-radius: 2px; margin-right: 12px; display: block;'></span>
        Selected District
    </h3>
</div>
""", unsafe_allow_html=True)
if selected_district:
    st.sidebar.markdown(f"""
    <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 15px; border-radius: 12px; text-align: center; margin: 10px 0; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'>
        <h4 style='color: white; margin: 0; font-size: 1.1rem; font-weight: 600;'>{selected_district}</h4>
        <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 0.9rem;'>District selected</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"""
    <div style='background: rgba(108, 117, 125, 0.3); padding: 15px; border-radius: 12px; text-align: center; margin: 10px 0; border: 2px dashed rgba(108, 117, 125, 0.5);'>
        <h4 style='color: #6c757d; margin: 0; font-size: 1.1rem; font-weight: 600;'>No District Selected</h4>
        <p style='color: rgba(108, 117, 125, 0.8); margin: 5px 0 0 0; font-size: 0.9rem;'>Click on the map to select</p>
    </div>
    """, unsafe_allow_html=True)

# --- Botón de estimación ---
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)  # Espacio adicional antes del botón
if st.sidebar.button("🔮 Estimate Price", 
                     use_container_width=True, 
                     help="Generate AI-powered price prediction based on your selections"):
    
    # Preparar datos para el modelo
    input_params = {
        'area': area,
        'rooms': rooms,
        'bathrooms': bathrooms,
        'amenities': selected_amenities,
        'district': selected_district
    }
    
    # Intentar cargar y usar el modelo Random Forest
    with st.spinner("Loading AI model..."):
        model, district_mapping, model_features, model_info = load_trained_model()
    
    if model is not None and district_mapping is not None and model_features is not None:
        # Mostrar información del modelo cargado
        if model_info:
            st.sidebar.info(f"🤖 **Random Forest Model Loaded**\n"
                          f"📊 Features: {len(model_features)}\n"
                          f"🏘️ Districts: {len(district_mapping)}\n"
                          f"📈 R²: {model_info.get('performance', {}).get('r2', 'N/A'):.3f}")
        
        # Usar el modelo Random Forest entrenado
        with st.spinner("Predicting with Random Forest..."):
            estimated_price = predict_with_model(model, district_mapping, model_features, model_info, input_params)
        
        if estimated_price is not None:
            # Guardar en session state
            st.session_state.estimated_price = estimated_price
            st.session_state.prediction_method = "Random Forest ML Model"
            st.session_state.price_breakdown = {
                'base_prediction': estimated_price,
                'model_used': 'Random Forest',
                'features_used': len(model_features),
                'district': selected_district or 'Not specified',
                'confidence': 'High (ML Model)',
                'model_performance': f"R²: {model_info.get('performance', {}).get('r2', 'N/A'):.3f}"
            }
            
            st.sidebar.success(f"🤖 ML Prediction: €{estimated_price:,}")
        else:
            # Error en la predicción
            st.session_state.estimated_price = None
            st.session_state.prediction_method = "Error"
            st.session_state.price_breakdown = None
            st.sidebar.error("❌ Error making prediction with the model")
    else:
        # Modelo no disponible
        st.session_state.estimated_price = None
        st.session_state.prediction_method = "Model not available"
        st.session_state.price_breakdown = None
        st.sidebar.error("❌ Random Forest model not available. Please train and save the model first.")
        st.sidebar.info("� Run the Random_Forest.ipynb notebook to train and save the model.")
    
    st.rerun()

# --- Mostrar filtros activos ---
with st.expander("🔎 Selected Filters Summary", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"- **Rooms**: {rooms}")
        st.markdown(f"- **Bathrooms**: {bathrooms}")
        st.markdown(f"- **Area**: {area} m²")
    with col2:
        # Mostrar amenidades directamente
        if selected_amenities:
            amenities_names = [a.split(' ', 1)[1] for a in selected_amenities]  # Eliminar el emoji
            amenities_text = ', '.join(amenities_names)
            st.markdown(f"- **Amenities**: {amenities_text}")
        else:
            st.markdown(f"- **Amenities**: None selected")
        
        # Mostrar distrito sincronizado con el mapa
        district_display = selected_district if selected_district else "Click on map to select"
        st.markdown(f"- **Selected District**: {district_display}")
        
        # Indicador visual si hay distrito seleccionado
        if selected_district:
            st.markdown(f"<span style='color: #28a745; font-weight: bold;'>✓ {selected_district} district active</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color: #ffc107; font-weight: bold;'>⚠ No district selected</span>", unsafe_allow_html=True)

# --- Mostrar precio estimado de forma prominente ---
if 'estimated_price' in st.session_state and st.session_state.estimated_price is not None:
    st.markdown("### 🎯 AI Property Price Prediction")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; 
                    border-radius: 20px; 
                    text-align: center; 
                    margin: 1.5rem 0; 
                    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4), 0 5px 15px rgba(0, 0, 0, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(20px);'>
            <h2 style='color: white; margin: 0 0 0.5rem 0; font-size: 3rem; font-weight: 800; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);'>€{st.session_state.estimated_price:,}</h2>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.3rem; font-weight: 600;'>estimated property value</p>
            <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.3);'>
                <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 1rem;'>🤖 AI Random Forest Model</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
elif 'prediction_method' in st.session_state:
    # Solo mostrar errores si ya se intentó hacer una predicción
    prediction_method = st.session_state.get("prediction_method", "Unknown")
    
    if prediction_method == "Model not available":
        st.markdown("### ❌ Model Not Available")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                        padding: 2rem; 
                        border-radius: 20px; 
                        text-align: center; 
                        margin: 1.5rem 0; 
                        box-shadow: 0 15px 35px rgba(220, 53, 69, 0.4), 0 5px 15px rgba(0, 0, 0, 0.1);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        backdrop-filter: blur(20px);'>
                <h2 style='color: white; margin: 0 0 0.5rem 0; font-size: 2rem; font-weight: 800; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);'>🤖 Model Required</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.1rem; font-weight: 600;'>Random Forest model not found</p>
                <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.3);'>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;'>Please run Random_Forest.ipynb to train and save the model</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    elif prediction_method == "Error":
        st.markdown("### ❌ Prediction Error")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%); 
                        padding: 2rem; 
                        border-radius: 20px; 
                        text-align: center; 
                        margin: 1.5rem 0; 
                        box-shadow: 0 15px 35px rgba(255, 193, 7, 0.4), 0 5px 15px rgba(0, 0, 0, 0.1);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        backdrop-filter: blur(20px);'>
                <h2 style='color: white; margin: 0 0 0.5rem 0; font-size: 2rem; font-weight: 800; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);'>⚠️ Prediction Error</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.1rem; font-weight: 600;'>Unable to generate prediction</p>
                <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.3);'>
                    <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;'>Please check model configuration</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    # Mensaje de bienvenida inicial - no se ha intentado hacer ninguna predicción todavía
    st.markdown("### 🏠 Welcome to Madrid Property Price Predictor")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%); 
                    padding: 2rem; 
                    border-radius: 20px; 
                    text-align: center; 
                    margin: 1.5rem 0; 
                    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(20px);'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🏡</div>
            <h2 style='color: white; margin: 0 0 1rem 0; font-size: 1.8rem; font-weight: 700; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);'>Get AI-Powered Price Predictions</h2>
            <p style='color: rgba(255,255,255,0.8); margin: 0 0 1.5rem 0; font-size: 1.1rem; line-height: 1.5;'>
                Configure your property preferences in the sidebar and click <strong>"🔮 Estimate Price"</strong> to get an intelligent prediction powered by our trained Random Forest model.
            </p>
            <div style='margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.2);'>
                <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.95rem;'>
                    ✨ Select district on map • 🏠 Configure property details • 🔮 Get instant predictions
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    # Mostrar breakdown del precio en el área principal
    if 'price_breakdown' in st.session_state and st.session_state.price_breakdown is not None:
        breakdown = st.session_state.price_breakdown
        prediction_method = st.session_state.get("prediction_method", "Unknown")
        
        if prediction_method.startswith("Random Forest"):
            # Breakdown para modelo ML únicamente
            st.markdown("#### 🤖 AI Model Prediction Details")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.2);'>
                    <h5 style='color: white; margin-bottom: 1rem;'>🧠 Model Information</h5>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Algorithm:</strong> {breakdown.get('model_used', 'Random Forest')}</p>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Features Used:</strong> {breakdown.get('features_used', 'Multiple')}</p>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Confidence:</strong> {breakdown.get('confidence', 'High')}</p>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Performance:</strong> {breakdown.get('model_performance', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.2);'>
                    <h5 style='color: white; margin-bottom: 1rem;'>📍 Input Parameters</h5>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>District:</strong> {breakdown.get('district', 'Not specified')}</p>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Prediction:</strong> €{breakdown.get('base_prediction', 0):,}</p>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Based on:</strong> ML Training Data</p>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Data Source:</strong> Madrid Real Estate</p>
                </div>
                """, unsafe_allow_html=True)
    elif 'prediction_method' in st.session_state and st.session_state.get("prediction_method") == "Model not available":
        # Solo mostrar instrucciones si se intentó hacer una predicción pero el modelo no está disponible
        st.markdown("#### 📋 How to Set Up the Model")
        st.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.2);'>
            <h5 style='color: white; margin-bottom: 1rem;'>🔧 Setup Instructions</h5>
            <ol style='color: rgba(255,255,255,0.9); margin: 0;'>
                <li>Open the <strong>Random_Forest.ipynb</strong> notebook</li>
                <li>Execute all cells to train the Random Forest model</li>
                <li>The model will be automatically saved for the dashboard</li>
                <li>Refresh this page to use the trained model</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# --- Sección de estadísticas del mercado ---
if os.path.exists('data_clean.csv'):
    st.markdown("---")
    st.markdown("### 📈 Madrid Real Estate Market Insights")
    
    try:
        # Cargar datos limpios
        df = pd.read_csv('data_clean.csv')
        
        # Estadísticas generales del mercado
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_price = df['PRICE'].mean()
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-value'>€{avg_price:,.0f}</div>
                <div class='metric-label'>Average Price</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_area = df['CONSTRUCTEDAREA'].mean()
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-value'>{avg_area:.0f}m²</div>
                <div class='metric-label'>Average Area</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_price_per_m2 = (df['PRICE'] / df['CONSTRUCTEDAREA']).mean()
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-value'>€{avg_price_per_m2:.0f}/m²</div>
                <div class='metric-label'>Price per m²</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Análisis por distritos
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Most Expensive Districts")
            
            # Si existe la columna DISTRICT, usarla; si no, usar DISTRICT_CODE
            district_col = 'DISTRICT' if 'DISTRICT' in df.columns else 'DISTRICT_CODE'
            
            if district_col in df.columns:
                # Top 5 distritos más caros
                district_prices = df.groupby(district_col)['PRICE'].mean().sort_values(ascending=False).head(5)
                
                for i, (district, price) in enumerate(district_prices.items(), 1):
                    # Si es código de distrito, intentar mapear al nombre
                    display_name = district
                    if district_col == 'DISTRICT_CODE' and os.path.exists('district_mapping.pkl'):
                        try:
                            with open('district_mapping.pkl', 'rb') as f:
                                district_mapping = pickle.load(f)
                            # Buscar el nombre por código
                            for name, code in district_mapping.items():
                                if code == district:
                                    display_name = name
                                    break
                        except:
                            pass
                    
                    st.markdown(f"""
                    <div style='display: flex; justify-content: space-between; align-items: center; 
                                padding: 16px 20px; margin: 8px 0; 
                                background: rgba(255,255,255,0.05); 
                                border-radius: 8px; 
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                        <div style='display: flex; align-items: center; gap: 16px;'>
                            <span style='font-weight: bold; font-size: 1.1em; min-width: 20px;'>{i}</span>
                            <span style='font-weight: 600; font-size: 1.05em;'>{display_name}</span>
                        </div>
                        <span style='font-weight: bold; font-size: 1.2em;'>€{price:,.0f}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("*District data not available*")
        
        with col2:
            st.markdown("#### Property Size Distribution")
            
            # Distribución por tamaño
            small_props = len(df[df['CONSTRUCTEDAREA'] < 60])
            medium_props = len(df[(df['CONSTRUCTEDAREA'] >= 60) & (df['CONSTRUCTEDAREA'] < 120)])
            large_props = len(df[df['CONSTRUCTEDAREA'] >= 120])
            
            total_props = len(df)
            
            # Crear barras visuales simples
            st.markdown(f"""
            <div style='margin: 10px 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin: 8px 0;'>
                    <span><strong>Small (&lt;60m²)</strong></span>
                    <span style='color: #ff6b6b;'>{small_props:,} ({small_props/total_props*100:.1f}%)</span>
                </div>
                <div style='background: rgba(255,107,107,0.2); height: 8px; border-radius: 4px;'>
                    <div style='background: #ff6b6b; height: 100%; width: {small_props/total_props*100:.1f}%; border-radius: 4px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='margin: 10px 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin: 8px 0;'>
                    <span><strong>Medium (60-120m²)</strong></span>
                    <span style='color: #4ecdc4;'>{medium_props:,} ({medium_props/total_props*100:.1f}%)</span>
                </div>
                <div style='background: rgba(78,205,196,0.2); height: 8px; border-radius: 4px;'>
                    <div style='background: #4ecdc4; height: 100%; width: {medium_props/total_props*100:.1f}%; border-radius: 4px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='margin: 10px 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin: 8px 0;'>
                    <span><strong>Large (&gt;120m²)</strong></span>
                    <span style='color: #45b7d1;'>{large_props:,} ({large_props/total_props*100:.1f}%)</span>
                </div>
                <div style='background: rgba(69,183,209,0.2); height: 8px; border-radius: 4px;'>
                    <div style='background: #45b7d1; height: 100%; width: {large_props/total_props*100:.1f}%; border-radius: 4px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Información adicional
            st.markdown("<br>", unsafe_allow_html=True)
            avg_rooms = df['ROOMNUMBER'].mean() if 'ROOMNUMBER' in df.columns else 0
            avg_bathrooms = df['BATHNUMBER'].mean() if 'BATHNUMBER' in df.columns else 0
            
            if avg_rooms > 0 or avg_bathrooms > 0:
                st.markdown("#### Property Features")
                
                if avg_rooms > 0:
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin: 8px 0;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <span style='font-weight: 500;'>Average Rooms</span>
                            <span style='font-size: 1.3em; font-weight: bold;'>{avg_rooms:.1f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if avg_bathrooms > 0:
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin: 8px 0;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <span style='font-weight: 500;'>Average Bathrooms</span>
                            <span style='font-size: 1.3em; font-weight: bold;'>{avg_bathrooms:.1f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Amenidades más comunes
        amenity_columns = ['HASTERRACE', 'HASLIFT', 'HASAIRCONDITIONING', 'HASGARDEN', 
                          'HASPARKINGSPACE', 'HASBOXROOM', 'HASWARDROBE', 'HASDOORMAN', 'HASSWIMMINGPOOL']
        
        available_amenities = [col for col in amenity_columns if col in df.columns]
        
        if available_amenities:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("Property Amenities Overview", expanded=False):
                
                amenity_names = {
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
                
                # Calcular porcentajes de amenidades
                amenity_stats = []
                for col in available_amenities:
                    if col in df.columns:
                        percentage = (df[col].sum() / len(df)) * 100
                        name = amenity_names.get(col, col.replace('HAS', '').title())
                        amenity_stats.append((name, percentage))
                
                # Ordenar por porcentaje descendente
                amenity_stats.sort(key=lambda x: x[1], reverse=True)
                
                # Mostrar todas las amenidades con barras de progreso
                for name, percentage in amenity_stats:
                    st.markdown(f"""
                    <div style='margin: 8px 0;'>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;'>
                            <span style='font-weight: 500;'>{name}</span>
                            <span style='color: #a29bfe; font-weight: bold;'>{percentage:.1f}%</span>
                        </div>
                        <div style='background: rgba(255,255,255,0.1); height: 6px; border-radius: 3px;'>
                            <div style='background: #a29bfe; height: 100%; width: {percentage:.1f}%; border-radius: 3px;'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading market data: {e}")

# --- Sección de información del modelo ---
if SKLEARN_AVAILABLE and os.path.exists('random_forest_model.pkl'):
    st.markdown("---")
    st.markdown("### 📊 Model Information & Performance")
    
    # Cargar información del modelo para mostrar métricas
    try:
        model, district_mapping, model_features, model_info = load_trained_model()
        
        if model_info and model_features and district_mapping:
            # Métricas principales del modelo
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                r2_score = model_info.get('performance', {}).get('r2', 0)
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-value'>{r2_score:.3f}</div>
                    <div class='metric-label'>R² Score</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                mae = model_info.get('performance', {}).get('mae', 0)
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-value'>€{mae:,.0f}</div>
                    <div class='metric-label'>Mean Absolute Error</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-value'>{len(model_features)}</div>
                    <div class='metric-label'>Features Used</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-value'>{len(district_mapping)}</div>
                    <div class='metric-label'>Districts Covered</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Top features utilizadas (si están disponibles)
            if 'feature_importance' in model_info and model_info['feature_importance']:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("🔍 Top Important Features", expanded=False):
                    feature_importance = model_info['feature_importance']
                    
                    # Crear dos columnas para mostrar las features
                    col1, col2 = st.columns(2)
                    
                    # Dividir las features en dos listas
                    mid_point = len(feature_importance) // 2
                    first_half = list(feature_importance.items())[:mid_point]
                    second_half = list(feature_importance.items())[mid_point:]
                    
                    with col1:
                        for feature, importance in first_half:
                            # Traducir nombres técnicos a nombres más amigables
                            feature_name = feature.replace('_', ' ').title()
                            if 'DISTRICT' in feature:
                                feature_name = 'District Location'
                            elif 'CONSTRUCTEDAREA' in feature:
                                feature_name = 'Property Area'
                            elif 'ROOMNUMBER' in feature:
                                feature_name = 'Number of Rooms'
                            elif 'BATHNUMBER' in feature:
                                feature_name = 'Number of Bathrooms'
                            elif 'DISTANCE' in feature:
                                feature_name = feature.replace('DISTANCE_TO_', '').replace('_', ' ').title() + ' Distance'
                            
                            st.markdown(f"**{feature_name}:** {importance:.3f}")
                    
                    with col2:
                        for feature, importance in second_half:
                            # Traducir nombres técnicos a nombres más amigables
                            feature_name = feature.replace('_', ' ').title()
                            if 'DISTRICT' in feature:
                                feature_name = 'District Location'
                            elif 'CONSTRUCTEDAREA' in feature:
                                feature_name = 'Property Area'
                            elif 'ROOMNUMBER' in feature:
                                feature_name = 'Number of Rooms'
                            elif 'BATHNUMBER' in feature:
                                feature_name = 'Number of Bathrooms'
                            elif 'DISTANCE' in feature:
                                feature_name = feature.replace('DISTANCE_TO_', '').replace('_', ' ').title() + ' Distance'
                            
                            st.markdown(f"**{feature_name}:** {importance:.3f}")
                            
    except Exception as e:
        st.error(f"Error loading model information: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.7); margin-top: 2rem;'>
    <p>🏠 Madrid Property Price Prediction Dashboard</p>
    <p>Powered by Random Forest Machine Learning • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
