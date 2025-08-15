"""
Market insights and model information components
"""
import streamlit as st
import pandas as pd
import os
import pickle
from config.constants import DATA_FILES, AMENITY_NAMES, MODEL_FILES

def render_market_insights():
    """Render market insights section exactly as in dashboard.py"""
    if not os.path.exists(DATA_FILES['clean_data']):
        st.error(f"Data file not found: {DATA_FILES['clean_data']}")
        return
        
    st.markdown("---")
    st.markdown("### 📈 Madrid Real Estate Market Insights")
    
    try:
        df = pd.read_csv(DATA_FILES['clean_data'])
        
        # Main metrics
        _render_main_metrics(df)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            _render_expensive_districts(df)
        
        with col2:
            _render_size_distribution(df)
            _render_property_features(df)
        
        _render_amenities_section(df)
        
    except Exception as e:
        st.error(f"Error loading market data: {e}")

def _render_main_metrics(df):
    """Render the three main metric cards"""
    col1, col2, col3 = st.columns(3)
    
    # Calculate metrics
    avg_price = df['PRICE'].mean()
    avg_area = df['CONSTRUCTEDAREA'].mean()
    avg_price_per_m2 = df['PRICE'].sum() / df['CONSTRUCTEDAREA'].sum()
    
    metrics = [
        (avg_price, "€{:,.0f}", "Average Price"),
        (avg_area, "{:.0f}m²", "Average Area"),
        (avg_price_per_m2, "€{:.0f}/m²", "Price per m²")
    ]
    
    for col, (value, format_str, label) in zip([col1, col2, col3], metrics):
        with col:
            st.markdown(f"""
            <div class='metric-container'>
                <div class='metric-value'>{format_str.format(value)}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

def _render_expensive_districts(df):
    """Render most expensive districts section"""
    st.markdown("#### Most Expensive Districts")
    
    district_col = 'DISTRICT' if 'DISTRICT' in df.columns else 'DISTRICT_CODE'
    
    if district_col not in df.columns:
        st.markdown("*District data not available*")
        return
    
    district_prices = df.groupby(district_col)['PRICE'].mean().sort_values(ascending=False).head(5)
    district_mapping = _load_district_mapping() if district_col == 'DISTRICT_CODE' else {}
    
    for i, (district, price) in enumerate(district_prices.items(), 1):
        display_name = _get_district_name(district, district_mapping) if district_col == 'DISTRICT_CODE' else district
        
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

def _render_size_distribution(df):
    """Render property size distribution section"""
    st.markdown("#### Property Size Distribution")
    
    small_props = len(df[df['CONSTRUCTEDAREA'] < 60])
    medium_props = len(df[(df['CONSTRUCTEDAREA'] >= 60) & (df['CONSTRUCTEDAREA'] < 120)])
    large_props = len(df[df['CONSTRUCTEDAREA'] >= 120])
    total_props = len(df)
    
    _render_size_category("Small (&lt;60m²)", small_props, total_props, "#ff6b6b")
    _render_size_category("Medium (60-120m²)", medium_props, total_props, "#4ecdc4")
    _render_size_category("Large (&gt;120m²)", large_props, total_props, "#45b7d1")

def _render_property_features(df):
    """Render average rooms and bathrooms"""
    avg_rooms = round(df['ROOMNUMBER'].mean()) if 'ROOMNUMBER' in df.columns else 0
    avg_bathrooms = round(df['BATHNUMBER'].mean()) if 'BATHNUMBER' in df.columns else 0
    
    if avg_rooms > 0 or avg_bathrooms > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Property Features")
        
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; margin: 8px 0;'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                <span style='font-weight: 500;'>Average Rooms</span>
                <span style='font-size: 1.3em; font-weight: bold;'>{avg_rooms}</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-weight: 500;'>Average Bathrooms</span>
                <span style='font-size: 1.3em; font-weight: bold;'>{avg_bathrooms}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def _render_amenities_section(df):
    """Render amenities distribution section"""
    amenity_columns = ['HASTERRACE', 'HASLIFT', 'HASAIRCONDITIONING', 'HASGARDEN', 
                      'HASPARKINGSPACE', 'HASBOXROOM', 'HASWARDROBE', 'HASDOORMAN', 'HASSWIMMINGPOOL']
    
    available_amenities = [col for col in amenity_columns if col in df.columns]
    
    if not available_amenities:
        return
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Property Amenities Distribution", expanded=False):
        
        amenity_names = {
            'HASTERRACE': 'Terrace', 'HASLIFT': 'Lift', 'HASAIRCONDITIONING': 'Air Conditioning',
            'HASGARDEN': 'Garden', 'HASPARKINGSPACE': 'Parking Space', 'HASBOXROOM': 'Storage Room',
            'HASWARDROBE': 'Built-in Wardrobe', 'HASDOORMAN': 'Doorman', 'HASSWIMMINGPOOL': 'Swimming Pool'
        }
        
        amenity_stats = []
        for col in available_amenities: 
            percentage = (df[col].sum() / len(df)) * 100
            name = amenity_names.get(col, col.replace('HAS', '').title())
            amenity_stats.append((name, percentage))
        
        amenity_stats.sort(key=lambda x: x[1], reverse=True)
        
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

def _load_district_mapping():
    """Load district mapping from file"""
    try:
        with open(MODEL_FILES['district_mapping'], 'rb') as f:
            return pickle.load(f)
    except Exception:
        return {}

def _get_district_name(district_code, district_mapping):
    """Get district name from code using mapping"""
    for name, code in district_mapping.items():
        if code == district_code:
            return name
    return district_code

def _render_size_category(label, count, total, color):
    """Render a single property size category bar"""
    percentage = count / total * 100
    st.markdown(f"""
    <div style='margin: 10px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin: 8px 0;'>
            <span><strong>{label}</strong></span>
            <span style='color: {color};'>{count:,} ({percentage:.1f}%)</span>
        </div>
        <div style='background: {color}20; height: 8px; border-radius: 4px;'>
            <div style='background: {color}; height: 100%; width: {percentage:.1f}%; border-radius: 4px;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
