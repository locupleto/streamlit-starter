import streamlit as st
from base_page import BasePage
from utilities import save_config, default_light_theme, default_dark_theme

class SettingsPage(BasePage):

    def show_page(self):
        st.title("Settings Page")

        # Ensure theme status is correctly determined
        if "theme_status" not in st.session_state:
            st.session_state.theme_status = "light" if st.session_state.theme == default_light_theme["theme"] else "dark"

        # Theme selection
        theme_status = st.selectbox(
            "Select Theme",
            options=["light", "dark", "custom"],
            index=["light", "dark", "custom"].index(st.session_state.get("theme_status", "light"))
        )

        # Menu orientation selection
        orientation = st.selectbox(
            "Select Menu Orientation",
            options=["vertical", "horizontal"],
            index=0 if st.session_state.get("orientation", "vertical") == "vertical" else 1
        )

        # Disable color and font pickers if the theme is not custom
        is_custom_theme = theme_status == "custom"

        primaryColor = st.color_picker("Primary Color", st.session_state.theme["primaryColor"], disabled=not is_custom_theme)
        backgroundColor = st.color_picker("Background Color", st.session_state.theme["backgroundColor"], disabled=not is_custom_theme)
        secondaryBackgroundColor = st.color_picker("Secondary Background Color", st.session_state.theme["secondaryBackgroundColor"], disabled=not is_custom_theme)
        textColor = st.color_picker("Text Color", st.session_state.theme["textColor"], disabled=not is_custom_theme)
        font = st.selectbox(
            "Select Font",
            options=["sans serif", "serif", "monospace"],
            index=["sans serif", "serif", "monospace"].index(st.session_state.theme["font"]),
            disabled=not is_custom_theme
        )

        if st.button("Apply Settings"):
            if theme_status == "dark":
                theme = default_dark_theme["theme"]
            elif theme_status == "light":
                theme = default_light_theme["theme"]
            else:
                theme = {
                    "base": st.session_state.theme["base"],
                    "primaryColor": primaryColor,
                    "backgroundColor": backgroundColor,
                    "secondaryBackgroundColor": secondaryBackgroundColor,
                    "textColor": textColor,
                    "font": font
                }

            save_config(theme, orientation)
            st.experimental_rerun()

    def label(self):
        return "Settings"

    def icon(self):
        return "gear"

    def order(self):
        return 3
