"""
Customer Order Page - Premium Redesigned with 3 Main Tabs
Tabs: Chatbot (multilingual), Menu (with images), Deals
Dark luxury theme with gold accents.
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.database import (
    load_menu, get_active_deals, create_order, get_menu_item,
    load_categories, get_active_categories
)
from utils.gemini_client import RestaurantChatbot
import config

# Page configuration
st.set_page_config(
    page_title="Order Food - Restaurant",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(184, 134, 11, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(212, 175, 55, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .main-header h2 {
        font-family: 'Playfair Display', serif;
        color: #d4af37;
        margin: 0;
        font-size: 2rem;
    }
    
    .table-badge {
        display: inline-block;
        background: linear-gradient(135deg, #d4af37, #b8860b);
        color: #0a0a0f;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        margin-top: 0.75rem;
    }
    
    /* Category cards with images */
    .category-card {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.9) 0%, rgba(15, 15, 26, 0.95) 100%);
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid rgba(212, 175, 55, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
        padding: 1rem;
    }
    
    .category-card:hover {
        border-color: rgba(212, 175, 55, 0.6);
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .category-card.selected {
        border-color: #d4af37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }
    
    .category-image {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 0.5rem;
        border: 2px solid rgba(212, 175, 55, 0.3);
    }
    
    .category-name {
        font-family: 'Playfair Display', serif;
        color: #d4af37; /* Golden color */
        font-size: 0.95rem;
        margin: 0;
        font-weight: 600;
    }
    
    /* Menu item cards */
    .menu-card {
        background: linear-gradient(145deg, rgba(26, 26, 46, 0.9) 0%, rgba(15, 15, 26, 0.95) 100%);
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(212, 175, 55, 0.2);
        transition: all 0.3s ease;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }
    
    .menu-card:hover {
        transform: translateY(-5px);
        border-color: rgba(212, 175, 55, 0.5);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4);
    }
    
    .menu-image {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    
    .menu-info {
        padding: 1.25rem;
    }
    
    .menu-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        color: #d4af37; /* Golden color */
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .menu-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #ffffff; /* White text */
        margin-bottom: 0.75rem;
    }
    
    .menu-price {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: #d4af37;
        font-weight: 600;
    }
    
    /* Deal cards */
    .deal-card {
        background: linear-gradient(145deg, rgba(212, 175, 55, 0.15) 0%, rgba(184, 134, 11, 0.1) 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .deal-badge {
        display: inline-block;
        background: linear-gradient(135deg, #d4af37, #b8860b);
        color: #0a0a0f;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .deal-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        background: linear-gradient(135deg, #d4af37 0%, #f7e98e 50%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .deal-desc {
        font-family: 'Inter', sans-serif;
        color: #ffffff; /* White text */
        margin-bottom: 1rem;
    }
    
    /* Cart styling */
    .cart-header {
        font-family: 'Playfair Display', serif;
        color: #d4af37;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    
    .cart-item {
        background: rgba(26, 26, 46, 0.8);
        padding: 0.75rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid rgba(212, 175, 55, 0.1);
    }
    
    .cart-total {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #d4af37;
        text-align: right;
        padding: 1rem 0;
        border-top: 1px solid rgba(212, 175, 55, 0.2);
        margin-top: 1rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(26, 26, 46, 0.5);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 10px;
        color: #ffffff; /* White text */
        font-family: 'Inter', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(184, 134, 11, 0.1));
        color: #d4af37;
    }
    
    /* Chat styling */
    .stChatMessage {
        background: #ffffff !important;
        border: 1px solid rgba(212, 175, 55, 0.5) !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        color: #1a1a2e !important; /* Dark text for readability on white */
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(184, 134, 11, 0.1)) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        color: #d4af37 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.3), rgba(184, 134, 11, 0.2)) !important;
        border-color: rgba(212, 175, 55, 0.6) !important;
        transform: translateY(-2px);
    }
    
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #d4af37, #b8860b) !important;
        color: #0a0a0f !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    /* Section header */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        background: linear-gradient(135deg, #d4af37 0%, #f7e98e 50%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    /* Footer */
    .premium-footer {
        text-align: center;
        padding: 1.5rem;
        color: #ffffff; /* White text */
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        border-top: 1px solid rgba(212, 175, 55, 0.1);
        margin-top: 2rem;
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
</style>
""", unsafe_allow_html=True)

# Get table_id from URL parameters
query_params = st.query_params
table_id = query_params.get("table_id", None)

