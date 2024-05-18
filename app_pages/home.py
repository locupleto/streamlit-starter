import streamlit as st

def show_page():
    st.title("Home Page")
    st.write("Welcome to the Home Page. This is the main dashboard of the application.")

# --- Mandatory functions for the menu to work properly ---

def label():
    return "Home"

def icon():
    return "house"

def order():
    return 1
