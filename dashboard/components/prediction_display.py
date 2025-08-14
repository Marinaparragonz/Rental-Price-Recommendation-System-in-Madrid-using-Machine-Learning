"""
Prediction display and filters summary components
"""
import streamlit as st
import pandas as pd
import os
from config.constants import MODEL_FILES
import pickle

def render_filters_summary(selected_amenities=None, rooms=None, bathrooms=None, area=None, selected_district=None):
    """Render the filters summary section"""
    # Get values from session state if not provided
    if selected_amenities is None:
        selected_amenities = st.session_state.get('selected_amenities', [])
    if rooms is None:
        rooms = st.session_state.get('rooms', 1)
    if bathrooms is None:
        bathrooms = st.session_state.get('bathrooms', 1)
    if area is None:
        area = st.session_state.get('area', 50)
    if selected_district is None:
        selected_district = st.session_state.get('last_selected_district', None)
    
    with st.expander("🔎 Selected Filters Summary", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"- **Rooms**: {rooms}")
            st.markdown(f"- **Bathrooms**: {bathrooms}")
            st.markdown(f"- **Area**: {area} m²")
        with col2:
            # Display amenities directly
            if selected_amenities:
                amenities_names = [a.split(' ', 1)[1] if ' ' in a else a for a in selected_amenities]  # Remove emoji
                amenities_text = ', '.join(amenities_names)
                st.markdown(f"- **Amenities**: {amenities_text}")
            else:
                st.markdown(f"- **Amenities**: None selected")
            
            # Display district synchronized with map
            district_display = selected_district if selected_district else "Click on map to select"
            st.markdown(f"- **Selected District**: {district_display}")
            
            # Visual indicator if district is selected
            if not selected_district:
                st.markdown(f"<span style='color: #ffc107; font-weight: bold;'>⚠ No district selected</span>", unsafe_allow_html=True)

def render_prediction_display():
    """Render the main prediction display section"""
    
    # Get values from session state
    estimated_price = st.session_state.get('estimated_price')
    prediction_method = st.session_state.get('prediction_method', '')
    
    if estimated_price is not None and prediction_method == "Random Forest ML Model":
        _render_successful_prediction(estimated_price)
    elif prediction_method == "Model not available":
        _render_model_unavailable()
    elif prediction_method == "Error":
        _render_prediction_error()
    else:
        _render_welcome_message()

def _render_successful_prediction(estimated_price):
    """Render successful prediction display"""
    st.markdown("### AI Property Price Prediction")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Display the estimated price in a prominent card with gradient background
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; 
                    border-radius: 20px; 
                    text-align: center; 
                    margin: 1.5rem 0; 
                    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4), 0 5px 15px rgba(0, 0, 0, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    backdrop-filter: blur(20px);'>
            <h2 style='color: white; margin: 0 0 0.5rem 0; font-size: 3rem; font-weight: 800; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);'>€{estimated_price:,}</h2>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1.3rem; font-weight: 600;'>estimated property value</p>
            <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.3);'>
                <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 1rem;'>AI Random Forest Model</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def _render_model_unavailable():
    """Render model unavailable message"""
    st.markdown("### ❌ Model Not Available")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Show error card indicating model needs to be trained
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

def _render_prediction_error():
    """Render prediction error message"""
    st.markdown("### ❌ Prediction Error")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Show error card for prediction failures
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

def _render_welcome_message():
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Show initial welcome card with instructions
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
                Configure your property preferences in the sidebar and click <strong>"Estimate Price"</strong> to get an intelligent prediction powered by a Random Forest model.
            </p>
            <div style='margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.2);'>
                <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.95rem;'>
                     Select district on map  •   Configure property details  •   Get instant predictions
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_prediction_breakdown():
    """Render detailed prediction breakdown if available - from model_info.pkl"""
    
    # Show detailed breakdown for ML model predictions
    if 'price_breakdown' in st.session_state and st.session_state.price_breakdown is not None:
        breakdown = st.session_state.price_breakdown
        prediction_method = st.session_state.get("prediction_method", "Unknown")
        
        if prediction_method.startswith("Random Forest"):
            try:
                with open(MODEL_FILES['model_info'], 'rb') as f:
                    model_info = pickle.load(f)
                
                performance = model_info.get('performance', {})
                r2_value = performance.get('r2', 0.0)
                mae_value = performance.get('mae', 0.0)
                rmse_value = performance.get('rmse', 0.0)
                features_used = len(model_info.get('features', []))
                
                model_name = model_info.get('model_type', 'Random Forest')
                
            except Exception as e:
                # Fallback values si no se puede cargar
                r2_value = 0.0
                mae_value = 0.0
                rmse_value = 0.0
                features_used = 20
                model_name = 'Random Forest'
            
            st.markdown(f"#### {model_name} Model Performance")

           
            if isinstance(rmse_value, (int, float)):
                rmse_display = f"€{rmse_value:,.0f}"
            else:
                rmse_display = f"€{rmse_value}"
            
            if isinstance(mae_value, (int, float)):
                mae_display = f"€{mae_value:,.0f}"
            else:
                mae_display = f"€{mae_value}"
            
            if isinstance(r2_value, (int, float)):
                r2_display = f"{r2_value:.4f}"
            else:
                r2_display = f"{r2_value}"
            
    
            col1, col2, col3, col4 = st.columns(4)
            
            # Column 1: Features Used
            with col1:
                st.markdown(f"""
                <div style='background: rgba(102, 126, 234, 0.3); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2); border: 1px solid rgba(102, 126, 234, 0.4);'>
                    <div style='font-size: 1.8rem; margin-bottom: 0.5rem; color: white; font-weight: bold; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);'>
                        {features_used}
                    </div>
                    <div style='color: rgba(255,255,255,0.95); font-size: 0.85rem; font-weight: 600;'>
                        Features Used
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Column 2: R² Score
            with col2:
                st.markdown(f"""
                <div style='background: rgba(102, 126, 234, 0.3); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2); border: 1px solid rgba(102, 126, 234, 0.4);'>
                    <div style='font-size: 1.8rem; margin-bottom: 0.5rem; color: white; font-weight: bold; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);'>
                        {r2_display}
                    </div>
                    <div style='color: rgba(255,255,255,0.95); font-size: 0.85rem; font-weight: 600;'>
                        R² Score
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Column 3: MAE
            with col3:
                st.markdown(f"""
                <div style='background: rgba(102, 126, 234, 0.3); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2); border: 1px solid rgba(102, 126, 234, 0.4);'>
                    <div style='font-size: 1.8rem; margin-bottom: 0.5rem; color: white; font-weight: bold; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);'>
                        {mae_display}
                    </div>
                    <div style='color: rgba(255,255,255,0.95); font-size: 0.85rem; font-weight: 600;'>
                        MAE
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Column 4: RMSE
            with col4:
                st.markdown(f"""
                <div style='background: rgba(102, 126, 234, 0.3); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; text-align: center; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2); border: 1px solid rgba(102, 126, 234, 0.4);'>
                    <div style='font-size: 1.8rem; margin-bottom: 0.5rem; color: white; font-weight: bold; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);'>
                        {rmse_display}
                    </div>
                    <div style='color: rgba(255,255,255,0.95); font-size: 0.85rem; font-weight: 600;'>
                        RMSE
                    </div>
                </div>
                """, unsafe_allow_html=True)
