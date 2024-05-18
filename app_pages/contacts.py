import streamlit as st
from base_page import BasePage

class ContactsPage(BasePage):

    def show_page(self):
        st.title("Contact Page")
        st.write("This is the Contacts Page.")

    def label(self):
        return "Contacts"

    def icon(self):
        return "envelope"

    def order(self):
        return 2
