# ============================================================================
# -*- coding: utf-8 -*-
#
# Module:       Utilities
# Description:  Contains utility functions for loading modules dynamically,
#               managing configurations, and applying theme settings.
#               Custom configuration settings are stored in a separate
#               app_config.toml file to avoid conflicts with Streamlit's
#               internal configuration handling.
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

# File paths for the configurations
STREAMLIT_CONFIG_PATH = ".streamlit/config.toml"
APP_CONFIG_PATH = "app_config.toml"

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

# Create default config files if they don't exist
def create_default_configs():
    default_streamlit_config = {
        "theme": default_dark_theme["theme"],  # Default to dark theme
    }
    os.makedirs(os.path.dirname(STREAMLIT_CONFIG_PATH), exist_ok=True)
    with open(STREAMLIT_CONFIG_PATH, "w") as f:
        toml.dump(default_streamlit_config, f)

    default_app_config = {
        "example-section": {
            "example-key": "example-value"
        },
        "streamlit-option-menu": {
            "orientation": "vertical",  # Default orientation
            "wide_mode": False  # Default to not wide mode
        }
    }
    with open(APP_CONFIG_PATH, "w") as f:
        toml.dump(default_app_config, f)

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

# Load current config values from configuration files if they exist
def load_config():
    if not os.path.exists(STREAMLIT_CONFIG_PATH) or not os.path.exists(APP_CONFIG_PATH):
        create_default_configs()
    
    config = toml.load(STREAMLIT_CONFIG_PATH)
    theme = config.get("theme", {})
    base = theme.get("base", "light")
    defaults = default_dark_theme if base == "dark" else default_light_theme
    for key, value in defaults["theme"].items():
        theme.setdefault(key, value)
    config["theme"] = theme

    app_config = toml.load(APP_CONFIG_PATH)
    extras = app_config.get("streamlit-option-menu", {})
    orientation = extras.get("orientation", "vertical")
    wide_mode = extras.get("wide_mode", False)

    st.session_state.theme = theme
    st.session_state.theme_status = determine_theme_status(theme)
    st.session_state.orientation = orientation
    st.session_state.wide_mode = wide_mode

# Ensure necessary session state variables are initialized
def validate_session_state():
    if "previous_page" not in st.session_state:
        st.session_state.previous_page = "Home"
    
    load_config()

# Save configuration to files and update session state
def save_config(theme=None, orientation=None, wide_mode=False):
    st.session_state.theme = theme
    st.session_state.orientation = orientation
    st.session_state.wide_mode = wide_mode
    st.session_state.theme_status = determine_theme_status(theme)

    streamlit_config = {
        "theme": theme,
    }

    app_config = toml.load(APP_CONFIG_PATH)
    app_config["streamlit-option-menu"] = {
        "orientation": orientation,
        "wide_mode": wide_mode
    }

    with open(STREAMLIT_CONFIG_PATH, "w") as f:
        toml.dump(streamlit_config, f)

    with open(APP_CONFIG_PATH, "w") as f:
        toml.dump(app_config, f)
    sleep(0.5)
    st.rerun()  # Re-run the app to apply the new config files

@st.cache_resource 
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
