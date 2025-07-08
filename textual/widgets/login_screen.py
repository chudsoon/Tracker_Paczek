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
        yield Input(placeholder="Podaj hasło...", id="password_input", password=True)
        yield Button("Zaloguj", id="login_btn")
        yield Static("", id="message")
        yield Button("Nie masz konta? Zarejestruj się", id="go_register")
        yield Footer()
    
    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "login_btn":
            email_input = self.query_one("#email_input", Input).value.strip()
            password_input = self.query_one("#password_input", Input).value.strip()
            message = self.query_one("#message", Static)
            
            
            if not email_input:
                self.app.notify("Wpisz adres email", severity="warning")
                return
            
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(f"{API_URL}/users/login", json={"email": email_input, "password": password_input})
                    if resp.status_code == 200:
                        data = resp.json()
                        headers = {"Authorization": f"Bearer {data['access_token']}"}
                        response_me = httpx.get(f"{API_URL}/users/me", headers=headers)
                        if response_me.status_code == 200:
                            user_data = response_me.json()
                            self.app.notify(f"Zalogowano {user_data['email']}", severity="success")
                            from  main import TrackingListView
                            self.app.push_screen(TrackingListView())
                    else:
                        message.update("Błąd logowania")
                        
            except Exception as e:
                message.update(f"Błąd połączenia: {e}")
                                        
                
               
        elif event.button.id == "go_register":
            from widgets.registration_screen import RegisterScreen
            self.app.pop_screen()
            self.app.push_screen(RegisterScreen())