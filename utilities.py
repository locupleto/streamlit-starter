# ============================================================================
# -*- coding: utf-8 -*-
#
# Module: Utilities
# Description: Contains utility functions for loading modules dynamically,
#              managing configurations, and applying theme settings.
#
# History:
# 2024-05-18    urot  Created
# ============================================================================

import os
import importlib
from time import sleep
import streamlit as st
from streamlit_option_menu import option_menu
import toml
from base_page import BasePage

# File path for the Streamlit configuration
CONFIG_PATH = ".streamlit/config.toml"

# Default themes
default_light_theme = {
    "theme": {
        "base": "light",
        "primaryColor": "#F63366",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730",
        "font": "sans serif"
    }
}

default_dark_theme = {
    "theme": {
        "base": "dark",
        "primaryColor": "#F63366",
        "backgroundColor": "#262730",
        "secondaryBackgroundColor": "#1A1A1A",
        "textColor": "#FFFFFF",
        "font": "sans serif"
    }
}

# Determine theme status
def determine_theme_status(theme):
    if theme == default_dark_theme["theme"]:
        return "dark"
    elif theme == default_light_theme["theme"]:
        return "light"
    else:
        return "custom"

# Create a default config file if it doesn't exist
def create_default_config():
    default_config = {
        "theme": default_dark_theme["theme"],  # Default to dark theme
        "extras": {
            "orientation": "vertical"  # Default orientation
        }
    }
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        toml.dump(default_config, f)

# Apply theme settings immediately
def apply_theme_settings(theme):
    st.config.set_option('theme.base', theme.get('base', 'light'))
    st.config.set_option('theme.primaryColor', theme.get('primaryColor', '#F63366'))
    st.config.set_option('theme.backgroundColor', theme.get('backgroundColor', '#FFFFFF'))
    st.config.set_option('theme.secondaryBackgroundColor', theme.get('secondaryBackgroundColor', '#F0F2F6'))
    st.config.set_option('theme.textColor', theme.get('textColor', '#262730'))
    # Apply custom font via CSS
    font_css = f"""
    <style>
    body {{
        font-family: {theme.get('font', 'sans serif')}, sans-serif;
    }}
    </style>
    """
    st.markdown(font_css, unsafe_allow_html=True)

# Load current config values from .streamlit/config.toml if it exists
def load_config():
    if not os.path.exists(CONFIG_PATH):
        create_default_config()
    
    config = toml.load(CONFIG_PATH)
    theme = config.get("theme", {})
    base = theme.get("base", "light")
    defaults = default_dark_theme if base == "dark" else default_light_theme
    for key, value in defaults["theme"].items():
        theme.setdefault(key, value)
    config["theme"] = theme

    extras = config.get("extras", {})
    orientation = extras.get("orientation", "vertical")

    st.session_state.theme = theme
    st.session_state.theme_status = determine_theme_status(theme)
    st.session_state.orientation = orientation
    apply_theme_settings(theme)  # Apply theme settings immediately

# Ensure necessary session state variables are initialized
def validate_session_state():
    if "previous_page" not in st.session_state:
        st.session_state.previous_page = "Home"
    
    load_config()

# Save configuration to file and update session state
def save_config(theme=None, orientation=None):
    st.session_state.theme = theme
    st.session_state.orientation = orientation
    st.session_state.theme_status = determine_theme_status(theme)

    config = {
        "theme": theme,
        "extras": {
            "orientation": orientation
        }
    }

    with open(CONFIG_PATH, "w") as f:
        toml.dump(config, f)

    apply_theme_settings(theme)  # Apply theme settings immediately
    st.experimental_rerun()  # Re-run the app to apply the new config file

@st.cache(allow_output_mutation=True)   
def load_modules():
    # Function to dynamically load modules from the app_pages directory
    pages_path = "./app_pages"
    modules = []
    for filename in os.listdir(pages_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module_path = f"app_pages.{module_name}"
            module = importlib.import_module(module_path)
            # Find the class that inherits from BasePage and create an instance
            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, BasePage) and obj is not BasePage:
                    modules.append((module_name, obj()))
                    break
    return modules

# Function to dynamically create menu options from loaded modules
def dynamic_streamlit_menu(orientation="vertical"):
    modules = load_modules()
    modules.sort(key=lambda x: x[1].order())

    options = [mod[1].label() for mod in modules]
    icons = [mod[1].icon() for mod in modules]

    if orientation == "vertical":
        with st.sidebar:
            selected = option_menu(
                menu_title=None,
                options=options,
                icons=icons,
                menu_icon="cast",
                default_index=0
            )
    else:
        selected = option_menu(
            menu_title=None,
            options=options,
            icons=icons,
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )

    return selected, {mod[1].label(): mod[1] for mod in modules}
