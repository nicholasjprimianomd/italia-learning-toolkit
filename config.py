"""
Configuration for the Italian Learning Toolkit.

For security, prefer setting the ``OPENAI_API_KEY`` environment variable
instead of keeping secrets in source control.
"""

import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

