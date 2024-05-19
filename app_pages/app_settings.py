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

        # Use st.form to group input elements
        with st.form(key="settings_form"):
            # Display and edit each section in the app configuration
            for section, settings in app_config.items():
                if section != "streamlit-option-menu":
                    st.subheader(section)
                    for key, value in settings.items():
                        new_value = st.text_input(f"{section} - {key}", value)
                        if new_value != value:
                            app_config[section][key] = new_value
            
            # Submit button for the form
            submit_button = st.form_submit_button(label="Save Settings")

        # Save the updated configuration when the form is submitted
        if submit_button:
            with open(APP_CONFIG_PATH, "w") as f:
                toml.dump(app_config, f)
            st.experimental_rerun()

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
