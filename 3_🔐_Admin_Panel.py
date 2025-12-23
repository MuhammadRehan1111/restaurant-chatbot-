"""
Admin Panel - Restaurant Management System
Premium redesigned with category analytics, logo upload, and multilingual support.
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from io import BytesIO
import json
import base64
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import (
    load_menu, save_menu, add_menu_item, update_menu_item, delete_menu_item,
    load_orders, get_paid_orders, get_pending_orders,
    load_deals, save_deals, add_deal, update_deal, delete_deal, get_next_deal_id,
    load_categories, save_categories, add_category, update_category, delete_category,
    get_active_categories, get_next_category_order
)
from utils.auth import check_password, logout
import config

# Page configuration
st.set_page_config(
    page_title="Admin Panel - Restaurant",
    page_icon="🔐",
    layout="wide"
)

# Data directories
DATA_DIR = Path(__file__).parent.parent / "data"
IMAGES_DIR = DATA_DIR / "images"
SETTINGS_FILE = DATA_DIR / "settings.json"

# Ensure images directory exists
IMAGES_DIR.mkdir(exist_ok=True)

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

def save_uploaded_file(uploaded_file, prefix="img"):
    """Save uploaded file and return the path."""
    if uploaded_file is not None:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = Path(uploaded_file.name).suffix
        filename = f"{prefix}_{timestamp}{ext}"
        filepath = IMAGES_DIR / filename
        
        # Save file
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return str(filepath)
    return None

# Translation dictionary
translations = {
    "English": {
        "admin_panel": "🔐 Admin Panel",
        "restaurant_management": "Restaurant Management System",
        "logout": "🚪 Logout",
        "categories": "📂 Categories",
        "menu_management": "📋 Menu Management",
        "deals": "🎁 Deals & Combos",
        "order_history": "📜 Order History",
        "analytics": "📊 Analytics",
        "settings": "⚙️ Settings",
        "add_category": "➕ Add Category",
        "add_item": "➕ Add Item",
        "add_deal": "➕ Add Deal",
        "save": "💾 Save",
        "delete": "🗑️ Delete",
        "cancel": "Cancel",
        "key_metrics": "💰 Key Metrics",
        "total_revenue": "💵 Total Revenue",
        "total_orders": "📋 Total Orders",
        "avg_order": "📊 Avg Order Value",
        "top_selling": "🏆 Top Selling Items",
        "payment_methods": "💳 Payment Methods"
    },
    "اردو (Urdu)": {
        "admin_panel": "🔐 ایڈمن پینل",
        "restaurant_management": "ریستوران مینجمنٹ سسٹم",
        "logout": "🚪 لاگ آؤٹ",
        "categories": "📂 زمرے",
        "menu_management": "📋 مینو مینجمنٹ",
        "deals": "🎁 ڈیلز اور کومبوز",
        "order_history": "📜 آرڈر ہسٹری",
        "analytics": "📊 تجزیات",
        "settings": "⚙️ ترتیبات",
        "add_category": "➕ زمرہ شامل کریں",
        "add_item": "➕ آئٹم شامل کریں",
        "add_deal": "➕ ڈیل شامل کریں",
        "save": "💾 محفوظ کریں",
        "delete": "🗑️ حذف کریں",
        "cancel": "منسوخ",
        "key_metrics": "💰 اہم میٹرکس",
        "total_revenue": "💵 کل آمدنی",
        "total_orders": "📋 کل آرڈرز",
        "avg_order": "📊 اوسط آرڈر ویلیو",
        "top_selling": "🏆 ٹاپ سیلنگ آئٹمز",
        "payment_methods": "💳 ادائیگی کے طریقے"
    },
    "العربية (Arabic)": {
        "admin_panel": "🔐 لوحة الإدارة",
        "restaurant_management": "نظام إدارة المطعم",
        "logout": "🚪 تسجيل خروج",
        "categories": "📂 الفئات",
        "menu_management": "📋 إدارة القائمة",
        "deals": "🎁 العروض والكومبو",
        "order_history": "📜 سجل الطلبات",
        "analytics": "📊 التحليلات",
        "settings": "⚙️ الإعدادات",
        "add_category": "➕ إضافة فئة",
        "add_item": "➕ إضافة عنصر",
        "add_deal": "➕ إضافة عرض",
        "save": "💾 حفظ",
        "delete": "🗑️ حذف",
        "cancel": "إلغاء",
        "key_metrics": "💰 المقاييس الرئيسية",
        "total_revenue": "💵 إجمالي الإيرادات",
        "total_orders": "📋 إجمالي الطلبات",
        "avg_order": "📊 متوسط قيمة الطلب",
        "top_selling": "🏆 الأكثر مبيعاً",
        "payment_methods": "💳 طرق الدفع"
    }
}

# Premium Dark Luxury Theme CSS
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .admin-header {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(184, 134, 11, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
    
    .admin-header h2 {
        font-family: 'Playfair Display', serif;
        color: #d4af37;
        margin: 0;
    }
    
    .admin-header p {
        color: #ffffff; /* White text */
        margin: 0.5rem 0 0 0;
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.9) 0%, rgba(15, 15, 26, 0.95) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        text-align: center;
    }
    
    .stat-number {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #d4af37;
        font-weight: 700;
    }
    
    .stat-label {
        font-family: 'Inter', sans-serif;
        color: #ffffff; /* White text */
        font-size: 0.9rem;
    }
    
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        background: linear-gradient(135deg, #d4af37 0%, #f7e98e 50%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1.5rem 0 1rem 0;
        font-weight: 700;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(26, 26, 46, 0.5);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        border-radius: 8px;
        color: #ffffff; /* White text */
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(184, 134, 11, 0.1));
        color: #d4af37;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(184, 134, 11, 0.1)) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        color: #d4af37 !important;
        border-radius: 10px !important;
    }
    
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #d4af37, #b8860b) !important;
        color: #0a0a0f !important;
        border: none !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(26, 26, 46, 0.8) !important;
        border-radius: 10px !important;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.8) 0%, rgba(15, 15, 26, 0.9) 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 12px;
        padding: 1rem;
    }
    
    [data-testid="stMetricValue"] {
        color: #d4af37 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #ffffff !important; /* White text */
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(26, 26, 46, 0.5);
        border-radius: 10px;
        padding: 1rem;
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
    
    /* Global label and header contrast fixes */
    label[data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    h3 {
        color: #d4af37 !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
    }
    
    /* Expander (Category/Menu Box) styling */
    [data-testid="stExpander"] {
        background: rgba(26, 26, 46, 0.5) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 12px !important;
        margin-bottom: 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stExpander"]:hover {
        border-color: rgba(212, 175, 55, 0.6) !important;
        background: rgba(26, 26, 46, 0.7) !important;
    }
    
    [data-testid="stExpander"] summary p {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: transparent !important;
        padding: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication
if not check_password():
    st.stop()

settings = load_settings()

# Language selection in session state
if 'admin_language' not in st.session_state:
    st.session_state.admin_language = "English"

def t(key):
    """Get translation for key."""
    return translations.get(st.session_state.admin_language, translations["English"]).get(key, key)

# Header
st.markdown(f"""
<div class="admin-header">
    <h2>{t('admin_panel')}</h2>
    <p>{t('restaurant_management')}</p>
