import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

# Project information
project = "yaml2pydantic"
copyright = f"{datetime.now().year}, Your Name"
author = "Your Name"

# The full version, including alpha/beta/rc tags
release = "0.1.0"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
]

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}

# Intersphinx settings
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# MyST settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "tasklist",
]

# HTML theme settings
html_theme = "furo"
html_theme_options = {
    "navigation_with_keys": True,
    "source_repository": "https://github.com/yourusername/yaml2pydantic/",
    "source_branch": "main",
    "source_directory": "docs/",
}

# Static files
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Copy button settings
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Add README.md to the documentation
myst_include_patterns = ["README.md"]
