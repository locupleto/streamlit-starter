import streamlit as st
from base_page import BasePage

class HomePage(BasePage):

    def show_page(self):
        st.title("Home Page")
        st.write("Welcome to the Home Page. This is the main dashboard of the application.")

    def label(self):
        return "Home"

    def icon(self):
        return "house"

    def order(self):
        return 1
