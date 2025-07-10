from textual.app import ComposeResult
from textual.widgets import Header, Input, Static, Button, Footer
from textual.containers import Vertical

import httpx

API_URL = "http://localhost:8000"

class RegistrationPanel(Vertical):
  
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Zarejestruj się", classes="title")
        yield Input(placeholder="Podaj nazwę uzytkownika...", id="full_name_input")
        yield Input(placeholder="Podaj adres email...", id="email_input")
        yield Input(placeholder="Podaj hasło...", id="password_input", password=True)
        yield Input(placeholder="Powtórz hasło...", id="password_confirm_input", password=True)
        yield Button("Zarejestruj", id="register_button")
        yield Button("Anuluj", id="cancel_button")
        yield Static("", id="message")
        yield Footer()
        
        
    async def on_button_pressed(self, event: Button.Pressed):
        
        if event.button.id == "register_button":
            
            self.register()
  

                
                
            
        
        if event.button.id == "cancel_button":
            self.remove()
            from widgets.login_panel import LoginPanel
            self.app.query_one("#left_panel").mount(LoginPanel(id="LoginPanel"))
        
        
    
    def register(self):
        username = self.query_one("#full_name_input", Input).value.strip()
        email = self.query_one("#email_input", Input).value.strip()
        password = self.query_one("#password_input", Input).value.strip()
        password_confirm = self.query_one("#password_confirm_input", Input).value.strip()
        
        if password != password_confirm:
            self.app.notify("Podane hasła nie są tozsame", severity="warning")
            return 
        
        # check if user exists
        
        try: 
            check = httpx.get(f"{API_URL}/users/by_email", params={"email": email})
            if check.status_code == 200:
                self.app.notify("Podany email jest juz zarejestrowany", severity="error")
                return 
        except Exception as e:
            self.app.notify(f"Bład połączenia {e}", severity="error")
            return
        
        # register user
        
        try:
            req = httpx.post(f"{API_URL}/users/", json={"email": email, "full_name": username, "password": password})
            if req.status_code != 200:
                self.app.notify("Rejestracja nieudana", severity="error")
                return
            
            self.app.notify("Zarejestrowano pomyślnie", severity="success")
            self.remove()
            from widgets.login_panel import LoginPanel
            self.app.query_one("#left_panel").mount(LoginPanel(id="LoginPanel"))   
            
        except Exception as e:
            self.app.notify(f"Wystąpił bład rejestacji {e}", severity="error")
        
                
                