</div>
""", unsafe_allow_html=True)

# Top bar: Language and Logout
col1, col2, col3 = st.columns([5, 1.5, 1])
with col2:
    language = st.selectbox(
        "🌐", 
        ["English", "اردو (Urdu)", "العربية (Arabic)"], 
        key="lang_select",
        label_visibility="collapsed"
    )
    if language != st.session_state.admin_language:
        st.session_state.admin_language = language
        st.rerun()
with col3:
    if st.button(t('logout')):
        logout()

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    t('settings'),
    t('categories'),
    t('menu_management'), 
    t('deals'), 
    t('order_history'), 
    t('analytics')
])

# =============================================================================
# TAB 1: SETTINGS (Logo Upload, Restaurant Name)
# =============================================================================
with tab1:
    st.markdown(f'<p class="section-header">{t("settings")}</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏷️ Restaurant Branding")
        
        # Restaurant name
        new_name = st.text_input("Restaurant Name", value=settings.get('restaurant_name', 'Restaurant'))
        
        # Logo upload
        st.markdown("### 🖼️ Logo")
        
        current_logo = settings.get('logo')
        if current_logo and Path(current_logo).exists():
            st.image(current_logo, width=200)
            if st.button("🗑️ Remove Logo"):
                settings['logo'] = None
                save_settings(settings)
                st.success("Logo removed!")
                st.rerun()
        
        uploaded_logo = st.file_uploader("Upload Logo", type=['png', 'jpg', 'jpeg', 'gif'], key="logo_upload")
        
        if uploaded_logo:
            st.image(uploaded_logo, width=200, caption="Preview")
        
        if st.button("💾 Save Settings", type="primary"):
            settings['restaurant_name'] = new_name
            
            if uploaded_logo:
                logo_path = save_uploaded_file(uploaded_logo, "logo")
                settings['logo'] = logo_path
            
            save_settings(settings)
            st.success("Settings saved! ✅")
            st.rerun()
    
    with col2:
        st.markdown("### 📊 App Statistics")
        
        orders = load_orders()
        menu = load_menu()
        deals_list = load_deals()
        
        st.metric("Total Orders", len(orders))
        st.metric("Menu Items", sum(len(items) for items in menu.values()))
        st.metric("Active Deals", len([d for d in deals_list if d.get('active')]))

# =============================================================================
# TAB 2: CATEGORY MANAGEMENT
# =============================================================================
with tab2:
    st.markdown(f'<p class="section-header">{t("categories")}</p>', unsafe_allow_html=True)
    
    categories = load_categories()
    
    # Add new category
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(t('add_category'), type="primary", use_container_width=True):
            st.session_state.show_add_category = True
    
    if st.session_state.get('show_add_category', False):
        st.markdown("#### Add New Category")
        with st.form("add_category_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_cat_id = st.text_input("Category ID (e.g., desserts)", help="Unique identifier, lowercase, no spaces")
                new_cat_name = st.text_input("Category Name")
                new_cat_image = st.file_uploader("Category Image", type=['png', 'jpg', 'jpeg'])
            with col2:
                new_cat_icon = st.text_input("Icon (emoji)", value="🍽️")
                new_cat_desc = st.text_input("Description")
                new_cat_active = st.checkbox("Active", value=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(t('add_category'), type="primary"):
                    image_path = None
                    if new_cat_image:
                        image_path = save_uploaded_file(new_cat_image, f"cat_{new_cat_id}")
                    
                    new_category = {
                        "id": new_cat_id.lower().replace(" ", "_"),
                        "name": new_cat_name,
                        "icon": new_cat_icon,
                        "description": new_cat_desc,
                        "image": image_path,
                        "active": new_cat_active,
                        "order": get_next_category_order()
                    }
                    if add_category(new_category):
                        st.success("Category added!")
                        st.session_state.show_add_category = False
                        st.rerun()
            with col2:
                if st.form_submit_button(t('cancel')):
                    st.session_state.show_add_category = False
                    st.rerun()
    
    st.divider()
    
    # Display categories
    if not categories:
        st.info("No categories yet. Add one to get started!")
    else:
        for cat in sorted(categories, key=lambda x: x.get('order', 999)):
            status = "🟢" if cat.get('active', True) else "🔴"
            with st.expander(f"{status} {cat.get('icon', '🍽️')} {cat['name']}"):
                with st.form(f"edit_cat_{cat['id']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        ed_name = st.text_input("Name", value=cat['name'], key=f"cat_name_{cat['id']}")
                        ed_icon = st.text_input("Icon", value=cat.get('icon', '🍽️'), key=f"cat_icon_{cat['id']}")
                        ed_image = st.file_uploader("Update Image", type=['png', 'jpg', 'jpeg'], key=f"cat_img_{cat['id']}")
                    with col2:
                        ed_desc = st.text_input("Description", value=cat.get('description', ''), key=f"cat_desc_{cat['id']}")
                        ed_order = st.number_input("Order", value=cat.get('order', 1), key=f"cat_order_{cat['id']}")
                        ed_active = st.checkbox("Active", value=cat.get('active', True), key=f"cat_active_{cat['id']}")
                        
                        if cat.get('image') and Path(cat['image']).exists():
                            st.image(cat['image'], width=100)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button(t('save')):
                            image_path = cat.get('image')
                            if ed_image:
                                image_path = save_uploaded_file(ed_image, f"cat_{cat['id']}")
                            
                            updated = {**cat, "name": ed_name, "icon": ed_icon, "description": ed_desc, 
                                       "order": ed_order, "active": ed_active, "image": image_path}
                            update_category(cat['id'], updated)
                            st.success("Updated!")
                            st.rerun()
                    with col2:
                        if st.form_submit_button(t('delete')):
                            delete_category(cat['id'])
                            st.success("Deleted!")
                            st.rerun()

# =============================================================================
# TAB 3: MENU MANAGEMENT
# =============================================================================
with tab3:
    st.markdown(f'<p class="section-header">{t("menu_management")}</p>', unsafe_allow_html=True)
    
    menu = load_menu()
    categories_list = [c['name'] for c in get_active_categories()]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_category = st.selectbox("Select Category", options=categories_list if categories_list else ["No categories"], key="menu_category")
    with col2:
        if st.button(t('add_item'), type="primary"):
            st.session_state.show_add_item = True
    
    # Add new item form
    if st.session_state.get('show_add_item', False):
        st.markdown("#### Add New Item")
        with st.form("add_item_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_item_id = st.text_input("Item ID (e.g., ff06)")
                name_en = st.text_input("Name (English)")
                price = st.number_input("Price (SAR)", min_value=0.0, step=1.0)
            with col2:
                category = st.selectbox("Category", options=categories_list)
                desc_en = st.text_area("Description")
                image_file = st.file_uploader("Item Image", type=['png', 'jpg', 'jpeg'])
                available = st.checkbox("Available", value=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(t('add_item'), type="primary"):
                    image_path = None
                    if image_file:
                        image_path = save_uploaded_file(image_file, f"item_{new_item_id}")
                    
                    new_item = {
                        "item_id": new_item_id,
                        "name": {"en": name_en, "ur": "", "ar": ""},
                        "price": price,
                        "description": {"en": desc_en, "ur": "", "ar": ""},
                        "image": image_path if image_path else "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400",
                        "available": available
                    }
                    add_menu_item(category, new_item)
                    st.success("Item added!")
                    st.session_state.show_add_item = False
                    st.rerun()
            with col2:
                if st.form_submit_button(t('cancel')):
                    st.session_state.show_add_item = False
                    st.rerun()
    
    st.divider()
    
    # Display items in selected category
    if selected_category and selected_category in menu:
        items = menu[selected_category]
        for item in items:
            status = "🟢" if item.get('available', True) else "🔴"
            with st.expander(f"{status} {item['name'].get('en', 'Unknown')} - {item['price']} SAR"):
                with st.form(f"edit_{item['item_id']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        ed_name = st.text_input("Name", value=item['name'].get('en', ''), key=f"name_{item['item_id']}")
                        ed_price = st.number_input("Price", value=float(item['price']), key=f"price_{item['item_id']}")
                        ed_desc = st.text_area("Description", value=item.get('description', {}).get('en', ''), key=f"desc_{item['item_id']}")
                    with col2:
                        ed_image_file = st.file_uploader("Update Image", type=['png', 'jpg', 'jpeg'], key=f"imgfile_{item['item_id']}")
                        ed_available = st.checkbox("Available", value=item.get('available', True), key=f"avail_{item['item_id']}")
                        
                        # Show current image
                        current_img = item.get('image', '')
                        if current_img:
                            if current_img.startswith('http'):
                                st.image(current_img, width=150)
                            elif Path(current_img).exists():
                                st.image(current_img, width=150)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button(t('save')):
                            image_path = item.get('image', '')
                            if ed_image_file:
                                image_path = save_uploaded_file(ed_image_file, f"item_{item['item_id']}")
                            
                            updated = {**item, "name": {"en": ed_name, "ur": "", "ar": ""}, "price": ed_price, 
                                       "description": {"en": ed_desc, "ur": "", "ar": ""}, "image": image_path, "available": ed_available}
                            update_menu_item(item['item_id'], updated)
                            st.success("Updated!")
                            st.rerun()
                    with col2:
                        if st.form_submit_button(t('delete')):
                            delete_menu_item(item['item_id'])
                            st.success("Deleted!")
                            st.rerun()

# =============================================================================
# TAB 4: DEALS & COMBOS
# =============================================================================
with tab4:
    st.markdown(f'<p class="section-header">{t("deals")}</p>', unsafe_allow_html=True)
    
    deals = load_deals()
    
    if st.button(t('add_deal'), type="primary"):
        st.session_state.show_add_deal = True
    
    if st.session_state.get('show_add_deal', False):
        st.markdown("#### Add New Deal")
        with st.form("add_deal_form"):
            col1, col2 = st.columns(2)
            with col1:
                deal_name = st.text_input("Deal Name")
                discount = st.number_input("Discount %", min_value=0, max_value=100, value=10)
                deal_image = st.file_uploader("Deal Image", type=['png', 'jpg', 'jpeg'])
            with col2:
                deal_desc = st.text_area("Description")
                deal_active = st.checkbox("Active", value=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(t('add_deal'), type="primary"):
                    image_path = None
                    if deal_image:
                        image_path = save_uploaded_file(deal_image, f"deal_{get_next_deal_id()}")
                    
                    new_deal = {
                        "deal_id": get_next_deal_id(),
                        "name": {"en": deal_name, "ur": "", "ar": ""},
                        "description": {"en": deal_desc, "ur": "", "ar": ""},
                        "discount_percent": discount,
                        "applicable_items": [],
                        "min_items": 1,
                        "image": image_path,
                        "active": deal_active
                    }
                    add_deal(new_deal)
                    st.success("Deal added!")
                    st.session_state.show_add_deal = False
                    st.rerun()
            with col2:
                if st.form_submit_button(t('cancel')):
                    st.session_state.show_add_deal = False
                    st.rerun()
    
    st.divider()
    
    for deal in deals:
        status = "🟢" if deal.get('active') else "🔴"
        with st.expander(f"{status} {deal['name'].get('en', 'Deal')} - {deal.get('discount_percent', 0)}% OFF"):
            with st.form(f"edit_deal_{deal['deal_id']}"):
                col1, col2 = st.columns(2)
                with col1:
                    ed_name = st.text_input("Name", value=deal['name'].get('en', ''), key=f"deal_name_{deal['deal_id']}")
                    ed_discount = st.number_input("Discount %", value=deal.get('discount_percent', 0), key=f"deal_disc_{deal['deal_id']}")
                    ed_deal_image = st.file_uploader("Update Image", type=['png', 'jpg', 'jpeg'], key=f"deal_img_{deal['deal_id']}")
                with col2:
                    ed_desc = st.text_area("Description", value=deal.get('description', {}).get('en', ''), key=f"deal_desc_{deal['deal_id']}")
                    ed_active = st.checkbox("Active", value=deal.get('active', False), key=f"deal_active_{deal['deal_id']}")
                    
                    if deal.get('image') and Path(deal['image']).exists():
                        st.image(deal['image'], width=150)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button(t('save')):
                        image_path = deal.get('image')
                        if ed_deal_image:
                            image_path = save_uploaded_file(ed_deal_image, f"deal_{deal['deal_id']}")
                        
                        updated = {**deal, "name": {"en": ed_name}, "description": {"en": ed_desc}, 
                                   "discount_percent": ed_discount, "active": ed_active, "image": image_path}
                        update_deal(deal['deal_id'], updated)
                        st.success("Updated!")
                        st.rerun()
                with col2:
                    if st.form_submit_button(t('delete')):
                        delete_deal(deal['deal_id'])
                        st.success("Deleted!")
                        st.rerun()

# =============================================================================
# TAB 5: ORDER HISTORY
# =============================================================================
with tab5:
    st.markdown(f'<p class="section-header">{t("order_history")}</p>', unsafe_allow_html=True)
    
    orders = load_orders()
    
    if not orders:
        st.info("No orders yet.")
    else:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Status", ["All", "Pending", "Paid"])
        with col2:
            payment_filter = st.selectbox("Payment Method", ["All", "Cash", "Card"])
        with col3:
            date_range = st.date_input("Date Range", value=(datetime.now().date() - timedelta(days=7), datetime.now().date()))
        
        # Apply filters
        filtered = orders.copy()
        
        if status_filter != "All":
            filtered = [o for o in filtered if o.get('status') == status_filter]
        
        if payment_filter != "All":
            filtered = [o for o in filtered if o.get('payment_method') == payment_filter]
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered = [o for o in filtered if start_date <= datetime.fromisoformat(o.get('timestamp', datetime.now().isoformat())).date() <= end_date]
        
        st.markdown(f"**Showing {len(filtered)} orders**")
        
        if filtered:
            # Create DataFrame
            df_data = []
            for o in filtered:
                items_str = ", ".join([f"{i['name']} x{i['quantity']}" for i in o.get('items', [])])
                df_data.append({
                    "Order ID": o.get('order_id'),
                    "Items": items_str,
                    "Total (SAR)": o.get('total_price', 0),
                    "Status": o.get('status'),
                    "Payment": o.get('payment_method', '-'),
                    "Time": o.get('timestamp', '')[:16].replace('T', ' ')
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Export
            col1, col2 = st.columns(2)
            with col1:
                csv = df.to_csv(index=False)
                st.download_button("📥 Export CSV", csv, f"orders_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
            with col2:
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                st.download_button("📥 Export Excel", buffer.getvalue(), f"orders_{datetime.now().strftime('%Y%m%d')}.xlsx")

# =============================================================================
# TAB 6: ANALYTICS (Category-specific top sellers)
# =============================================================================
with tab6:
    st.markdown(f'<p class="section-header">{t("analytics")}</p>', unsafe_allow_html=True)
    st.caption("⚠️ Analytics calculated from **PAID orders only**")
    
    paid_orders = get_paid_orders()
    
    if not paid_orders:
        st.info("No paid orders for analytics.")
    else:
        df = pd.DataFrame(paid_orders)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Date filter
        col1, col2 = st.columns([2, 2])
        with col1:
            analytics_range = st.date_input("Date Range", value=(datetime.now().date() - timedelta(days=30), datetime.now().date()), key="analytics_date")
        
        if len(analytics_range) == 2:
            start_date, end_date = analytics_range
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        # Key metrics (3 metrics)
        st.markdown(f"### {t('key_metrics')}")
        col1, col2, col3 = st.columns(3)
        
        total_revenue = df['total_price'].sum()
        total_orders = len(df)
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        
        with col1:
            st.metric(t('total_revenue'), f"{total_revenue:,.0f} SAR")
        with col2:
            st.metric(t('total_orders'), total_orders)
        with col3:
            st.metric(t('avg_order'), f"{avg_order:,.0f} SAR")
        
        st.divider()
        
        # Payment Methods Chart
        st.markdown(f"### {t('payment_methods')}")
        payment_data = df['payment_method'].value_counts().reset_index()
        payment_data.columns = ['Method', 'Count']
        
        fig = px.pie(payment_data, values='Count', names='Method', hole=0.4,
                    color_discrete_sequence=['#d4af37', '#f7e98e', '#b8860b', '#ffd700'])
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff', family='Inter, sans-serif'),
            title=dict(
                text=f"<b>{t('payment_methods')}</b>",
                font=dict(color='#d4af37', size=20),
                x=0.5,
                xanchor='center'
            ),
            legend=dict(font=dict(color='#ffffff')),
            margin=dict(t=80, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Extract all items with category info
        menu = load_menu()
        
        # Create item to category mapping
        item_category = {}
        for category, items in menu.items():
            for item in items:
                item_category[item['name'].get('en', '')] = category
        
        # Get all items from orders
        all_items = []
        for _, row in df.iterrows():
            for item in row.get('items', []):
                item_name = item['name']
                all_items.append({
                    'name': item_name, 
                    'quantity': item['quantity'], 
                    'revenue': item['price'] * item['quantity'],
                    'category': item_category.get(item_name, 'Other')
                })
        
        if all_items:
            df_items = pd.DataFrame(all_items)
            
            # Overall Top Selling Items
            st.markdown(f"### {t('top_selling')} - Overall")
            top_items = df_items.groupby('name').agg({'quantity': 'sum', 'revenue': 'sum'}).reset_index()
            top_items = top_items.sort_values('quantity', ascending=False).head(10)
            
            fig = px.bar(top_items, x='name', y='quantity', 
                        color='revenue', 
                        color_continuous_scale=[[0, '#b8860b'], [0.5, '#d4af37'], [1, '#f7e98e']],
                        labels={'name': 'Item', 'quantity': 'Quantity Sold', 'revenue': 'Revenue'})
            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff', family='Inter, sans-serif'),
                title=dict(
                    text=f"<b>{t('top_selling')} - Overall</b>",
                    font=dict(color='#d4af37', size=20),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(tickfont=dict(color='#ffffff'), title_font=dict(color='#d4af37')),
                yaxis=dict(tickfont=dict(color='#ffffff'), title_font=dict(color='#d4af37')),
                coloraxis_colorbar=dict(tickfont=dict(color='#ffffff'), title_font=dict(color='#d4af37')),
                margin=dict(t=80, b=40, l=40, r=40)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Category-specific Top Sellers
            st.markdown(f"### {t('top_selling')} - By Category")
            
            categories_in_data = df_items['category'].unique()
            
            # Create columns for category charts
            if len(categories_in_data) > 0:
                cols = st.columns(min(len(categories_in_data), 3))
                
                for i, category in enumerate(categories_in_data):
                    if category != 'Other':
                        with cols[i % 3]:
                            st.markdown(f"**{category}**")
                            
                            cat_items = df_items[df_items['category'] == category]
                            cat_top = cat_items.groupby('name').agg({'quantity': 'sum'}).reset_index()
                            cat_top = cat_top.sort_values('quantity', ascending=True).tail(5)
                            
                            if not cat_top.empty:
                                fig = px.bar(cat_top, x='quantity', y='name', orientation='h',
                                            color='quantity',
                                            color_continuous_scale=[[0, '#b8860b'], [1, '#d4af37']])
                                fig.update_layout(
                                    height=300,
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    font=dict(color='#ffffff', family='Inter, sans-serif'),
                                    title=dict(
                                        text=f"<b>{category}</b>",
                                        font=dict(color='#d4af37', size=16),
                                        x=0.5,
                                        xanchor='center'
                                    ),
                                    xaxis=dict(showticklabels=True, tickfont=dict(color='#ffffff'), title=""),
                                    yaxis=dict(tickfont=dict(color='#ffffff'), title=""),
                                    coloraxis_showscale=False,
                                    margin=dict(l=10, r=10, t=50, b=20)
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("No data")
        
        # Export report
        st.divider()
        if st.button("📥 Download Analytics Report"):
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                pd.DataFrame({'Metric': [t('total_revenue'), t('total_orders'), t('avg_order')], 
                             'Value': [f"{total_revenue:.0f} SAR", total_orders, f"{avg_order:.0f} SAR"]}).to_excel(writer, sheet_name='Summary', index=False)
                if all_items:
                    top_items.to_excel(writer, sheet_name='Top Items', index=False)
            st.download_button("📥 Download", buffer.getvalue(), f"analytics_{datetime.now().strftime('%Y%m%d')}.xlsx")

# Footer
st.divider()
st.caption(f"🔐 {t('admin_panel')} | {t('restaurant_management')}")
