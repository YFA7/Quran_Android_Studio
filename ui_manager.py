"""
UI Manager Module
Handles UI styling, themes, and component management
"""

import tkinter as tk
from tkinter import ttk
from enum import Enum
from typing import Dict


class Theme(Enum):
    """Application themes"""
    LIGHT = "light"
    DARK = "dark"
    SEPIA = "sepia"


class UIManager:
    """Manages UI styling and appearance"""
    
    # Color schemes
    THEMES: Dict[Theme, Dict[str, str]] = {
        Theme.LIGHT: {
            "bg": "#f5f5dc",
            "fg": "#2c3e50",
            "button_bg": "#ecf0f1",
            "button_fg": "#2c3e50",
            "accent": "#3498db",
            "border": "#bdc3c7",
        },
        Theme.DARK: {
            "bg": "#2c3e50",
            "fg": "#ecf0f1",
            "button_bg": "#34495e",
            "button_fg": "#ecf0f1",
            "accent": "#3498db",
            "border": "#7f8c8d",
        },
        Theme.SEPIA: {
            "bg": "#f4ebd9",
            "fg": "#5c4033",
            "button_bg": "#d7ccc8",
            "button_fg": "#5c4033",
            "accent": "#8d6e63",
            "border": "#a1887f",
        }
    }
    
    def __init__(self, root, theme=Theme.LIGHT):
        self.root = root
        self.current_theme = theme
        self.apply_theme(theme)
    
    def apply_theme(self, theme: Theme):
        """Apply a theme to the application"""
        self.current_theme = theme
        colors = self.THEMES[theme]
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure(
            'TButton',
            background=colors['button_bg'],
            foreground=colors['button_fg'],
            borderwidth=1,
            focuscolor='none',
            padding=5
        )
        
        # Configure label style
        style.configure(
            'TLabel',
            background=colors['bg'],
            foreground=colors['fg']
        )
        
        # Configure frame style
        style.configure(
            'TFrame',
            background=colors['bg']
        )
        
        self.root.configure(bg=colors['bg'])
    
    @staticmethod
    def create_styled_button(parent, text, command, style="primary"):
        """Create a styled button"""
        btn = ttk.Button(parent, text=text, command=command)
        return btn
    
    @staticmethod
    def create_styled_label(parent, text, size="normal", bold=False):
        """Create a styled label"""
        font_size = {"small": 10, "normal": 12, "large": 14, "xlarge": 24}
        weight = "bold" if bold else "normal"
        label = tk.Label(
            parent,
            text=text,
            font=("Arial", font_size.get(size, 12), weight)
        )
        return label


class FontConfig:
    """Font configuration for the application"""
    
    FONTS = {
        "title": ("Arial", 28, "bold"),
        "heading": ("Arial", 16, "bold"),
        "normal": ("Arial", 12),
        "small": ("Arial", 10),
        "arabic_large": ("Traditional Arabic", 24, "bold"),
        "arabic_normal": ("Traditional Arabic", 14),
        "mono": ("Courier New", 10),
    }
    
    @staticmethod
    def get_font(font_name):
        """Get a configured font"""
        return FontConfig.FONTS.get(font_name, ("Arial", 12))
