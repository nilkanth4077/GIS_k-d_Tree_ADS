import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from kd_tree import build_kdtree, nearest_neighbor, range_search
import streamlit.components.v1 as components

if "lat" not in st.session_state:
    st.session_state.lat = 23.0225

if "lon" not in st.session_state:
    st.session_state.lon = 72.5714

# ------------------ SESSION STATE ------------------
if "results" not in st.session_state:
    st.session_state.results = None

if "search_type" not in st.session_state:
    st.session_state.search_type = None
# --------------------------------------------------

def get_current_location():
    html_code = """
    <script>
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            const streamlitInput = window.parent.document.querySelectorAll('input[type="number"]');
            streamlitInput[0].value = lat;
            streamlitInput[1].value = lon;
            streamlitInput[0].dispatchEvent(new Event('input', { bubbles: true }));
            streamlitInput[1].dispatchEvent(new Event('input', { bubbles: true }));
        }
    );
    </script>
    """
    components.html(html_code)

# Page Config
st.set_page_config(page_title="GIS using k-D Tree", layout="wide")

st.title("📍 Geographic Information System using k-D Tree")
st.markdown("### Ahmedabad Municipal Corporation Spatial Dataset")

# Load dataset
df = pd.read_csv("ahmedabad_facilities.csv")

# Sidebar Inputs
st.sidebar.header("🔍 Search Panel")

# if st.sidebar.button("📍 Use My Current Location"):
#     get_current_location()
#     st.info("Location detected. Click Search to apply.")

lat = st.sidebar.number_input(
    "Enter Latitude",
    value=st.session_state.lat,
    format="%.6f"
)

lon = st.sidebar.number_input(
    "Enter Longitude",
    value=st.session_state.lon,
    format="%.6f"
)

st.session_state.lat = lat
st.session_state.lon = lon

category = st.sidebar.selectbox(
    "Select Facility Type",
    ["All"] + sorted(df["category"].unique())
)

search_type = st.sidebar.radio(
    "Select Search Type",
    ["Nearest Neighbor", "Range Search"]
)

radius = st.sidebar.slider(
    "Radius (for range search)",
    0.001, 0.05, 0.01
)

# Filter Data
if category == "All":
    filtered_df = df
else:
    filtered_df = df[df["category"] == category]

points = list(zip(
    filtered_df["lat"],
    filtered_df["lon"],
    filtered_df["name"],
    filtered_df["category"]
))

tree = build_kdtree(points)
query = (lat, lon)

# ------------------ SEARCH BUTTON ------------------
if st.sidebar.button("Search"):
    st.session_state.search_type = search_type

    if search_type == "Nearest Neighbor":
        st.session_state.results = nearest_neighbor(tree, query)

    else:
        results = []
        range_search(tree, query, radius, results)
        st.session_state.results = results
# --------------------------------------------------

# ------------------ MAP SETUP ------------------
m = folium.Map(location=[lat, lon], zoom_start=13)

facility_colors = {
    "Swimming_pools": "blue",
    "Municipal_gyms": "brown",
    "Library": "green"
}

folium.Marker(
    [lat, lon],
    tooltip="Query Location",
    icon=folium.Icon(color="red")
).add_to(m)

# ------------------ PLOT STORED RESULTS ------------------
if st.session_state.results:

    if st.session_state.search_type == "Nearest Neighbor":
        r = st.session_state.results
        color = facility_colors.get(r[3], "gray")

        st.success(f"Nearest Facility: {r[2]} ({r[3]})")
        folium.Marker(
            [r[0], r[1]],
            tooltip=f"{r[2]} ({r[3]})",
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

    else:
        st.success(f"Total facilities found: {len(st.session_state.results)}")

        for r in st.session_state.results:
            color = facility_colors.get(r[3], "gray")
            folium.CircleMarker(
                [r[0], r[1]],
                radius=6,
                popup=f"{r[2]} ({r[3]})",
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8
            ).add_to(m)
# --------------------------------------------------

# Display Map
st_folium(m, width=900)

# Show Dataset
st.markdown("### 📊 Dataset Preview")
st.dataframe(df.head(20))