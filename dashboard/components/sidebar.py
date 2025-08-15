"""
Sidebar component for filters and controls
"""
import streamlit as st
from config.constants import AMENITIES_OPTIONS
from utils.model_utils import load_trained_model, predict_with_model

# Constants for styling
SECTION_STYLES = {
    'gradient': 'linear-gradient(45deg, #667eea, #764ba2)',
    'text_color': '#2c3e50',
    'border': '2px solid rgba(102, 126, 234, 0.4)',
    'secondary_color': '#34495e'
}

def render_sidebar():
    """Render the sidebar with all controls"""
    _render_sidebar_header()
    _render_property_specs()
    selected_amenities = _render_amenities_selection()
    _render_selected_district()
    _render_prediction_button(selected_amenities)
    
    return selected_amenities

def _render_sidebar_header():
    """Render sidebar header section"""
    st.sidebar.markdown(f"""
    <div style='text-align: center; margin-bottom: 2rem; padding: 1rem 0; border-bottom: {SECTION_STYLES['border']};'>
        <h1 style='color: {SECTION_STYLES['text_color']}; font-size: 1.8rem; margin-bottom: 0.8rem; font-weight: 900; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);'>Filter Properties</h1>
        <p style='color: {SECTION_STYLES['secondary_color']}; font-size: 1rem; font-weight: 500; margin: 0;'>Customize your search criteria</p>
    </div>
    """, unsafe_allow_html=True)

def _render_section_header(title):
    """Render a section header with consistent styling"""
    st.sidebar.markdown(f"""
    <div style='margin: 30px 0 20px 0; padding: 0 0 15px 0; border-bottom: {SECTION_STYLES['border']};'>
        <h3 style='color: {SECTION_STYLES['text_color']}; font-weight: 700; margin: 0; font-size: 1.15rem; display: flex; align-items: center; text-transform: capitalize;'>
            <span style='background: {SECTION_STYLES['gradient']}; width: 4px; height: 20px; border-radius: 2px; margin-right: 12px; display: block;'></span>
            {title}
        </h3>
    </div>
    """, unsafe_allow_html=True)

def _render_property_specs():
    """Render property specifications section"""
    _render_section_header("Property Specifications")
    
    # Property sliders with session state management
    sliders_config = [
        ("🛏️ Number of Rooms", "rooms", 1, 7, 3, "Select the number of bedrooms"),
        ("🚿 Number of Bathrooms", "bathrooms", 1, 4, 2, "Select the number of bathrooms"),
        ("📐 Constructed Area (m²)", "area", 30, 300, 80, "Select the total area of the property")
    ]
    
    for label, key, min_val, max_val, default, help_text in sliders_config:
        value = st.sidebar.slider(label, min_value=min_val, max_value=max_val, value=default, help=help_text)
        st.session_state[key] = value

def _render_amenities_selection():
    """Render amenities selection section"""
    _render_section_header("Select Amenities")
    return st.sidebar.multiselect(" Property Amenities", options=AMENITIES_OPTIONS, help="Select all desired amenities for your property")

def _render_selected_district():
    """Render selected district display"""
    _render_section_header("Selected District")
    
    selected_district = st.session_state.get("last_selected_district", None)
    
    if selected_district:
        _render_district_card(selected_district, "selected")
    else:
        _render_district_card("No District Selected", "unselected")

