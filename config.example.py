"""
Configuration for the Italian Learning Toolkit.

Copy this file to config.py and set your OPENAI_API_KEY environment variable,
or set it directly in config.py (not recommended for production).

For security, prefer setting the ``OPENAI_API_KEY`` environment variable
instead of keeping secrets in source control.
"""

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

