"""
Map component for district selection
"""
import streamlit as st
import folium
import geopandas as gpd
import os
from streamlit_folium import st_folium
from config.constants import DATA_FILES

# Optional imports with error handling
try:
    from shapely.geometry import Point
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False

def render_map():
    """Render the interactive Madrid districts map"""
    
    try:
        # --- Load GeoJSON data and get selected district ---
        if os.path.exists(DATA_FILES['geojson']):
            gdf_districts = gpd.read_file(DATA_FILES['geojson'])
            gdf_districts = gdf_districts.to_crs(epsg=4326)  # Ensure lat/lon format
            
            # --- Initialize selected district from session_state ---
            selected_district = st.session_state.get("last_selected_district", None)

            # --- Create the map ---
            madrid_center = [40.4168, -3.7038]
            m = folium.Map(
                location=madrid_center, 
                zoom_start=12, 
                tiles="CartoDB positron",
                control_scale=False,
                prefer_canvas=True
            )

            # --- Add district polygons with events ---
            for idx, row in gdf_districts.iterrows():
                district_name = row["name"]
                
                # Determine if this district is selected
                is_selected = (selected_district == district_name)
                
                # Create polygon with improved configuration to capture clicks
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
                    # Add tooltip with district name (appears on hover)
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
                    # No popup to avoid annoying boxes when clicking
                )
                
                # Add polygon to map
                geojson_layer.add_to(m)

            # --- Display map and interact ---
            st.markdown("""
            <div class='map-container'>
                <h2 style='color: white; text-align: center; margin-bottom: 20px;'> 📍 Select District by Clicking on the Map</h2>
            </div>
            """, unsafe_allow_html=True)

            map_data = st_folium(
                m, 
                width="100%", 
                height=600, 
                returned_objects=["last_object_clicked_tooltip", "last_object_clicked"],
                key="madrid_map",
                use_container_width=True
            )

            # Add additional CSS to completely remove any popup or unwanted visual element
            _add_map_styling()
            
            # Handle map interactions
            _handle_map_interactions(map_data, gdf_districts)
            
            _add_map_cleanup_script()
            
    except Exception as e:
        st.error(f"❌ Error loading map: {str(e)}")
        st.info("🔧 Please check that all required files are present and accessible.")

def _handle_map_interactions(map_data, gdf_districts):
    """Handle map click interactions and district selection"""
    try:
        new_selected_district = None
        district_changed = False

        if map_data:
            if map_data.get("last_object_clicked_tooltip"):
                tooltip_text = map_data["last_object_clicked_tooltip"]
                new_district = tooltip_text.replace("✓ ", "") if tooltip_text.startswith("✓ ") else tooltip_text
                if new_district != st.session_state.get("last_selected_district"):
                    new_selected_district = new_district
                    district_changed = True
            
            # Fallback method: Using coordinates (only if tooltip fails)
            elif map_data.get("last_object_clicked") and isinstance(map_data["last_object_clicked"], dict):
                clicked_coords = map_data["last_object_clicked"]
                if "lat" in clicked_coords and "lng" in clicked_coords and SHAPELY_AVAILABLE:
                    lat = clicked_coords["lat"]
                    lng = clicked_coords["lng"]
                    clicked_point = Point(lng, lat)
                    
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

        # Update state
        if new_selected_district:
            st.session_state["last_selected_district"] = new_selected_district
            
        if district_changed:
            st.rerun()
                    
    except Exception as e:
        st.error(f"Error handling map interaction: {str(e)}")

def _add_map_styling():
    """Add CSS styling to remove unwanted map elements"""
    st.markdown("""
    <style>
    /* Remove popups and overlays completely */
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

    /* Remove annoying selection overlays */
    .leaflet-overlay-pane .leaflet-interactive:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    .leaflet-interactive:active,
    .leaflet-interactive:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Ensure no black borders or annoying visual elements */
    .leaflet-clickable {
        outline: none !important;
    }

    .leaflet-container a.leaflet-popup-close-button {
        display: none !important;
    }

    /* Improve tooltip appearance */
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

def _add_map_cleanup_script():
    """Add JavaScript to remove unwanted map elements"""
    st.markdown("""
    <script>
    // Function to remove popups and unwanted visual elements more aggressively
    function removeUnwantedMapElements() {
        // Remove all popups
        const popups = document.querySelectorAll('.leaflet-popup, .leaflet-popup-pane, .leaflet-popup-content-wrapper, .leaflet-popup-tip');
        popups.forEach(popup => {
            popup.style.display = 'none';
            popup.style.visibility = 'hidden';
            popup.style.opacity = '0';
            popup.remove();
        });
        
        // Remove popup containers
        const popupPanes = document.querySelectorAll('.leaflet-popup-pane');
        popupPanes.forEach(pane => {
            pane.style.display = 'none';
            pane.innerHTML = '';
        });
        
        // Ensure no annoying overlays
        const overlays = document.querySelectorAll('.leaflet-overlay-pane .leaflet-interactive');
        overlays.forEach(overlay => {
            overlay.style.outline = 'none';
            overlay.style.boxShadow = 'none';
            // Remove any click listener that might generate popups
            overlay.removeEventListener('click', null);
        });
        
        // Remove any element with black boxes
        const interactiveElements = document.querySelectorAll('.leaflet-interactive');
        interactiveElements.forEach(el => {
            el.style.outline = 'none';
            el.style.border = 'none';
            el.style.boxShadow = 'none';
        });
    }

    // Execute function immediately
    removeUnwantedMapElements();

    // Execute function every time a change is detected in the map
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

    // Also execute when clicking on the map or when loading
    document.addEventListener('click', function(e) {
        if (e.target.closest('.folium-map')) {
            setTimeout(removeUnwantedMapElements, 10);
        }
    });

    // Execute periodically to ensure unwanted elements don't appear
    setInterval(removeUnwantedMapElements, 1000);

    // Execute when page is fully loaded
    window.addEventListener('load', function() {
        setTimeout(removeUnwantedMapElements, 500);
    });
    </script>
    """, unsafe_allow_html=True)