from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.containers import Vertical
import json
import httpx
from pathlib import Path

TOKEN_FILE = Path("token.json")
API_URL = "http://localhost:8000"

class UserInfoPanel(Static):
    def compose(self) -> ComposeResult:
        info_text = self.get_user_info_text()
        yield Static(info_text, id="userinfo-text")
        yield Button("Wyloguj", id="logout")
        
    def get_user_info_text(self) -> str:
        user_text = ""
        with open(TOKEN_FILE, "r") as file:
            token = json.load(file)

        resp_me = httpx.get(f"{API_URL}/users/me", headers={"Authorization": f"Bearer {token['access_token']}"})
        if resp_me.status_code == 200:
            data = resp_me.json()
            user_text = f"[b]Uzytkownik:[/b] {data['email']}\n[b]ID: {str(data['id'])}[/b]"
        else:
            user_text = f"[italic red]Nie zalogowano[/italic red]"
            
        # sprawdź, czy backend zyje
        
        try:
            httpx.get("http://localhost:8000/api/ping", timeout=1.5)
            status_line = "[green]•[/green] [b]Status:[/b] Online"
        except Exception:
            status_line = "[red]•[/red] [b]Status:[/b] Offline="
        return f"{user_text}\n{status_line}"
        
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "logout":
            if TOKEN_FILE.exists():
                TOKEN_FILE.unlink()
                self.app.notify("Wylogowano", timeout=2)
                
                # Goes to the login screen
                from widgets.login_screen import LoginScreen
                self.app.pop_screen() # removes TrackingListView
                self.app.push_screen(LoginScreen())
            else:
                self.app.notify("Nie byłeś zalogowany", timeout=2)        
        
        
        

