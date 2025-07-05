from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, Static
from textual.containers import Vertical
import httpx
import json
from pathlib import Path

USER_FILE = Path(".tracker_user")
API_URL = "http://localhost:8000"

class LoginScreen(Screen):
    def compose(self):
        yield Header()
        yield Static("Zaloguj się", classes="title")
        yield Input(placeholder="Podaj email...", id="email_input")
        yield Button("Zaloguj", id="login_btn")
        yield Button("Nie masz konta? Zarejestruj się", id="go_register")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "login_btn":
            email = self.query_one("#email_input", Input).value.strip()
            if not email:
                self.app.notify("Wpisz adres email", severity="warning")
                return
            
            try:
                resp = httpx.get(f"{API_URL}/users/by_email", params={"email": email})
                if resp.status_code == 404:
                    self.app.notify("Nie znaleziono uzytkownika", severity="error")
                    return
                
                user = resp.json()
                USER_FILE.write_text(json.dumps(user))
                self.app.notify(f"Zalogowano jako {user['email']}", timeout=2)
                
                # Go to the main view
                from main import TrackingListView
                self.app.push_screen(TrackingListView())
                
                
            except Exception as  e:
                self.app.notify(f"Błąd logowania: {e}", severity="error")
        elif event.button.id == "go_register":
            from widgets.registration_screen import RegisterScreen
            self.app.pop_screen()
            self.app.push_screen(RegisterScreen())