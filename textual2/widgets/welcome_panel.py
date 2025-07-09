from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static


class WelcomePanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Konsolowy Tracker Paczek", classes="title")
        yield Static("Witamy w aplikacji do zarządzania i śledzenia przesyłek. Dzięki niej możesz sprawdzać status swoich przesyłek w czasie rzeczywistym, dodawać nowe przesyłki do monitorowania zarządzać kontem oraz dostępem do panelu administratora. Połączono z API — dane są aktualizowane automatycznie.")
        
        