# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Speech Emotion Recognition'
copyright = '2023, Kuan-Yu (Claire) Lin'
author = 'Kuan-Yu (Claire) Lin'
release = '15-03-2023'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

import sphinx_nameko_theme
html_theme = 'nameko'
html_theme_path = [sphinx_nameko_theme.get_html_theme_path()]
html_static_path = ['_static']
