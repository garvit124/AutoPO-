"""
Involexis Dashboard Theme Configuration
Red & Black color scheme
"""

# Color palette - Involexis Red & Black
PRIMARY_COLOR = "#DC143C"  # Crimson Red
SECONDARY_COLOR = "#000000"  # Black
BACKGROUND_COLOR = "#1E1E1E"  # Dark Gray
TEXT_COLOR = "#FFFFFF"  # White
ACCENT_COLOR = "#FF4444"  # Light Red

# Custom CSS for "Involexis Premium" look
CUSTOM_CSS = """
<style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    h1, h2, h3 {
        color: #DC143C !important;
    }
    
    .stMetric {
        background-color: #2D2D2D;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #DC143C;
    }
    
    .stMetric label {
        color: #FFFFFF !important;
    }
    
    .stMetric div {
        color: #DC143C !important;
    }
    
    .stDataFrame {
        background-color: #2D2D2D;
        border-radius: 10px;
    }
    
    .stButton>button {
        background-color: #DC143C;
        color: white;
        border-radius: 5px;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #FF4444;
        box-shadow: 0 4px 12px rgba(220, 20, 60, 0.4);
    }
    
    /* Logo styling */
    .logo-text {
        font-size: 2em;
        font-weight: bold;
        color: #DC143C;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #000000 0%, #2D2D2D 100%);
        border-radius: 10px;
        margin-bottom: 30px;
    }
</style>
"""

def apply_theme():
    """Apply custom theme to Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
def display_logo():
    """Display Involexis logo/branding."""
    import streamlit as st
    st.markdown('<div class="logo-text">INVOLEXIS</div>', unsafe_allow_html=True)



