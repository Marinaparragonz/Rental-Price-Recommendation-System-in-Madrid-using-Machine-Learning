import streamlit as st 
import geopandas as gpd
from streamlit_folium import st_folium
import folium

try:
    from shapely.geometry import Point
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False

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
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: #2c3e50;
    }

    .stMultiSelect > div {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: #2c3e50;
    }
    
    /* Estilos específicos para elementos del sidebar */
    section[data-testid="stSidebar"] .stSlider > div > div > div > div {
        color: #2c3e50 !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect > div > div > div {
        color: #2c3e50 !important;
    }
    
    section[data-testid="stSidebar"] .stSlider label {
        color: #2c3e50 !important;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: #2c3e50 !important;
        font-weight: 600;
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
    
    /* Personalizar colores de los sliders en el sidebar - Versión mejorada */
    
    /* Contenedor principal del slider */
    section[data-testid="stSidebar"] .stSlider > div > div > div > div[data-baseweb="slider"] {
        background: transparent !important;
    }
    
    /* Track del slider (línea de fondo) */
    section[data-testid="stSidebar"] .stSlider > div > div > div > div[data-baseweb="slider"] > div:first-child {
        background: rgba(102, 126, 234, 0.25) !important;
        border-radius: 8px !important;
        height: 6px !important;
    }
    
    /* Track activo del slider (parte llena) */
    section[data-testid="stSidebar"] .stSlider > div > div > div > div[data-baseweb="slider"] > div:nth-child(2) {
        background: linear-gradient(90deg, #4A90E2 0%, #667eea 50%, #764ba2 100%) !important;
        border-radius: 8px !important;
        height: 6px !important;
    }
    
    /* Thumb del slider (la barrita/círculo que se desplaza) */
    section[data-testid="stSidebar"] .stSlider > div > div > div > div[data-baseweb="slider"] > div:last-child {
        background: linear-gradient(135deg, #4A90E2 0%, #667eea 50%, #764ba2 100%) !important;
        border: 3px solid white !important;
        box-shadow: 0 3px 12px rgba(74, 144, 226, 0.4), 0 1px 4px rgba(0, 0, 0, 0.2) !important;
        width: 20px !important;
        height: 20px !important;
        border-radius: 50% !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    
    /* Efecto hover para el thumb */
    section[data-testid="stSidebar"] .stSlider > div > div > div > div[data-baseweb="slider"] > div:last-child:hover {
        background: linear-gradient(135deg, #764ba2 0%, #4A90E2 100%) !important;
        transform: scale(1.15) !important;
        box-shadow: 0 4px 16px rgba(74, 144, 226, 0.6), 0 2px 8px rgba(118, 75, 162, 0.3) !important;
        border: 3px solid #f8f9fa !important;
    }
    
    /* Asegurar que todos los elementos del slider usen los colores correctos */
    section[data-testid="stSidebar"] .stSlider div[role="slider"] div {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] .stSlider div[role="slider"] div div {
        background: linear-gradient(90deg, #4A90E2 0%, #667eea 100%) !important;
    }
    
    /* Sobrescribir cualquier estilo de Streamlit que use rojo */
    section[data-testid="stSidebar"] .stSlider [style*="rgb(255"] {
        background: linear-gradient(135deg, #4A90E2, #667eea) !important;
    }
    
    section[data-testid="stSidebar"] .stSlider [style*="#ff"] {
        background: linear-gradient(135deg, #4A90E2, #667eea) !important;
    }
    
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
    
    /* Footer estilo */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(0, 0, 0, 0.5);
        color: white;
        text-align: center;
        padding: 10px 0;
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
        Discover the perfect rental property in Madrid with AI-powered price predictions
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
    
    # Crear el polígono con configuración mejorada para capturar clics
    geojson_layer = folium.GeoJson(
        data=row["geometry"],
        style_function=lambda feature, name=district_name: {
            'fillColor': "#667eea",
            'color': 'white',
            'weight': 2,
            'fillOpacity': 0.4,
        },
        highlight_function=lambda feature: {
            'fillColor': "#764ba2",
            'color': '#ffffff',
            'weight': 3,
            'fillOpacity': 0.7,
        },
        # Agregar tooltip con el nombre del distrito (aparece al hacer hover)
        tooltip=folium.Tooltip(
            text=district_name,
            permanent=False,
            sticky=True,
            style="""
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.98) 100%);
                border: 1px solid rgba(102, 126, 234, 0.3);
                border-radius: 8px;
                color: #2c3e50;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-weight: 600;
                font-size: 13px;
                padding: 8px 14px;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2), 0 3px 10px rgba(0, 0, 0, 0.1);
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

# --- Obtener el distrito seleccionado ---
selected_district = None
district_changed = False

# Verificar diferentes formas de obtener el distrito seleccionado
if map_data:
    # Método 1: Usando last_object_clicked_tooltip
    if map_data.get("last_object_clicked_tooltip"):
        new_district = map_data["last_object_clicked_tooltip"]
        if new_district != st.session_state.get("last_selected_district"):
            selected_district = new_district
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
                            selected_district = new_district
                            district_changed = True
                        break
                except Exception:
                    continue
    
    # Método 3: Otros métodos de fallback
    elif map_data.get("last_clicked") and map_data["last_clicked"].get("tooltip"):
        new_district = map_data["last_clicked"]["tooltip"]
        if new_district != st.session_state.get("last_selected_district"):
            selected_district = new_district
            district_changed = True
    
    elif map_data.get("objects_clicked") and len(map_data["objects_clicked"]) > 0:
        last_clicked = map_data["objects_clicked"][-1]
        if "tooltip" in last_clicked:
            new_district = last_clicked["tooltip"]
            if new_district != st.session_state.get("last_selected_district"):
                selected_district = new_district
                district_changed = True

# Si no hay nueva selección, mantener la anterior
if not selected_district and "last_selected_district" in st.session_state:
    selected_district = st.session_state["last_selected_district"]

# Guardar la selección actual y forzar actualización si cambió
if selected_district:
    st.session_state["last_selected_district"] = selected_district
    
# Si el distrito cambió, forzar recarga para actualizar la interfaz
if district_changed:
    st.rerun()

# Debug: Mostrar información del mapa para diagnosticar
debug_mode = st.sidebar.checkbox("🔍 Debug Mode", help="Show map interaction data")
if debug_mode:
    st.sidebar.write("Map data keys:", list(map_data.keys()) if map_data else "No map data")
    if map_data:
        st.sidebar.write("Full map data:", map_data)
        st.sidebar.write("Selected district detected:", selected_district)
        st.sidebar.write("Shapely available:", SHAPELY_AVAILABLE)
        
    # Mostrar debug también en la zona principal
    with st.expander("🔍 Map Debug Information", expanded=True):
        st.write("**Map Data Keys:**", list(map_data.keys()) if map_data else "No map data")
        if map_data:
            for key, value in map_data.items():
                st.write(f"**{key}:**", value)
        st.write("**Detected District:**", selected_district or "None")
        st.write("**Shapely Available:**", SHAPELY_AVAILABLE)
        
        # Botón para testear selección manual de distrito
        if map_data and map_data.get("last_object_clicked"):
            coords = map_data["last_object_clicked"]
            st.write("**Clicked Coordinates:**", f"Lat: {coords.get('lat', 'N/A')}, Lng: {coords.get('lng', 'N/A')}")
            
        # Selector manual de distrito para testing
        manual_district = st.selectbox("🔧 Manual District Override (for testing)", 
                                     options=[""] + gdf_districts["name"].tolist())
        if manual_district and st.button("🔧 Set Manual District"):
            st.session_state["last_selected_district"] = manual_district
            selected_district = manual_district
            st.success(f"✅ District set to: {manual_district}")
            st.experimental_rerun()

# --- Sección de amenidades en sidebar ---
st.sidebar.markdown("""
<div style='margin: 30px 0 20px 0; padding: 0 0 15px 0; border-bottom: 2px solid rgba(102, 126, 234, 0.4);'>
    <h3 style='color: #2c3e50; font-weight: 700; margin: 0; font-size: 1.15rem; display: flex; align-items: center; text-transform: capitalize;'>
        <span style='background: linear-gradient(45deg, #667eea, #764ba2); width: 4px; height: 20px; border-radius: 2px; margin-right: 12px; display: block;'></span>
        Select Amenities
    </h3>
</div>
""", unsafe_allow_html=True)
amenities_options = [
    "🏗️ Lift", "❄️ Air Conditioning", "🚗 Parking Space", "👔 Built-in Wardrobe",
    "📦 Storage Room", "🌿 Terrace", "🏊 Swimming Pool", "🛡️ Doorman", "🌺 Garden"
]
selected_amenities = st.sidebar.multiselect("Available Amenities", options=amenities_options, help="Select all desired amenities")

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
    
    # Calcular precio base usando fórmula mejorada
    base_price = 800
    room_multiplier = rooms * 200
    bathroom_multiplier = bathrooms * 150
    area_multiplier = area * 3.5
    amenity_multiplier = len(selected_amenities) * 100
    
    # Boost de distrito si está seleccionado
    district_boost = 0
    if selected_district and selected_district in ["Salamanca", "Chamberí", "Centro"]:
        district_boost = 20  # 20% boost para distritos premium
    elif selected_district and selected_district in ["Retiro", "Chamartín", "Moncloa-Aravaca"]:
        district_boost = 15  # 15% boost para distritos semi-premium
    elif selected_district:
        district_boost = 5   # 5% boost para otros distritos
    
    # Precio total
    estimated_price = int((base_price + room_multiplier + bathroom_multiplier + area_multiplier + amenity_multiplier) * (1 + district_boost/100))
    
    # Guardar en session state
    st.session_state.estimated_price = estimated_price
    st.session_state.price_breakdown = {
        'base_price': base_price,
        'room_price': room_multiplier,
        'bathroom_price': bathroom_multiplier,
        'area_price': int(area_multiplier),
        'amenity_price': amenity_multiplier,
        'district_boost': district_boost
    }
    
    st.sidebar.success(f"✅ Price estimated: €{estimated_price:,}/month")
    st.rerun()

# --- Sistema de Comparación en Sidebar ---
st.sidebar.markdown("""
<div style='margin: 40px 0 20px 0; padding: 0 0 15px 0; border-bottom: 2px solid rgba(102, 126, 234, 0.4);'>
    <h3 style='color: #2c3e50; font-weight: 700; margin: 0; font-size: 1.15rem; display: flex; align-items: center; text-transform: capitalize;'>
        <span style='background: linear-gradient(45deg, #667eea, #764ba2); width: 4px; height: 20px; border-radius: 2px; margin-right: 12px; display: block;'></span>
        Property Comparison
    </h3>
</div>
""", unsafe_allow_html=True)

# Inicializar variables de comparación en session_state
if 'comparison_data' not in st.session_state:
    st.session_state.comparison_data = {}

# Función para calcular precio (fuera del condicional)
def calculate_price_comparison(rooms_val, bathrooms_val, area_val, amenities_val, district_val):
    base_price = 800
    room_multiplier = rooms_val * 200
    bathroom_multiplier = bathrooms_val * 150
    area_multiplier = area_val * 3.5
    amenity_multiplier = len(amenities_val) * 100
    
    district_boost = 0
    if district_val and district_val in ["Salamanca", "Chamberí", "Centro"]:
        district_boost = 20
    elif district_val and district_val in ["Retiro", "Chamartín", "Moncloa-Aravaca"]:
        district_boost = 15
    elif district_val:
        district_boost = 5
    
    estimated_price = int((base_price + room_multiplier + bathroom_multiplier + area_multiplier + amenity_multiplier) * (1 + district_boost/100))
    
    breakdown = {
        'base_price': base_price,
        'room_price': room_multiplier,
        'bathroom_price': bathroom_multiplier,
        'area_price': int(area_multiplier),
        'amenity_price': amenity_multiplier,
        'district_boost': district_boost
    }
    
    return estimated_price, breakdown

# Configuración Property A (siempre disponible)
st.sidebar.markdown("**🏠 Property A Configuration:**")

col1, col2 = st.sidebar.columns(2)
with col1:
    rooms_a = st.slider("Rooms A", min_value=1, max_value=7, value=3, key="rooms_a_sidebar")
    bathrooms_a = st.slider("Bathrooms A", min_value=1, max_value=4, value=2, key="bathrooms_a_sidebar")
with col2:
    area_a = st.slider("Area A (m²)", min_value=30, max_value=300, value=80, key="area_a_sidebar")

districts_list = ["No District"] + gdf_districts["name"].tolist()
district_a = st.sidebar.selectbox("🏘️ District A", options=districts_list, key="district_a_sidebar")
amenities_a = st.sidebar.multiselect("🏗️ Amenities A", options=amenities_options, key="amenities_a_sidebar")

if st.sidebar.button("💡 Calculate Property A", key="calc_a_sidebar"):
    district_a_val = district_a if district_a != "No District" else None
    price_a, breakdown_a = calculate_price_comparison(rooms_a, bathrooms_a, area_a, amenities_a, district_a_val)
    st.session_state.comparison_data['property_a'] = {
        'price': price_a,
        'breakdown': breakdown_a,
        'config': {
            'rooms': rooms_a,
            'bathrooms': bathrooms_a,
            'area': area_a,
            'district': district_a_val or "No District",
            'amenities': amenities_a
        }
    }
    st.sidebar.success(f"✅ Property A: €{price_a:,}/month")

# Separador
st.sidebar.markdown("---")

# Configuración Property B (siempre disponible)
st.sidebar.markdown("**🏡 Property B Configuration:**")

col1, col2 = st.sidebar.columns(2)
with col1:
    rooms_b = st.slider("Rooms B", min_value=1, max_value=7, value=2, key="rooms_b_sidebar")
    bathrooms_b = st.slider("Bathrooms B", min_value=1, max_value=4, value=1, key="bathrooms_b_sidebar")
with col2:
    area_b = st.slider("Area B (m²)", min_value=30, max_value=300, value=60, key="area_b_sidebar")

district_b = st.sidebar.selectbox("🏘️ District B", options=districts_list, key="district_b_sidebar")
amenities_b = st.sidebar.multiselect("🏗️ Amenities B", options=amenities_options, key="amenities_b_sidebar")

if st.sidebar.button("💡 Calculate Property B", key="calc_b_sidebar"):
    district_b_val = district_b if district_b != "No District" else None
    price_b, breakdown_b = calculate_price_comparison(rooms_b, bathrooms_b, area_b, amenities_b, district_b_val)
    st.session_state.comparison_data['property_b'] = {
        'price': price_b,
        'breakdown': breakdown_b,
        'config': {
            'rooms': rooms_b,
            'bathrooms': bathrooms_b,
            'area': area_b,
            'district': district_b_val or "No District",
            'amenities': amenities_b
        }
    }
    st.sidebar.success(f"✅ Property B: €{price_b:,}/month")

# Separador final
st.sidebar.markdown("---")

# Checkbox para activar comparación (después de configurar las propiedades)
enable_comparison = st.sidebar.checkbox("⚖️ Show Property Comparison", 
                                       help="Display comparison between Property A and B in the main dashboard")

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

# --- Mostrar Comparación de Propiedades (solo si está habilitada) ---
if enable_comparison and 'comparison_data' in st.session_state and len(st.session_state.comparison_data) >= 2:
    st.markdown("### ⚖️ Property Comparison Results")
    st.markdown("""
    <div style='color: rgba(255, 255, 255, 0.8); margin-bottom: 1.5rem; text-align: center;'>
        Compare your two property configurations side by side
    </div>
    """, unsafe_allow_html=True)
    
    prop_a = st.session_state.comparison_data['property_a']
    prop_b = st.session_state.comparison_data['property_b']
    
    # Comparison Summary Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center; margin: 1rem 0;
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);'>
            <h4 style='color: white; margin: 0 0 0.5rem 0;'>🏠 Property A</h4>
            <h2 style='color: white; margin: 0; font-size: 2rem;'>€{prop_a['price']:,}</h2>
            <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;'>per month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        price_diff = prop_a['price'] - prop_b['price']
        diff_color = "#28a745" if price_diff < 0 else "#dc3545"
        diff_symbol = "↓" if price_diff < 0 else "↑"
        diff_text = f"€{abs(price_diff):,} {diff_symbol}"
        
        st.markdown(f"""
        <div style='background: rgba(255, 255, 255, 0.15); 
                    padding: 1.5rem; border-radius: 15px; text-align: center; margin: 1rem 0;
                    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);'>
            <h4 style='color: white; margin: 0 0 0.5rem 0;'>💰 Difference</h4>
            <h2 style='color: {diff_color}; margin: 0; font-size: 2rem;'>{diff_text}</h2>
            <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;'>A vs B</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); 
                    padding: 1.5rem; border-radius: 15px; text-align: center; margin: 1rem 0;
                    box-shadow: 0 8px 25px rgba(118, 75, 162, 0.3);'>
            <h4 style='color: white; margin: 0 0 0.5rem 0;'>🏡 Property B</h4>
            <h2 style='color: white; margin: 0; font-size: 2rem;'>€{prop_b['price']:,}</h2>
            <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;'>per month</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Comparison Table
    st.markdown("#### 📋 Detailed Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); 
                    padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                    border: 1px solid rgba(255, 255, 255, 0.2);'>
            <h5 style='color: white; margin-bottom: 1rem;'>🏠 Property A Details</h5>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Rooms:</strong> {prop_a['config']['rooms']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Bathrooms:</strong> {prop_a['config']['bathrooms']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Area:</strong> {prop_a['config']['area']} m²</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>District:</strong> {prop_a['config']['district']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Amenities:</strong> {', '.join([a.split(' ', 1)[1] for a in prop_a['config']['amenities']]) if prop_a['config']['amenities'] else 'None'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); 
                    padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                    border: 1px solid rgba(255, 255, 255, 0.2);'>
            <h5 style='color: white; margin-bottom: 1rem;'>🏡 Property B Details</h5>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Rooms:</strong> {prop_b['config']['rooms']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Bathrooms:</strong> {prop_b['config']['bathrooms']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Area:</strong> {prop_b['config']['area']} m²</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>District:</strong> {prop_b['config']['district']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Amenities:</strong> {', '.join([a.split(' ', 1)[1] for a in prop_b['config']['amenities']]) if prop_b['config']['amenities'] else 'None'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Price Breakdown Comparison
    st.markdown("#### 💰 Price Breakdown Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); 
                    padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                    border: 1px solid rgba(255, 255, 255, 0.2);'>
            <h5 style='color: white; margin-bottom: 1rem;'>🏠 Property A Breakdown</h5>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Base Price:</strong> €{prop_a['breakdown']['base_price']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Rooms:</strong> €{prop_a['breakdown']['room_price']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Bathrooms:</strong> €{prop_a['breakdown']['bathroom_price']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Area:</strong> €{prop_a['breakdown']['area_price']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Amenities:</strong> €{prop_a['breakdown']['amenity_price']}</p>
            {f"<p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>District Boost:</strong> +{prop_a['breakdown']['district_boost']}%</p>" if prop_a['breakdown']['district_boost'] > 0 else ''}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); 
                    padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                    border: 1px solid rgba(255, 255, 255, 0.2);'>
            <h5 style='color: white; margin-bottom: 1rem;'>🏡 Property B Breakdown</h5>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Base Price:</strong> €{prop_b['breakdown']['base_price']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Rooms:</strong> €{prop_b['breakdown']['room_price']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Bathrooms:</strong> €{prop_b['breakdown']['bathroom_price']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Area:</strong> €{prop_b['breakdown']['area_price']}</p>
            <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Amenities:</strong> €{prop_b['breakdown']['amenity_price']}</p>
            {f"<p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>District Boost:</strong> +{prop_b['breakdown']['district_boost']}%</p>" if prop_b['breakdown']['district_boost'] > 0 else ''}
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendation
    st.markdown("#### 🎯 Value Analysis")
    
    # Calcular precio por m²
    price_per_sqm_a = prop_a['price'] / prop_a['config']['area']
    price_per_sqm_b = prop_b['price'] / prop_b['config']['area']
    
    if price_per_sqm_a < price_per_sqm_b:
        better_value = "Property A"
        better_color = "#667eea"
        recommendation = f"Property A offers better value at €{price_per_sqm_a:.0f}/m² vs €{price_per_sqm_b:.0f}/m²"
    else:
        better_value = "Property B"
        better_color = "#764ba2"
        recommendation = f"Property B offers better value at €{price_per_sqm_b:.0f}/m² vs €{price_per_sqm_a:.0f}/m²"
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {better_color}, rgba(255,255,255,0.1)); 
                padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);'>
        <h4 style='color: white; margin: 0 0 1rem 0;'>🏆 Best Value: {better_value}</h4>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.1rem;'>{recommendation}</p>
    </div>
    """, unsafe_allow_html=True)

elif enable_comparison:
    st.markdown("### ⚖️ Property Comparison")
    st.info("🔄 Configure and calculate prices for both Property A and Property B in the sidebar to see the comparison here.")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: rgba(255,255,255,0.7);'>
        <h4>How to use the comparison tool:</h4>
        <p>1. Enable "Property Comparison" in the sidebar</p>
        <p>2. Configure Property A and click "Calculate Property A"</p>
        <p>3. Configure Property B and click "Calculate Property B"</p>
        <p>4. The comparison will appear here automatically</p>
    </div>
    """, unsafe_allow_html=True)

# --- Mostrar precio estimado de forma prominente ---
if 'estimated_price' in st.session_state and st.session_state.estimated_price is not None:
    st.markdown("### 🎯 AI Price Prediction")
    
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
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.3rem; font-weight: 600;'>per month</p>
            <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.3);'>
                <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 1rem;'>Based on your selected criteria</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Mostrar breakdown del precio en el área principal
    if 'price_breakdown' in st.session_state:
        st.markdown("#### 📋 Price Breakdown")
        col1, col2 = st.columns(2)
        
        breakdown = st.session_state.price_breakdown
        with col1:
            st.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.2);'>
                <h5 style='color: white; margin-bottom: 1rem;'>💰 Base Components</h5>
                <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Base Price:</strong> €{breakdown['base_price']}</p>
                <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Rooms:</strong> €{breakdown['room_price']}</p>
                <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Bathrooms:</strong> €{breakdown['bathroom_price']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.2);'>
                <h5 style='color: white; margin-bottom: 1rem;'>🏗️ Additional Features</h5>
                <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Area:</strong> €{breakdown['area_price']}</p>
                <p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>Amenities:</strong> €{breakdown['amenity_price']}</p>
                {f"<p style='color: rgba(255,255,255,0.9); margin: 0.3rem 0;'><strong>District Boost:</strong> +{breakdown['district_boost']}%</p>" if breakdown.get('district_boost', 0) > 0 else ''}
            </div>
            """, unsafe_allow_html=True)

# --- Sección de métricas atractivas ---
st.markdown("### 📊 Property Market Insights")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='metric-container'>
        <div class='metric-value'>€364k</div>
        <div class='metric-label'>Avg Price</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-container'>
        <div class='metric-value'>96m²</div>
        <div class='metric-label'>Avg Area</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-container'>
        <div class='metric-value'>2.6</div>
        <div class='metric-label'>Avg Bedrooms</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='metric-container'>
        <div class='metric-value'>21</div>
        <div class='metric-label'>Districts</div>
    </div>
    """, unsafe_allow_html=True)

# --- Sección de estadísticas adicionales ---
st.markdown("### 📈 Market Trends")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='info-card'>
        <h4 style='color: white; margin-bottom: 15px;'>🏆 Most Popular Districts</h4>
        <ul style='color: rgba(255,255,255,0.8); margin: 0; padding-left: 20px;'>
            <li>Salamanca - €1,800/month avg</li>
            <li>Chamberí - €1,650/month avg</li>
            <li>Centro - €1,500/month avg</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='info-card'>
        <h4 style='color: white; margin-bottom: 15px;'>💰 Price Range Distribution</h4>
        <ul style='color: rgba(255,255,255,0.8); margin: 0; padding-left: 20px;'>
            <li>€0-200k: 27,698 properties (38%)</li>
            <li>€200-400k: 23,883 properties (33%)</li>
            <li>€400k+: 21,615 properties (30%)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style='margin-top: 50px; text-align: center; color: rgba(255,255,255,0.6); padding: 20px;'>
    <hr style='border: 1px solid rgba(255,255,255,0.2); margin: 20px 0;'>
    <p>Madrid Housing Dashboard | Powered by Machine Learning & Data Science</p>
    <p style='font-size: 0.9rem;'>Helping you find the perfect home in Madrid since 2024</p>
</div>
""", unsafe_allow_html=True)
