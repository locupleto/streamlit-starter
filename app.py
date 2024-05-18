# ============================================================================
# -*- coding: utf-8 -*-
#
# Description: Run with 'streamlit run app.py' from the terminal or 
# Press Cmd+Shift+D. This brings up the debugging interface on the top left
# where you can select and start your configuration.
#
# Extra requirements:
# pip install streamlit-option-menu
#
# Useful links
# https://icons.getbootstrap.com/
#
# History       Rev   Description
# 2024-05-13    urot  Created
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

    # Initialize necessary session state variables if they don't exist
    validate_session_state()
    selected, modules = \
        dynamic_streamlit_menu(orientation=st.session_state.orientation)
    
     # Call the debug function to print session state variables
    debug_session_state()

    # Update the session state on navigation
    if selected != st.session_state.previous_page:
        st.session_state.previous_page = selected

    # Display the selected page module
    page = modules[selected]
    page.show_page()

    # Debugging information
    if False:
        st.write(f"Initial orientation: {st.session_state.orientation}")
        st.write(f"Previous page: {st.session_state.previous_page}")
        st.write(f"Selected page: {selected}")
        st.write(f"Current theme: {st.session_state.theme}")
        st.write(f"Current orientation: {st.session_state.orientation}")

if __name__ == "__main__":
    event_handler()
