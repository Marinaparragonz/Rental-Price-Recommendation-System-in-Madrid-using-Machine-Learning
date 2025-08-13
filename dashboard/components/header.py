"""
Header component for the dashboard
"""
import streamlit as st
from utils.model_utils import get_model_status

def render_header():
    """Render the main header section"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <h1 style='text-align: center; color: white; font-size: 3rem; margin-bottom: 0.5rem; font-weight: 700;'>
            Madrid Housing Dashboard
        </h1>
        """, unsafe_allow_html=True)
        
        # Subtitle with description
        st.markdown("""
        <p style='text-align: center; color: rgba(255, 255, 255, 0.8); font-size: 1.2rem; margin-bottom: 0.3rem; font-weight: 400;'>
            Property Price Prediction in Madrid using Machine Learning
        </p>
        """, unsafe_allow_html=True)
        
        # Data source information
        st.markdown("""
        <p style='text-align: center; color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin-bottom: 1.5rem; font-style: italic;'>
            Based on Madrid Real Estate Market Data (2018)
        </p>
        """, unsafe_allow_html=True)
        
    # Model status indicator
    model_status, model_color = get_model_status()
    
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 1rem;'>
        <span style='background: rgba(255, 255, 255, 0.15); color: {model_color}; padding: 8px 16px; border-radius: 20px; font-weight: 600; font-size: 0.9rem; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);'>
            {model_status}
        </span>
    </div>
    """, unsafe_allow_html=True)