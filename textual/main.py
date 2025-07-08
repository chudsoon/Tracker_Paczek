from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button
from textual.containers import VerticalScroll, Horizontal
from textual.screen import Screen
from textual import events

from widgets.tracking_list import TrackingList
from widgets.user_info import UserInfoPanel
from widgets.add_tracking import TrackingListView
import json
from pathlib import Path


API_URL = "http://localhost:8000"
TOKEN_FILE = Path("token.json")

# --- Ekran: lista przeysłek --- 


class TrackerApp(App):
    """Główna aplikacja TUI."""
    
    CSS_PATH = "main.tcss"
    TITLE = "Śledzenie przesyłek"
    SUB_TITLE = "Konsolowy interfejs Textual"
    
    def on_mount(self) -> None:
        if TOKEN_FILE.exists():
            self.push_screen(TrackingListView())
        else:
            from widgets.login_screen import LoginScreen
            self.push_screen(LoginScreen())
    


def on_mount(self) -> None:
    self.push_screen(TrackingListView()) 


if __name__ == "__main__":

    app = TrackerApp()
    app.run()