"""
Web entry point for cloud deployment.
Run this file when deploying to web hosting platforms.
"""
import os
os.environ["FLET_WEB_MODE"] = "true"

from main import main
import flet as ft

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8550"))
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        port=port, 
        host="0.0.0.0",
        web_renderer=ft.WebRenderer.HTML,  # Better mobile support
    )

