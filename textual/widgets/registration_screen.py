from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, Static
from textual.containers import Vertical
import httpx, json
from pathlib import Path

USER_FILE = Path.home() / ".tracker_user"
API_URL = "http://localhost:8000"

class RegisterScreen(Screen):
    def compose(self):
        yield Header()
        yield Static("Rejestracja", classes="title")
        yield Input(placeholder="Email", id="email_input")
        yield Input(placeholder="Imię i nazwisko", id="name_input")
        yield Button("Zarejestruj", id="register_btn")
        yield Button("Mam juz konto", id="go_login")
        yield Footer()
        
    def _on_mount(self):
        self.query_one("#email_input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "register_btn":
            self.register()
        elif event.button.id == "go_login":
            from widgets.login_screen import LoginScreen
            self.app.push_screen(LoginScreen())
    
    def register(self):
        email = self.query_one("#email_input", Input).value.strip()
        name = self.query_one("#name_input", Input).value.strip()
        
        if not email or not name:
            self.app.notify("Wypełnij wszystkie pola", severity="warning")
            return
        
        try:
            resp = httpx.post(f"{API_URL}/users/", json={"email": email, "full_name": name})
            if resp.status_code != 200:
                self.app.notify("Rejestracja nieudana", severity="error")
                return
            
            user = resp.json()
            USER_FILE.write_text(json.dumps(user))
            self.app.notify("Zarejestrowano pomyślnie", timeout=2)
            from main import TrackingListView
            self.app.push_screen(TrackingListView())
        
        except Exception as e:
            self.app.notify(f"Błąd: {e}", severity="error")            