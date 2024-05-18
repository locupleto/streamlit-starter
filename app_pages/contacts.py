import streamlit as st

def show_page():
    st.title("Contact Page")
    st.write("This is the Contacts Page.")

# --- Mandatory functions for the menu to work properly ---

def label():
    return "Contacts"

def icon():
    return "envelope"

def order():
    return 2
