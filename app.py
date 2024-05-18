# ============================================================================
# -*- coding: utf-8 -*-
#
# Project:      Streamlit Application with Dynamic Page Loading
# Description:  This Streamlit application dynamically loads and displays
#               pages defined in the app_pages package. Each page must 
#               implement the BasePage abstract base class.
#
# Usage:        Run with 'streamlit run app.py' from the terminal.
#
# Virtual Environment Setup:
#   python3 -m venv venv
#   source venv/bin/activate
#   pip install --upgrade pip
#   pip install -r requirements.txt
#
# Required Packages:
#   altair==4.1.0
#   streamlit
#   watchdog
#   streamlit-js-eval
#   streamlit-option-menu
#
# VSCode Notes: Run with 'streamlit run app.py' from the terminal or press
#               Cmd+Shift+D to bring up the debugging interface.
#
# Useful Links:
#   https://icons.getbootstrap.com/
#
# History:
# 2024-05-18    urot  Created
# ============================================================================

import streamlit as st
from utilities import validate_session_state, dynamic_streamlit_menu

# Debug function to print all session state variables
def debug_session_state():
    st.sidebar.subheader("Debug Info")
    for key, value in st.session_state.items():
        st.sidebar.write(f"{key}: {value}")

# Main application logic
def event_handler():
    # Initialize necessary session state variables
    validate_session_state()

    selected_page, page_dict = dynamic_streamlit_menu(
        st.session_state.get("orientation", "vertical")
    )

    # Call the debug function to print session state variables
    #debug_session_state()

    page_dict[selected_page].show_page()

if __name__ == "__main__":
    event_handler()
