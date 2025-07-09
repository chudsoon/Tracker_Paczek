from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Static, Input, Button
from textual.containers import VerticalScroll, Horizontal
from textual.screen import Screen
from textual import events

from widgets.tracking_list import TrackingList
from widgets.user_info import UserInfoPanel
from widgets.add_tracking import TrackingListView
from widgets.user_info import UserInfoPanel
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
    BINDINGS = [Binding("q", "quit_app", "Quit")]
    
    async def action_quit_app(self) -> None:
    # Removes token after closing the app
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
            self.log("Token usunięty - wylogowano uzytkownika")
        self.app.exit()
        
    def on_mount(self) -> None:
        if TOKEN_FILE.exists():
            self.push_screen(TrackingListView())
        else:
            from widgets.login_screen import LoginScreen
            self.push_screen(LoginScreen())
            

    




if __name__ == "__main__":

    app = TrackerApp()
    app.run()