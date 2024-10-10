"""Sphinx configuration."""

project = "django-owm"
author = "Jack Linke"
copyright = "2024, Jack Linke"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
