# ============================================================================
# -*- coding: utf-8 -*-
#
# Module: Contacts Page
# Description: Implements the ContactsPage class that inherits from BasePage
#              and defines the content and properties for the contacts page.
#
# Useful Links:
#   https://icons.getbootstrap.com/
#
# History:
# 2024-05-18    urot  Created
# ============================================================================

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
