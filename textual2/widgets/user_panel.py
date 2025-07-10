from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button, Label


from auth import token_extist, get_access_token, remove_token

import httpx

API_URL = "http://localhost:8000"


class User():
    full_name: str
    email: str


class UserPanel(Vertical):
    
    user = User()
        
    def get_user_info(self) -> User:
        resp_me = httpx.get(f"{API_URL}/users/me", headers={"Authorization": f"Bearer {get_access_token()}"})
        if resp_me.status_code == 200:
            data = resp_me.json()
            self.user.full_name = data['full_name']
            self.user.email = data['email']
            return self.user
            
        else:
            self.app.notify("Niezalogowano", severity="error")
            

            
            
    
    def compose(self) -> ComposeResult:
        user = self.get_user_info()
        yield Static(user.full_name, classes="user_name")
        yield Static(user.email, classes="user_email")
        yield Static("rola: Client", classes="user_role")
        yield Button("DODAJ PRZESYŁKĘ", id="add_package")
        yield Button("PANEL ADMINISTRATORA", id="admin_panel")
        yield Button("WYLOGUJ", id="logout")
        
    
    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "logout":
            remove_token()
            self.remove()
            self.app.query_one("#PackageList").remove()
            from widgets.login_panel import LoginPanel
            from widgets.welcome_panel import WelcomePanel
            self.app.query_one("#left_panel").mount(LoginPanel(id="LoginPanel"))
            self.app.query_one("#right_panel").mount(WelcomePanel(id="WelcomePanel"))
            self.app.notify(f"Wylogowano {self.user.email}")