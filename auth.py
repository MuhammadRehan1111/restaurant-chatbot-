"""
Simple authentication utilities for the admin panel.
"""
import streamlit as st
import config


def check_password() -> bool:
    """
    Returns True if the user has entered the correct password.
    Uses Streamlit session state to track authentication.
    """
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (st.session_state.get("username") == config.ADMIN_USERNAME and 
            st.session_state.get("password") == config.ADMIN_PASSWORD):
            st.session_state["password_correct"] = True
            # Clear password from session state for security
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # First run or logged out
    if "password_correct" not in st.session_state:
        st.markdown("### 🔐 Admin Login")
        st.markdown('<p style="color: #ffffff; opacity: 0.9;">Please enter your credentials to access the admin panel.</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                password_entered()
        
        if st.session_state.get("password_correct") == False:
            st.error("😕 Invalid username or password")
        
        return False
    
    # Password correct
    elif st.session_state.get("password_correct"):
        return True
    
    # Password incorrect, show form again
    else:
        st.markdown("### 🔐 Admin Login")
        st.markdown('<p style="color: #ffffff; opacity: 0.9;">Please enter your credentials to access the admin panel.</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                password_entered()
        
        st.error("😕 Invalid username or password")
        return False


def logout():
    """Log out the current user."""
    if "password_correct" in st.session_state:
        del st.session_state["password_correct"]
    st.rerun()
