"""
Sidebar component for filters and controls
"""
import streamlit as st
from config.constants import AMENITIES_OPTIONS
from utils.model_utils import load_trained_model, predict_with_model, is_model_available

def render_sidebar():
    """Render the sidebar with all controls"""
    st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 2rem; padding: 1rem 0; border-bottom: 2px solid rgba(102, 126, 234, 0.2);'>
        <h1 style='color: #2c3e50; font-size: 1.8rem; margin-bottom: 0.8rem; font-weight: 900; text-align: center; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);'>Filter Properties</h1>
        <p style='color: #34495e; font-size: 1rem; font-weight: 500; text-align: center; margin: 0;'>Customize your search criteria</p>
    </div>
    """, unsafe_allow_html=True)

    # Property specifications section
    _render_property_specs()
    
    # Amenities selection
    selected_amenities = _render_amenities_selection()
    
    # Selected district display
    _render_selected_district()
    
    # Prediction button
    _render_prediction_button(selected_amenities)
    
    return selected_amenities

def _render_property_specs():
    """Render property specifications section"""
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
    
    # Store in session state
    st.session_state.rooms = rooms
    st.session_state.bathrooms = bathrooms
    st.session_state.area = area

def _render_amenities_selection():
    """Render amenities selection section"""
    st.sidebar.markdown("""
    <div style='margin: 30px 0 20px 0; padding: 0 0 15px 0; border-bottom: 2px solid rgba(102, 126, 234, 0.4);'>
        <h3 style='color: #2c3e50; font-weight: 700; margin: 0; font-size: 1.6rem !important; display: flex; align-items: center; text-transform: capitalize;'>
            <span style='background: linear-gradient(45deg, #667eea, #764ba2); width: 4px; height: 20px; border-radius: 2px; margin-right: 12px; display: block;'></span>
            Select Amenities
        </h3>
    </div>
    """, unsafe_allow_html=True)

    return st.sidebar.multiselect(" Property Amenities", options=AMENITIES_OPTIONS, help="Select all desired amenities for your property")

def _render_selected_district():
    """Render selected district display"""
    st.sidebar.markdown("""
    <div style='margin: 30px 0 20px 0; padding: 0 0 15px 0; border-bottom: 2px solid rgba(102, 126, 234, 0.4);'>
        <h3 style='color: #2c3e50; font-weight: 700; margin: 0; font-size: 1.15rem; display: flex; align-items: center; text-transform: capitalize;'>
            <span style='background: linear-gradient(45deg, #667eea, #764ba2); width: 4px; height: 20px; border-radius: 2px; margin-right: 12px; display: block;'></span>
            Selected District
        </h3>
    </div>
    """, unsafe_allow_html=True)

    selected_district = st.session_state.get("last_selected_district", None)
    
    if selected_district:
        st.sidebar.markdown(f"""
        <div style='background: linear-gradient(45deg, #667eea, #764ba2); padding: 15px; border-radius: 12px; text-align: center; margin: 10px 0; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'>
            <h4 style='color: white; margin: 0; font-size: 1.1rem; font-weight: 600;'>{selected_district}</h4>
            <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 0.9rem;'>District selected</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div style='background: rgba(108, 117, 125, 0.3); padding: 15px; border-radius: 12px; text-align: center; margin: 10px 0; border: 2px dashed rgba(108, 117, 125, 0.5);'>
            <h4 style='color: #6c757d; margin: 0; font-size: 1.1rem; font-weight: 600;'>No District Selected</h4>
            <p style='color: rgba(108, 117, 125, 0.8); margin: 5px 0 0 0; font-size: 0.9rem;'>Click on the map to select</p>
        </div>
        """, unsafe_allow_html=True)

def _render_prediction_button(selected_amenities):
    """Render prediction button and handle prediction logic"""
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.sidebar.button(" Estimate Price", use_container_width=True, help="Generate AI-powered price prediction based on your selections"):
        input_params = {
            'area': st.session_state.get('area', 80),
            'rooms': st.session_state.get('rooms', 3),
            'bathrooms': st.session_state.get('bathrooms', 2),
            'amenities': selected_amenities,
            'district': st.session_state.get("last_selected_district", None)
        }
        
        with st.spinner("Loading AI model..."):
            model, district_mapping, model_features, model_info = load_trained_model()
        
        if model is not None:
            if model_info:
                st.sidebar.info(f"🤖 **Random Forest Model Loaded**\n"
                              f"📊 Features: {len(model_features)}\n"
                              f"🏘️ Districts: {len(district_mapping)}\n"
                              f"📈 R²: {model_info.get('performance', {}).get('r2', 'N/A'):.3f}")
            
            with st.spinner("Predicting with Random Forest..."):
                estimated_price = predict_with_model(model, district_mapping, model_features, model_info, input_params)
            
            if estimated_price is not None:
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
                st.sidebar.success(f"🤖 ML Prediction: €{estimated_price:,}")
            else:
                st.session_state.estimated_price = None
                st.session_state.prediction_method = "Error"
                st.session_state.price_breakdown = None
                st.sidebar.error("❌ Error making prediction with the model")
        else:
            st.session_state.estimated_price = None
            st.session_state.prediction_method = "Model not available"
            st.session_state.price_breakdown = None
            st.sidebar.error("❌ Random Forest model not available. Please train and save the model first.")
            st.sidebar.info("📝 Run the Random_Forest.ipynb notebook to train and save the model.")
        
        st.rerun()