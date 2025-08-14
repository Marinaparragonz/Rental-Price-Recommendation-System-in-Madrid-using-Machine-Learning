"""
Market insights and model information components
"""
import streamlit as st
import pandas as pd
import os
import pickle
import joblib
from config.constants import DATA_FILES, AMENITY_NAMES, MODEL_FILES

try:
    from sklearn.ensemble import RandomForestRegressor
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

def render_market_insights():
    """Render market insights section exactly as in dashboard.py"""
    if os.path.exists(DATA_FILES['clean_data']):
        st.markdown("---")
        st.markdown("### 📈 Madrid Real Estate Market Insights")
        
        try:
            # Load clean data for market analysis
            df = pd.read_csv(DATA_FILES['clean_data'])
            
            # Display general market statistics
            col1, col2, col3 = st.columns(3)
            
            # Average price metric
            with col1:
                avg_price = df['PRICE'].mean()
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-value'>€{avg_price:,.0f}</div>
                    <div class='metric-label'>Average Price</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Average area metric
            with col2:
                avg_area = df['CONSTRUCTEDAREA'].mean()
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-value'>{avg_area:.0f}m²</div>
                    <div class='metric-label'>Average Area</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Price per square meter metric
            with col3:
                avg_price = df['PRICE'].mean()
                avg_area = df['CONSTRUCTEDAREA'].mean()
                avg_price_per_m2 = avg_price / avg_area
                st.markdown(f"""
                <div class='metric-container'>
                    <div class='metric-value'>€{avg_price_per_m2:.0f}/m²</div>
                    <div class='metric-label'>Price per m²</div>
                </div>
                """, unsafe_allow_html=True)
            
            # District analysis and property size distribution
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            # Left column: Most expensive districts
            with col1:
                st.markdown("#### Most Expensive Districts")
                
                # Check which district column is available
                district_col = 'DISTRICT' if 'DISTRICT' in df.columns else 'DISTRICT_CODE'
                
                if district_col in df.columns:
                    # Get top 5 most expensive districts
                    district_prices = df.groupby(district_col)['PRICE'].mean().sort_values(ascending=False).head(5)
                    
                    # Display each district with its average price
                    for i, (district, price) in enumerate(district_prices.items(), 1):
                        # Map district code to name if needed
                        display_name = district
                        if district_col == 'DISTRICT_CODE' and os.path.exists(MODEL_FILES['district_mapping']):
                            with open(MODEL_FILES['district_mapping'], 'rb') as f:
                                district_mapping = pickle.load(f)
                            # Find name by code
                            for name, code in district_mapping.items():
                                if code == district:
                                    display_name = name
                                    break
                                
                        # Display district ranking card
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
            
            # Right column: Property size distribution
            with col2:
                st.markdown("#### Property Size Distribution")
                
                # Calculate property size categories
                small_props = len(df[df['CONSTRUCTEDAREA'] < 60])
                medium_props = len(df[(df['CONSTRUCTEDAREA'] >= 60) & (df['CONSTRUCTEDAREA'] < 120)])
                large_props = len(df[df['CONSTRUCTEDAREA'] >= 120])
                total_props = len(df)
                
                # Display small properties bar
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
                
                # Display medium properties bar
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
                
                # Display large properties bar
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
                
                # Additional property features information
                st.markdown("<br>", unsafe_allow_html=True)
                avg_rooms = round(df['ROOMNUMBER'].mean()) if 'ROOMNUMBER' in df.columns else 0
                avg_bathrooms = round(df['BATHNUMBER'].mean()) if 'BATHNUMBER' in df.columns else 0
                
                st.markdown("#### Property Features")
                
                # Display average rooms
                if avg_rooms > 0:
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin: 8px 0;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <span style='font-weight: 500;'>Average Rooms</span>
                            <span style='font-size: 1.3em; font-weight: bold;'>{avg_rooms:.1f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display average bathrooms
                if avg_bathrooms > 0:
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin: 8px 0;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <span style='font-weight: 500;'>Average Bathrooms</span>
                            <span style='font-size: 1.3em; font-weight: bold;'>{avg_bathrooms:.1f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
            # Property amenities overview section
            amenity_columns = ['HASTERRACE', 'HASLIFT', 'HASAIRCONDITIONING', 'HASGARDEN', 
                              'HASPARKINGSPACE', 'HASBOXROOM', 'HASWARDROBE', 'HASDOORMAN', 'HASSWIMMINGPOOL']
            
            available_amenities = [col for col in amenity_columns if col in df.columns]
            
            if available_amenities:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("Property Amenities Distribution", expanded=False):
                    
                    # Mapping of column names to user-friendly names
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
                    
                    # Calculate amenity percentages
                    amenity_stats = []
                    for col in available_amenities:
                        if col in df.columns:
                            percentage = (df[col].sum() / len(df)) * 100
                            name = amenity_names.get(col, col.replace('HAS', '').title())
                            amenity_stats.append((name, percentage))
                    
                    # Sort by percentage descending
                    amenity_stats.sort(key=lambda x: x[1], reverse=True)
                    
                    # Display all amenities with progress bars
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
    else:
        st.warning("📊 Market data not available. Please ensure data_clean.csv is in the project directory.")


def render_model_info():
    """Render model information section exactly as in dashboard.py"""
    if SKLEARN_AVAILABLE and os.path.exists(MODEL_FILES['model']):
        st.markdown("---")
        st.markdown("### 📊 Model Information & Performance")
        
        # Load model information for display
        try:
            model, district_mapping, model_features, model_info = load_trained_model()
            
            if model_info and model_features and district_mapping:
                # Display main model metrics
                col1, col2, col3, col4 = st.columns(4)
                
                # R² Score metric
                with col1:
                    r2_score = model_info.get('performance', {}).get('r2', 0)
                    st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-value'>{r2_score:.3f}</div>
                        <div class='metric-label'>R² Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Mean Absolute Error metric
                with col2:
                    mae = model_info.get('performance', {}).get('mae', 0)
                    st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-value'>€{mae:,.0f}</div>
                        <div class='metric-label'>Mean Absolute Error</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Features used metric
                with col3:
                    st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-value'>{len(model_features)}</div>
                        <div class='metric-label'>Features Used</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Districts covered metric
                with col4:
                    st.markdown(f"""
                    <div class='metric-container'>
                        <div class='metric-value'>{len(district_mapping)}</div>
                        <div class='metric-label'>Districts Covered</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display feature importance if available
                if 'feature_importance' in model_info and model_info['feature_importance']:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("🔍 Top Important Features", expanded=False):
                        feature_importance = model_info['feature_importance']
                        
                        # Create two columns for feature display
                        col1, col2 = st.columns(2)
                        
                        # Split features into two lists
                        mid_point = len(feature_importance) // 2
                        first_half = list(feature_importance.items())[:mid_point]
                        second_half = list(feature_importance.items())[mid_point:]
                        
                        # Display first half of features
                        with col1:
                            for feature, importance in first_half:
                                # Translate technical names to user-friendly names
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
                        
                        # Display second half of features
                        with col2:
                            for feature, importance in second_half:
                                # Translate technical names to user-friendly names
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

@st.cache_resource
def load_trained_model():
    """
    Loads the trained Random Forest model and its associated components
    Returns: model, district_mapping, model_features, model_info
    """
    try:
        if SKLEARN_AVAILABLE and os.path.exists(MODEL_FILES['model']):
            # Load the trained model
            model = joblib.load(MODEL_FILES['model'])
            
            # Load district name to DISTRICT_CODE mapping
            with open(MODEL_FILES['district_mapping'], 'rb') as f:
                district_mapping = pickle.load(f)
            
            # Load model features list
            with open(MODEL_FILES['model_features'], 'rb') as f:
                model_features = pickle.load(f)
                
            # Load model information (optional)
            with open(MODEL_FILES['model_info'], 'rb') as f:
                model_info = pickle.load(f)
            
            return model, district_mapping, model_features, model_info
        else:
            return None, None, None, None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None, None, None