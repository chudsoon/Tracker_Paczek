from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, Static
from textual.containers import Vertical, Horizontal
import httpx
import json
from pathlib import Path

from auth import token_save
from pathlib import Path

API_URL = "http://localhost:8000"

class LoginPanel(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Zaloguj się", classes="title")
        yield Input(placeholder="Podaj email...", id="email_input")
        yield Input(placeholder="Podaj hasło...", id="password_input", password=True)
        yield Button("Zaloguj", id="login_btn")
        yield Button("Nie masz konta? Zarejestruj się ", id="go_register")
        yield Static("", id="message")
        
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
                        token_save(data)
                        headers = {"Authorization": f"Bearer {data['access_token']}"}
                        response_me = httpx.get(f"{API_URL}/users/me", headers=headers)
                        if response_me.status_code == 200:
                            user_data = response_me.json()
                            self.app.notify(f"Zalogowano {user_data['email']}", severity="success")
                            self.remove()
                            from widgets.user_panel import UserPanel
                            from widgets.package_list import PackageList
                            self.app.query_one("#left_panel").mount(UserPanel(id="UserPane"))
                            self.app.query_one("#WelcomePanel").remove()
                            self.app.query_one("#right_panel").mount(PackageList(id="PackageList"))
                        else:
                            message.update("Błąd logowania")
            except Exception as e:
                message.update(f"Błąd połączenia: {e}")
            
        if event.button.id == "go_register":
            self.remove()
            from widgets.registration_panel import  RegistrationPanel
            self.app.query_one("#left_panel").mount(RegistrationPanel(id="RegistrationPanel"))
            
        

        
