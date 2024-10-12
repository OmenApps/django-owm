"""Sphinx configuration."""

import inspect
import os
import sys

import django
from django.utils.html import strip_tags


sys.path.insert(0, os.path.abspath(".."))
os.environ["DJANGO_SETTINGS_MODULE"] = "example_project.settings"
django.setup()

project = "django-owm"
author = "Jack Linke"
copyright = "2024, Jack Linke"
extensions = [
    "celery.contrib.sphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
autodoc_default_options = {
    "members": True,
    "special-members": "__init__",
    "exclude-members": "__weakref__,Meta",
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": ("https://docs.djangoproject.com/en/stable/", "https://docs.djangoproject.com/en/stable/_objects/"),
}


def project_django_models(app, what, name, obj, options, lines):  # pylint: disable=W0613 disable=R0913
    """Process Django models for autodoc.

    From: https://djangosnippets.org/snippets/2533/
    """
    from django.db import models  # pylint: disable=C0415

    # Only look at objects that inherit from Django's base model class
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        # Grab the field list from the meta class
        fields = obj._meta.get_fields()  # pylint: disable=W0212

        for field in fields:
            # Decode and strip any html out of the field's help text
            help_text = strip_tags(field.help_text)

            # Decode and capitalize the verbose name, for use if there isn't
            # any help text
            verbose_name = field.verbose_name

            if help_text:
                # Add the model field to the end of the docstring as a param
                # using the help text as the description
                lines.append(f":param {field.attname}: {help_text}")
            else:
                # Add the model field to the end of the docstring as a param
                # using the verbose name as the description
                lines.append(f":param {field.attname}: {verbose_name}")

            # Add the field's type to the docstring
            lines.append(f":type {field.attname}: {field.__class__.__name__}")

    # Return the extended docstring
    return lines


def setup(app):
    """Register the Django model processor with Sphinx."""
    app.connect("autodoc-process-docstring", project_django_models)
