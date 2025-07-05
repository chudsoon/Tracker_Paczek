from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.containers import Vertical
import json
import httpx
from pathlib import Path

USER_FILE = Path.home() / ".tracker_user" # jak w CLI

class UserInfoPanel(Static):
    def compose(self) -> ComposeResult:
        info_text = self.get_user_info_text()
        yield Static(info_text, id="userinfo-text")
        yield Button("Wyloguj", id="logout")
        
    def get_user_info_text(self) -> str:
        user_text = ""
        if USER_FILE.exists():
            data = json.load(open(USER_FILE))
            email = data.get("email", "Nieznany")
            user_id = data.get("id", "?")
            user_text = f"[b]Uzytkownik:[/b] {email}\n[b]ID:[/b] {user_id}"
        else:
            user_text = "[italic red]NIe zalogowano[/italic red]"
            
        # sprawdź, czy backend zyje
        
        try:
            httpx.get("http://localhost:8000/api/ping", timeout=1.5)
            status_line = "[green]•[/green] [b]Status:[/b] Online"
        except Exception:
            status_line = "[red]•[/red] [b]Status:[/b] Offline="
        return f"{user_text}\n{status_line}"
        
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "logout":
            if USER_FILE.exists():
                USER_FILE.unlink()
                self.app.notify("Wylogowano", timeout=2)
                
                # Goes to the login screen
                from widgets.login_screen import LoginScreen
                self.app.pop_screen() # removes TrackingListView
                self.app.push_screen(LoginScreen())
            else:
                self.app.notify("Nie byłeś zalogowany", timeout=2)        
        
        
        

