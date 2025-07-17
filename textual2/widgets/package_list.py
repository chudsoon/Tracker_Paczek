from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static,Label, Button, Footer
from textual.binding import Binding
from auth import token_extist, get_access_token

import httpx

API_URL = "http://localhost:8000"

class PackageList(Vertical):
    def compose(self) -> ComposeResult:
        self.load()
        yield Static("", id="message")
        
    def load(self):
        self.mount(Static("Znajdź przesyłkę", classes="title"))
        try:
            resp = httpx.get(f"{API_URL}/trackings/", params={"user_id": self.get_user_id()})
            data = resp.json()
            if not data:
                self.mount(Static("Brak przesyłek"))
                return
            for t in data:
                self.mount(Button(f"{t['number']} ({t['carrier']})", id=f"num-{t['number']}"))
        except Exception as e:
            self.mount(Static(f"[red]Błąd:[/] {e}"))
            
    def get_user_id(self):
        if token_extist():
            resp_me = httpx.get(f"{API_URL}/users/me", headers={"Authorization": f"Bearer {get_access_token()}"})
            data = resp_me.json()
            return int(data['id'])  
        return None         
            
    def on_button_pressed(self, event: Button.Pressed):
        raw_id = event.button.id 
        if raw_id.startswith("num-"):
            tracking_number = int(raw_id.split("-")[1])
            self.remove()
            from widgets.tracking_status import TrackingStatus
            self.app.query_one("#right_panel").mount(TrackingStatus(id="TrackingStatus"))
            
            
            
            
            
class PackageEntry(Horizontal):
    def __init__(self, number: str, status: str):
        super().__init__()
        self.number = number
        self.status = status

    def compose(self) -> ComposeResult:
        yield Label(self.number, classes="package_number")
        yield Label(self.status, classes="package_status")