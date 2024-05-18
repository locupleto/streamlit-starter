# ============================================================================
# -*- coding: utf-8 -*-
#
# Module:       Application Settings Page
# Description:  Implements the AppSettingsPage class that inherits from 
#               BasePage and defines the content and properties for the 
#               application settings page. This page allows users to edit all 
#               existing sections and settings in the app_config.toml file.
# Useful Links:
#   https://icons.getbootstrap.com/
#
# History:
# 2024-05-18    urot  Created
# ============================================================================

import os
import streamlit as st
from base_page import BasePage
import toml

APP_CONFIG_PATH = "app_config.toml"

class AppSettingsPage(BasePage):

    def show_page(self):
        st.title("Application Settings")

        # Load current app configuration
        if not os.path.exists(APP_CONFIG_PATH):
            self.create_default_app_config()

        app_config = toml.load(APP_CONFIG_PATH)

        # Display and edit each section in the app configuration
        for section, settings in app_config.items():
            if section != "streamlit-option-menu":
                st.subheader(section)
                for key, value in settings.items():
                    new_value = st.text_input(f"{section} - {key}", value)
                    if new_value != value:
                        app_config[section][key] = new_value

        # Save the updated configuration
        if st.button("Save Settings"):
            with open(APP_CONFIG_PATH, "w") as f:
                toml.dump(app_config, f)
            st.rerun()

    def create_default_app_config(self):
        default_app_config = {
            "example-section": {
                "example-key": "example-value"
            }
        }
        with open(APP_CONFIG_PATH, "w") as f:
            toml.dump(default_app_config, f)

    def label(self):
        return "App Settings"

    def icon(self):
        return "sliders"

    def order(self):
        return 4
