"""
Footer component for Madrid Housing Dashboard
"""
import streamlit as st

def render_footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: rgba(255, 255, 255, 0.7); margin-top: 2rem; padding: 1.5rem 0;'>
        <div style='margin-bottom: 0.5rem;'>
            <p style='color: rgba(255, 255, 255, 0.6); margin: 0; font-size: 1rem; font-weight: 500;'>
                Madrid Property Price Prediction Dashboard
            </p>
        </div>
        <div style='font-size: 1rem; color: rgba(255, 255, 255, 0.6);'>
            <p style='margin: 0; font-weight: 500;'>
                Powered by Random Forest Machine Learning | Built with Streamlit
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)