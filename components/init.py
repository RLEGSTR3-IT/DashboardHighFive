"""
Dashboard High Five Components Package

Modular components untuk Dashboard Monitoring High Five Telkom Indonesia
"""

__version__ = "1.0.0"
__author__ = "Telkom Indonesia"

# Import all components for easier access
from .layout import setup_page_config, apply_custom_css
from .sidebar import render_sidebar
from .viz_piechart import render_astinet_visualization
from .viz_other import render_other_visualization

__all__ = [
    'setup_page_config',
    'apply_custom_css',
    'render_sidebar',
    'render_astinet_visualization',
    'render_other_visualization'
]