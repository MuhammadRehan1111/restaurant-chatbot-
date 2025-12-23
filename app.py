"""
Restaurant Ordering System - Main Application Entry Point
Premium redesigned home page with logo and food showcase.
"""
import streamlit as st
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Restaurant Ordering System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Data directory
DATA_DIR = Path(__file__).parent / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"
IMAGES_DIR = DATA_DIR / "images"

def load_settings():
    """Load app settings."""
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {"logo": None, "restaurant_name": "Restaurant", "theme": "dark_luxury"}

def save_settings(settings):
    """Save app settings."""
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

settings = load_settings()

# Premium Dark Luxury Theme CSS
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Logo container */
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem 1rem;
        margin-bottom: 2rem;
    }
    
    .logo-image {
        max-width: 280px;
        max-height: 280px;
        border-radius: 50%;
        box-shadow: 0 0 60px rgba(212, 175, 55, 0.3), 0 0 100px rgba(212, 175, 55, 0.1);
        border: 3px solid rgba(212, 175, 55, 0.5);
        margin-bottom: 1.5rem;
    }
    
    .restaurant-name {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #d4af37 0%, #f7e98e 50%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
    }
    
    .tagline {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #ffffff; /* White text */
        text-align: center;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    /* Section header */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        background: linear-gradient(135deg, #d4af37 0%, #f7e98e 50%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 2.5rem 0 1.5rem 0;
        position: relative;
        font-weight: 700;
    }
    
    .section-header::after {
        content: '';
        display: block;
        width: 80px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
        margin: 0.75rem auto 0;
    }
    
    /* Food item cards */
    .food-card {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.9) 0%, rgba(15, 15, 26, 0.95) 100%);
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(212, 175, 55, 0.2);
        transition: all 0.3s ease;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .food-card:hover {
        transform: translateY(-5px);
        border-color: rgba(212, 175, 55, 0.5);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 30px rgba(212, 175, 55, 0.1);
    }
    
    .food-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    
    .food-info {
        padding: 1.25rem;
    }
    
    .food-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        color: #d4af37; /* Golden color */
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .food-price {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #d4af37;
        font-weight: 600;
    }
    
    /* Navigation buttons */
    .nav-btn {
        display: inline-block;
        padding: 1rem 2.5rem;
        margin: 0.5rem;
        background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
        color: #0a0a0f !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 50px;
        text-decoration: none;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
    }
    
    .nav-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(212, 175, 55, 0.5);
    }
    
    .nav-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        margin: 2rem 0;
    }
    
    /* Page links styling */
    .stPageLink > a {
        background: rgba(26, 26, 46, 0.9) !important;
        border: 1px solid rgba(212, 175, 55, 0.5) !important;
        border-radius: 15px !important;
        color: #d4af37 !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stPageLink > a:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.2) !important;
        border-color: #d4af37 !important;
        background: rgba(212, 175, 55, 0.1) !important;
    }
    
    /* Footer */
    .premium-footer {
        text-align: center;
        padding: 2rem;
        color: #ffffff; /* White text */
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        border-top: 1px solid rgba(212, 175, 55, 0.1);
        margin-top: 3rem;
    }
    
    /* Ensure white text on blue/dark backgrounds */
    .stAlert {
        color: #ffffff !important;
    }
    .stAlert [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
    .stAlert [data-testid="stMarkdownContainer"] b {
        color: #d4af37 !important; /* Golden for bold text in alerts */
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.8) 0%, rgba(15, 15, 26, 0.9) 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-number {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        color: #d4af37;
        font-weight: 700;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        color: #ffffff; /* White text */
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Streamlit metric overrides */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.8) 0%, rgba(15, 15, 26, 0.9) 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 15px;
        padding: 1rem;
    }
    
    [data-testid="stMetricValue"] {
        color: #d4af37 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff !important; /* White text */
    }
</style>
""", unsafe_allow_html=True)

# Logo Section
st.markdown('<div class="logo-container">', unsafe_allow_html=True)

# Display logo if available
logo_path = settings.get('logo')
if logo_path and Path(logo_path).exists():
    st.image(logo_path, width=280)
else:
    # Default elegant placeholder
    st.markdown("""
    <div style="width: 180px; height: 180px; 
                background: linear-gradient(135deg, #d4af37 0%, #b8860b 100%);
                border-radius: 50%; 
                display: flex; align-items: center; justify-content: center;
                font-size: 5rem; color: #0a0a0f;
                box-shadow: 0 0 60px rgba(212, 175, 55, 0.4);
                margin: 0 auto 1.5rem auto;">
        🍽️
    </div>
    """, unsafe_allow_html=True)

restaurant_name = settings.get('restaurant_name', 'Restaurant')
st.markdown(f'<h1 class="restaurant-name">{restaurant_name}</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Premium Dining Experience</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation Buttons
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    nav_cols = st.columns(3)
    with nav_cols[0]:
        st.page_link("pages/1_🍽️_Customer_Order.py", label="🍽️ Order Now", use_container_width=True)
    with nav_cols[1]:
        st.page_link("pages/2_💰_Cashier_Panel.py", label="💰 Cashier", use_container_width=True)
    with nav_cols[2]:
        st.page_link("pages/3_🔐_Admin_Panel.py", label="🔐 Admin", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Featured Items Section
st.markdown('<h2 class="section-header">Featured Delicacies</h2>', unsafe_allow_html=True)

# Import database functions
import sys
sys.path.insert(0, str(Path(__file__).parent))

try:
    from utils.database import load_menu
    
    menu = load_menu()
    
    # Get featured items (first 2 from each category, max 6 total)
    featured_items = []
    for category, items in menu.items():
        available = [item for item in items if item.get('available', True)]
        featured_items.extend(available[:2])
    
    featured_items = featured_items[:6]
    
    if featured_items:
        cols = st.columns(3)
        for i, item in enumerate(featured_items):
            with cols[i % 3]:
                image_url = item.get('image', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400')
                name = item['name'].get('en', 'Delicious Item')
                price = item['price']
                
                st.markdown(f"""
                <div class="food-card">
                    <img src="{image_url}" class="food-image" alt="{name}" onerror="this.src='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400'">
                    <div class="food-info">
                        <div class="food-name">{name}</div>
                        <div class="food-price">{price} SAR</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.info("Visit our menu to explore our delicious offerings!")

# Footer
st.markdown("""
<div class="premium-footer">
    <p>🍽️ Premium Dining Experience | Powered by AI</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">English • اردو • العربية</p>
</div>
""", unsafe_allow_html=True)
