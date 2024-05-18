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
