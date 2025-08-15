"""
Prediction display and filters summary components
"""
import streamlit as st
import pickle
from config.constants import MODEL_FILES

# Constants for styling
CARD_STYLES = {
    'success': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'error': 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)',
    'info': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)'
}

METRIC_BACKGROUND = 'rgba(102, 126, 234, 0.3)'

# Error message configurations
ERROR_CONFIGS = {
    "Model not available": {
        'main_text': " Model Required",
        'subtitle': "Random Forest model not found", 
        'footer': "Please run Random_Forest.ipynb to train and save the model",
        'title': " Model Not Available"
    },
    "Error": {
        'main_text': " Prediction Error",
        'subtitle': "Unable to generate prediction",
        'footer': "Please check model configuration", 
        'title': " Prediction Error"
    }
}

def render_filters_summary(selected_amenities=None, rooms=None, bathrooms=None, area=None, selected_district=None):
    """Render the filters summary section"""

    params = {
        'selected_amenities': selected_amenities or st.session_state.get('selected_amenities', []),
        'rooms': rooms or st.session_state.get('rooms', 1),
        'bathrooms': bathrooms or st.session_state.get('bathrooms', 1),
        'area': area or st.session_state.get('area', 50),
        'selected_district': selected_district or st.session_state.get('last_selected_district', None)
    }
    
    with st.expander("🔎 Selected Filters Summary", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            - **Rooms**: {params['rooms']}
            - **Bathrooms**: {params['bathrooms']}
            - **Area**: {params['area']} m²
            """)
        
        with col2:
            # Display amenities
            if params['selected_amenities']:
                amenities_names = [a.split(' ', 1)[1] if ' ' in a else a for a in params['selected_amenities']]
                amenities_text = ', '.join(amenities_names)
                st.markdown(f"- **Amenities**: {amenities_text}")
            else:
                st.markdown("- **Amenities**: None selected")
            
            # Display district
            district_display = params['selected_district'] if params['selected_district'] else "Click on map to select"
            st.markdown(f"- **Selected District**: {district_display}")
            
            if not params['selected_district']:
                st.markdown("<span style='color: #ffc107; font-weight: bold;'>⚠ No district selected</span>", unsafe_allow_html=True)

def render_prediction_display():
    """Render the main prediction display section"""
    estimated_price = st.session_state.get('estimated_price')
    prediction_method = st.session_state.get('prediction_method', '')
    
    # Handle successful prediction
    if estimated_price is not None and prediction_method == "Random Forest ML Model":
        _render_prediction_card('success', f"€{estimated_price:,}", "estimated property value", "AI Random Forest Model", "AI Property Price Prediction")
    
    # Handle error cases using configuration
    elif prediction_method in ERROR_CONFIGS:
        config = ERROR_CONFIGS[prediction_method]
        _render_prediction_card('error', config['main_text'], config['subtitle'], config['footer'], config['title'])
    
    # Default welcome message
    else:
        _render_welcome_message()

def _render_prediction_card(card_type, main_text, subtitle, footer_text, title):
    """Render a prediction card with specified styling"""
    st.markdown(f"### {title}")
    
    _render_centered_content(CARD_STYLES[card_type], f"""
        <h2 style='color: white; margin: 0 0 0.5rem 0; font-size: {"3rem" if card_type == "success" else "2rem"}; font-weight: 800; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);'>{main_text}</h2>
        <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.1rem; font-weight: 600;'>{subtitle}</p>
        <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.3);'>
            <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;'>{footer_text}</p>
        </div>
    """)

def _render_welcome_message():
    """Render welcome message for new users"""
    _render_centered_content(CARD_STYLES['info'], """
        <div style='font-size: 4rem; margin-bottom: 1rem;'>🏡</div>
        <h2 style='color: white; margin: 0 0 1rem 0; font-size: 1.8rem; font-weight: 700; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);'>Get AI-Powered Price Predictions</h2>
        <p style='color: rgba(255,255,255,0.8); margin: 0 0 1.5rem 0; font-size: 1.1rem; line-height: 1.5;'>
            Configure your property preferences in the sidebar and click <strong>"Estimate Price"</strong> to get an intelligent prediction powered by a Random Forest model.
        </p>
        <div style='margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.2);'>
            <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.95rem;'>
                 Select district on map  •   Configure property details  •   Get instant predictions
            </p>
        </div>
    """)

def _render_centered_content(background, content):
    """Render content in a centered column with specified background"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='background: {background}; 
                    padding: 2rem; 
                    border-radius: 20px; 
                    text-align: center; 
                    margin: 1.5rem 0; 
                    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4), 0 5px 15px rgba(0, 0, 0, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(20px);'>
            {content}
        </div>
        """, unsafe_allow_html=True)

def render_prediction_breakdown():
    """Render detailed prediction breakdown if available"""
    if not _should_show_breakdown():
        return
    
    model_info = _load_model_info()
    if not model_info:
        return
    
    st.markdown(f"#### {model_info.get('model_type', 'Random Forest')} Model Performance")
    
    metrics = _prepare_metrics_data(model_info)
    _render_metrics_grid(metrics)

def _should_show_breakdown():
    """Check if breakdown should be shown"""
    return (st.session_state.get('price_breakdown') is not None and 
            st.session_state.get('prediction_method', '').startswith('Random Forest'))

def _load_model_info():
    """Load model info with fallback values"""
    try:
        with open(MODEL_FILES['model_info'], 'rb') as f:
            return pickle.load(f)
    except Exception:
        return {
            'performance': {'r2': 0.0, 'mae': 0.0, 'rmse': 0.0},
            'features': [None] * 20,
            'model_type': 'Random Forest'
        }

def _prepare_metrics_data(model_info):
    """Prepare metrics data for display"""
    performance = model_info['performance'] 
    
    return [
        (len(model_info['features']), "Features Used"),
        (_format_metric(performance['r2'], 'ratio'), "R² Score"),
        (_format_metric(performance['mae'], 'currency'), "MAE"),
        (_format_metric(performance['rmse'], 'currency'), "RMSE")
    ]

def _format_metric(value, metric_type):
    """Format metric value based on type"""
    if not isinstance(value, (int, float)):
        return str(value)
    
    return f"€{value:,.0f}" if metric_type == 'currency' else f"{value:.4f}"

def _render_metrics_grid(metrics):
    """Render metrics in a grid layout"""
    cols = st.columns(4)
    
    for col, (value, label) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div style='background: {METRIC_BACKGROUND}; 
                        backdrop-filter: blur(15px); 
                        padding: 1.5rem; 
                        border-radius: 15px; 
                        margin: 1rem 0; 
                        text-align: center; 
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2); 
                        border: 1px solid rgba(102, 126, 234, 0.4);'>
                <div style='font-size: 1.8rem; margin-bottom: 0.5rem; color: white; font-weight: bold; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);'>
                    {value}
                </div>
                <div style='color: rgba(255,255,255,0.95); font-size: 0.85rem; font-weight: 600;'>
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)