def _render_district_card(district_name, card_type):
    """Render district card with specified type"""
    if card_type == "selected":
        bg_style = f'background: {SECTION_STYLES["gradient"]}; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'
        text_color = 'white'
        subtitle = 'District selected'
        subtitle_color = 'rgba(255,255,255,0.9)'
    else:
        bg_style = 'background: rgba(108, 117, 125, 0.3); border: 2px dashed rgba(108, 117, 125, 0.5);'
        text_color = '#6c757d'
        subtitle = 'Click on the map to select'
        subtitle_color = 'rgba(108, 117, 125, 0.8)'
    
    st.sidebar.markdown(f"""
    <div style='{bg_style} padding: 15px; border-radius: 12px; text-align: center; margin: 10px 0;'>
        <h4 style='color: {text_color}; margin: 0; font-size: 1.1rem; font-weight: 600;'>{district_name}</h4>
        <p style='color: {subtitle_color}; margin: 5px 0 0 0; font-size: 0.9rem;'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def _render_prediction_button(selected_amenities):
    """Render prediction button and handle click"""
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.sidebar.button(" Estimate Price", use_container_width=True, help="Generate AI-powered price prediction based on your selections"):
        _handle_prediction_request(selected_amenities)

def _handle_prediction_request(selected_amenities):
    """Handle the prediction request logic"""
    input_params = _prepare_input_params(selected_amenities)
    
    # Load model with spinner
    with st.spinner("Loading AI model..."):
        model_data = load_trained_model()
    
    if _is_model_loaded(model_data):
        _process_successful_model_load(model_data, input_params)
    else:
        _handle_model_not_available()
    
    st.rerun()

def _prepare_input_params(selected_amenities):
    """Prepare input parameters for prediction"""
    return {
        'area': st.session_state.get('area', 80),
        'rooms': st.session_state.get('rooms', 3),
        'bathrooms': st.session_state.get('bathrooms', 2),
        'amenities': selected_amenities,
        'district': st.session_state.get("last_selected_district", None)
    }

def _is_model_loaded(model_data):
    """Check if model was loaded successfully"""
    model, district_mapping, model_features, model_info = model_data
    return model is not None

def _process_successful_model_load(model_data, input_params):
    """Process successful model load and make prediction"""
    model, district_mapping, model_features, model_info = model_data
    
    # Show model info
    if model_info:
        _display_model_info(model_features, district_mapping, model_info)
    
    # Make prediction
    with st.spinner("Predicting with Random Forest..."):
        estimated_price = predict_with_model(model, district_mapping, model_features, model_info, input_params)
    
    if estimated_price is not None:
        _handle_successful_prediction(estimated_price, model_features, model_info, input_params)
    else:
        _handle_prediction_error()

def _display_model_info(model_features, district_mapping, model_info):
    """Display model information in sidebar"""
    r2_score = model_info.get('performance', {}).get('r2', 'N/A')
    r2_display = f"{r2_score:.3f}" if isinstance(r2_score, (int, float)) else str(r2_score)
    
    st.sidebar.info(f"**Random Forest Model Loaded**\n"
                   f"Features: {len(model_features)}\n"
                   f"Districts: {len(district_mapping)}\n"
                   f"R²: {r2_display}")

def _handle_successful_prediction(estimated_price, model_features, model_info, input_params):
    """Handle successful prediction result"""
    st.session_state.estimated_price = estimated_price
    st.session_state.prediction_method = "Random Forest ML Model"
    st.session_state.price_breakdown = {
        'base_prediction': estimated_price,
        'model_used': 'Random Forest',
        'features_used': len(model_features),
        'district': input_params['district'] or 'Not specified',
        'confidence': 'High (ML Model)',
        'model_performance': f"R²: {model_info.get('performance', {}).get('r2', 'N/A'):.3f}"
    }
    st.sidebar.success(f"ML Prediction: €{estimated_price:,}")

def _handle_prediction_error():
    """Handle prediction error"""
    st.session_state.estimated_price = None
    st.session_state.prediction_method = "Error"
    st.session_state.price_breakdown = None
    st.sidebar.error("Error making prediction with the model")

def _handle_model_not_available():
    """Handle case when model is not available"""
    st.session_state.estimated_price = None
    st.session_state.prediction_method = "Model not available"
    st.session_state.price_breakdown = None
    st.sidebar.error(" Random Forest model not available. Please train and save the model first.")
    st.sidebar.info("Run the Random_Forest.ipynb notebook to train and save the model.")