# Validate table_id
if table_id is None:
    st.markdown("""
    <div class="main-header">
        <h2>🍽️ Welcome to Our Restaurant</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.error("⚠️ No table detected!")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(212, 175, 55, 0.05); border-radius: 15px; border: 1px solid rgba(212, 175, 55, 0.1); margin-bottom: 2rem;">
        <h3 style="color: #d4af37; font-family: 'Playfair Display', serif; margin-bottom: 0.5rem;">How to Order</h3>
        <p style="color: #ffffff; font-family: 'Inter', sans-serif; font-size: 1.1rem; margin-bottom: 1.5rem;">Please scan the QR code at your table to start ordering.</p>
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent); margin: 1.5rem 0;"></div>
        <p style="color: #d4af37; font-weight: 600; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">For Demo/Testing:</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p style="color: #d4af37; font-weight: 600; margin-bottom: -15px;">Enter table number:</p>', unsafe_allow_html=True)
    demo_table = st.number_input("Enter table number:", min_value=1, max_value=50, value=1, label_visibility="collapsed")
    if st.button("Start Ordering", type="primary"):
        st.query_params["table_id"] = str(demo_table)
        st.rerun()
    st.stop()

try:
    table_id = int(table_id)
except ValueError:
    st.error("Invalid table ID. Please scan the QR code again.")
    st.stop()

# Header
st.markdown(f"""
<div class="main-header">
    <h2>🍽️ Welcome to Our Restaurant</h2>
    <div class="table-badge">Table {table_id}</div>
</div>
""", unsafe_allow_html=True)

# Initialize session state - Clear chat for new sessions
if 'session_initialized' not in st.session_state:
    # This is a new session - clear everything
    st.session_state.session_initialized = True
    st.session_state.cart_items = []
    st.session_state.chat_messages = []
    st.session_state.chatbot = None
    st.session_state.order_submitted = False
    st.session_state.last_order = None
    st.session_state.cart_version = 0

if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

if 'cart_version' not in st.session_state:
    st.session_state.cart_version = 0

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

if 'chatbot' not in st.session_state or st.session_state.chatbot is None:
    menu = load_menu()
    deals = get_active_deals()
    st.session_state.chatbot = RestaurantChatbot(table_id, menu, deals)
    welcome = st.session_state.chatbot.get_welcome_message()
    st.session_state.chat_messages = [{"role": "assistant", "content": welcome}]

if 'order_submitted' not in st.session_state:
    st.session_state.order_submitted = False

if 'last_order' not in st.session_state:
    st.session_state.last_order = None

# Load data
menu = load_menu()
deals = get_active_deals()
categories = get_active_categories()

# Helper function to add item to cart
def add_to_cart(item_id: str, name: str, price: float, quantity: int = 1):
    # Check if item already exists in cart
    for i, item in enumerate(st.session_state.cart_items):
        if item['item_id'] == item_id:
            item['quantity'] += quantity
            new_qty = item['quantity']
            
            # Increment version to force widget refresh
            st.session_state.cart_version += 1
                
            # Trigger state update explicitly
            st.session_state.cart_items = st.session_state.cart_items
            return new_qty
            
    # If not found, add new
    st.session_state.cart_items.append({
        "item_id": item_id,
        "name": name,
        "price": round(float(price), 2),
        "quantity": quantity
    })
    st.session_state.cart_version += 1
    return quantity

# Helper function to calculate cart total
def get_cart_total():
    return sum(item['price'] * item['quantity'] for item in st.session_state.cart_items)

# Helper function to format bill
def format_bill(items, total):
    bill = "```\n"
    bill += "=" * 40 + "\n"
    bill += "           ORDER RECEIPT\n"
    bill += "=" * 40 + "\n"
    bill += f"Table: {table_id}\n"
    bill += "-" * 40 + "\n"
    bill += f"{'Item':<20} {'Qty':>3} {'Price':>12}\n"
    bill += "-" * 40 + "\n"
    for item in items:
        subtotal = item['price'] * item['quantity']
        # Truncate or pad
        name = item['name'][:20]
        bill += f"{name:<20} {item['quantity']:>3} {subtotal:>12.2f} SAR\n"
    bill += "-" * 40 + "\n"
    bill += f"{'TOTAL':<20} {'':>3} {total:>12.2f} SAR\n"
    bill += "=" * 40 + "\n"
    bill += "```"
    return bill

# Sidebar - Cart
with st.sidebar:
    st.markdown('<p class="cart-header">🛒 Your Order</p>', unsafe_allow_html=True)
    
    if st.session_state.order_submitted and st.session_state.last_order:
        st.success("✅ Order Submitted!")
        order = st.session_state.last_order
        st.markdown(f"**Order #{order['order_id']}**")
        st.markdown(format_bill(order['items'], order['total_price']))
        st.markdown("""
        <div style="background: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
            <p style="color: #d4af37; font-weight: 600; margin: 0;">✨ Please proceed to cashier for payment. ✨</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("New Order", type="primary", use_container_width=True):
            st.session_state.cart_items = []
            st.session_state.order_submitted = False
            st.session_state.last_order = None
            st.rerun()
    
    elif not st.session_state.cart_items:
        st.markdown("""
        <div style="background: rgba(212, 175, 55, 0.1); border: 2px solid #d4af37; padding: 1.5rem; border-radius: 15px; text-align: center; margin: 1rem 0; box-shadow: 0 0 20px rgba(212, 175, 55, 0.15);">
            <p style="color: #ffffff; font-size: 1.1rem; margin: 0;">Your cart is empty.</p>
            <p style="color: #d4af37; font-weight: 700; font-size: 1.2rem; margin: 0.75rem 0 0 0; text-transform: uppercase; letter-spacing: 1px;">✨ Add items from the menu! ✨</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        for i, item in enumerate(st.session_state.cart_items):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{item['name']}**")
                st.caption(f"{item['price']} SAR each")
            with col2:
                new_qty = st.number_input(
                    "Qty", 
                    min_value=0, 
                    max_value=10, 
                    value=item['quantity'],
                    key=f"cart_qty_{item['item_id']}_{i}_v{st.session_state.get('cart_version', 0)}",
                    label_visibility="collapsed"
                )
                if new_qty != item['quantity']:
                    if new_qty == 0:
                        st.session_state.cart_items.pop(i)
                        st.rerun()
                    else:
                        item['quantity'] = new_qty
                        st.rerun()
            with col3:
                subtotal = item['price'] * item['quantity']
                st.markdown(f"**{subtotal:.2f}**")
            st.divider()
        
        # Total
        total = get_cart_total()
        st.markdown(f'<p class="cart-total">Total: {total:.0f} SAR</p>', unsafe_allow_html=True)
        
        # Submit Order
        if st.button("✅ Confirm Order", type="primary", use_container_width=True):
            order = create_order(
                table_id=table_id,
                items=st.session_state.cart_items,
                total_price=total
            )
            st.session_state.order_submitted = True
            st.session_state.last_order = order
            st.session_state.cart_items = []
            st.rerun()
        
        if st.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart_items = []
            st.rerun()

# Main content - Three tabs
tab1, tab2, tab3 = st.tabs(["🤖 Chatbot", "📋 Menu", "🎁 Deals"])

# =============================================================================
# TAB 1: CHATBOT (Multilingual)
# =============================================================================
with tab1:
    st.markdown('<p class="section-header">💬 Chat with our AI Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #ffffff; font-size: 0.9rem;">Supports English • اردو • العربية</p>', unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container(height=400)
    with chat_container:
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message... / اپنا پیغام لکھیں / اكتب رسالتك"):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Get chatbot response
        with st.spinner("..."):
            response = st.session_state.chatbot.send_message(prompt)
        
        # Parse for hidden order tags: [ORDER: item_id, quantity]
        import re
        order_tags = re.findall(r'\[ORDER:\s*([^,]+),\s*(\d+)\]', response)
        
        # Process orders if found
        items_added = []
        if order_tags:
            for item_id, qty in order_tags:
                try:
                    # Clean the ID (remove potential whitespace) and parse qty
                    item_id = item_id.strip() 
                    qty = int(qty)
                    
                    # We need to fetch the item details to add it
                    # Try menu first
                    item_details = get_menu_item(item_id)
                    if item_details:
                        name = item_details['name'].get('en', 'Unknown')
                        price = item_details['price']
                        add_to_cart(item_id, name, price, qty)
                        items_added.append(f"{qty}x {name}")
                except Exception as e:
                    print(f"Error processing tag: {e}")
            
            # Clean response text (remove tags)
            response = re.sub(r'\[ORDER:.*?\]', '', response).strip()
            
            if items_added:
                st.toast(f"Added to cart: {', '.join(items_added)} 🛒", icon="✅")
                # Add a visible reminder to confirm logic
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": "✅ **Items added to cart!** Please review your order in the sidebar and click **'Confirm Order'** to send it to the kitchen."
                })
        
        # Add assistant response
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Quick actions
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Show Menu", use_container_width=True):
            st.session_state.chat_messages.append({"role": "user", "content": "Show me the menu"})
            response = st.session_state.chatbot.send_message("Show me the full menu with prices")
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("🎁 View Deals", use_container_width=True):
            st.session_state.chat_messages.append({"role": "user", "content": "What deals are available?"})
            response = st.session_state.chatbot.send_message("What deals and offers do you have?")
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("🛒 View Cart", use_container_width=True):
            if st.session_state.cart_items:
                bill = format_bill(st.session_state.cart_items, get_cart_total())
                st.session_state.chat_messages.append({"role": "assistant", "content": f"Here's your current order:\n\n{bill}"})
            else:
                st.session_state.chat_messages.append({"role": "assistant", "content": "Your cart is empty. Would you like to see the menu?"})
            st.rerun()
    
    with col4:
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.chat_messages = []
            menu = load_menu()
            deals = get_active_deals()
            st.session_state.chatbot = RestaurantChatbot(table_id, menu, deals)
            welcome = st.session_state.chatbot.get_welcome_message()
            st.session_state.chat_messages.append({"role": "assistant", "content": welcome})
            st.rerun()

# =============================================================================
# TAB 2: MENU (with images)
# =============================================================================
with tab2:
    st.markdown('<p class="section-header">📋 Our Menu</p>', unsafe_allow_html=True)
    
    # Category selection
    if 'selected_menu_category' not in st.session_state:
        st.session_state.selected_menu_category = None
    
    # Display category buttons with images
    st.markdown("**Select a Category:**")
    cols = st.columns(len(categories) if categories else 5)
    
    # Category images mapping (using food images for categories)
    category_images = {
        "Fast Food": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200",
        "Pizza": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=200",
        "Meat & BBQ": "https://images.unsplash.com/photo-1544025162-d76694265947?w=200",
        "Tea": "https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=200",
        "Ice Cream": "https://images.unsplash.com/photo-1570197571499-166b36435e9f?w=200",
        "naan": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=200"
    }
    
    for i, cat in enumerate(categories):
        with cols[i % len(cols)]:
            cat_image = cat.get('image', category_images.get(cat['name'], 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=200'))
            is_selected = st.session_state.selected_menu_category == cat['name']
            
            # Category Card HTML
            st.markdown(f"""
            <div class="category-card {'selected' if is_selected else ''}">
                <img src="{cat_image}" class="category-image" onerror="this.src='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=200'">
                <p class="category-name">{cat['name']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Invisible button for selection
            if st.button(
                f"Select {cat['name']}", 
                key=f"cat_btn_{cat['id']}",
                use_container_width=True
            ):
                st.session_state.selected_menu_category = cat['name']
                st.rerun()
    
    st.divider()
    
    # Display menu items
    if st.session_state.selected_menu_category and st.session_state.selected_menu_category in menu:
        items = menu[st.session_state.selected_menu_category]
        available_items = [item for item in items if item.get('available', True)]
        
        # Display in grid (3 columns)
        cols = st.columns(3)
        for i, item in enumerate(available_items):
            with cols[i % 3]:
                # Image
                image_url = item.get('image', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400')
                
                # Item details
                name = item['name'].get('en', 'Unknown')
                desc = item.get('description', {}).get('en', '')
                price = item['price']
                
                st.markdown(f"""
                <div class="menu-card">
                    <img src="{image_url}" class="menu-image" alt="{name}" onerror="this.src='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400'">
                    <div class="menu-info">
                        <div class="menu-name">{name}</div>
                        <div class="menu-desc">{desc[:60] + '...' if len(desc) > 60 else desc}</div>
                        <div class="menu-price">{price} SAR</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add to cart button with unique key
                if st.button(f"➕ Add to Cart", key=f"add_{item['item_id']}_{i}", use_container_width=True):
                    new_qty = add_to_cart(item['item_id'], name, price)
                    st.toast(f"Added {name} (Qty: {new_qty})! ✨", icon="✅")
                    st.rerun()
    else:
        st.info("👆 Select a category above to view items")

# =============================================================================
# TAB 3: DEALS
# =============================================================================
with tab3:
    st.markdown('<p class="section-header">🎁 Special Deals & Offers</p>', unsafe_allow_html=True)
    
    if not deals:
        st.info("No active deals at the moment. Check back later!")
    else:
        for deal in deals:
            if deal.get('active', False):
                name = deal['name'].get('en', 'Special Deal')
                desc = deal.get('description', {}).get('en', '')
                discount = deal.get('discount_percent', 0)
                deal_image = deal.get('image', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600')
                
                applicable = deal.get('applicable_items', [])
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(deal_image, use_container_width=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="deal-card">
                        <div class="deal-badge">{discount}% OFF</div>
                        <h3 class="deal-name">{name}</h3>
                        <p class="deal-desc">{desc}</p>
                        <div style="margin-top: 1rem;">
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🛍️ Order Full Deal", key=f"full_deal_{deal['deal_id']}", type="primary", use_container_width=True):
                        added_any = False
                        for item_id in applicable:
                            item = get_menu_item(item_id)
                            if item:
                                discounted_price = round(item['price'] * (1 - discount / 100), 2)
                                add_to_cart(f"{item_id}_deal_{deal['deal_id']}", f"{item['name'].get('en', 'Item')} (Deal)", discounted_price)
                                added_any = True
                        if added_any:
                            st.toast(f"Full Deal '{name}' added to cart! 🎁", icon="✅")
                            st.rerun()
                    
                    st.markdown("""
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()

# Footer
st.markdown(f"""
<div class="premium-footer">
    🍽️ Table {table_id} | Need help? Use the Chatbot!
</div>
""", unsafe_allow_html=True)
