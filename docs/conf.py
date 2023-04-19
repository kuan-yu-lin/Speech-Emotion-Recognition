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

extensions = [
    'sphinx_book_theme',
    "ablog",
    "myst_nb",
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinxcontrib.youtube",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_examples",
    "sphinx_tabs.tabs",
    "sphinx_thebe",
    "sphinx_togglebutton",
    "sphinxcontrib.bibtex",
    "sphinxext.opengraph",
    # For the kitchen sink
    "sphinx.ext.todo",
]

templates_path = ['_templates']
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_title = "Speech Emotion Recognition"
html_static_path = ['_static']

# -- Download latest theme elements page from PyData -----------------------------

path_pydata_content = "https://raw.githubusercontent.com/pydata/pydata-sphinx-theme/main/docs/user_guide/theme-elements.md"  # noqa
path_content_file = Path(__file__).parent / "content/pydata-content-blocks.md"
if not path_content_file.exists():
    with urlopen(path_pydata_content) as resp:
        # Read in the content page file, then update the title and add context
        content = resp.read().decode().split("\n")
        ix_title = content.index("# Theme-specific elements")
        content[ix_title] = "# PyData Theme Elements"
        content.insert(
            ix_title + 1,
            "\nThis is a collection of content blocks with special support from this theme's parent theme, [the PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/latest/user_guide/theme-elements.html)\n",  # noqa
        )  # noqa
        content = "\n".join(content)
        # Replace a relative link in the pydata docs w/ the respective one here
        content = content.replace("../examples/pydata.md", "notebooks.md")
        # Write to disk in a location that will be ignored by git
        path_content_file.write_text(content)


def setup(app):
    # -- To demonstrate ReadTheDocs switcher -------------------------------------
    # This links a few JS and CSS files that mimic the environment that RTD uses
    # so that we can test RTD-like behavior. We don't need to run it on RTD and we
    # don't wanted it loaded in GitHub Actions because it messes up the lighthouse
    # results.
    if not os.environ.get("READTHEDOCS") and not os.environ.get("GITHUB_ACTIONS"):
        app.add_css_file(
            "https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css"
        )
        app.add_css_file("https://assets.readthedocs.org/static/css/badge_only.css")

        # Create the dummy data file so we can link it
        # ref: https://github.com/readthedocs/readthedocs.org/blob/bc3e147770e5740314a8e8c33fec5d111c850498/readthedocs/core/static-src/core/js/doc-embed/footer.js  # noqa: E501
        app.add_js_file("rtd-data.js")
        app.add_js_file(
            "https://assets.readthedocs.org/static/javascript/readthedocs-doc-embed.js",
            priority=501,
        )