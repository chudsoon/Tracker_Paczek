from textual.app import ComposeResult
from textual.widgets import Header, Footer, Static, Button
from textual.screen import Screen
from pathlib import Path

import json
import httpx


API_URL = "http://localhost:8000"

TOKEN_FILE  = Path("token.json")

class TrackingList(Static):
    """Widget do wyświetlania listy przesyłek."""
  

    def on_mount(self):
        self.load()
        
    def get_user_id(self):
        if TOKEN_FILE.exists():
            with TOKEN_FILE.open("r", encoding="utf-8") as f:
                token = json.load(f)
            resp_me = httpx.get(f"{API_URL}/users/me", headers={"Authorization": f"Bearer {token['access_token']}"})
            data = resp_me.json()
            return int(data['id'])
        return None
        
    
    def load(self):
        self.update("") # wyczyść
    
        
        try:
            resp = httpx.get(f"{API_URL}/trackings/", params={"user_id": self.get_user_id()})
            data = resp.json()
            if not data:
                self.update("Brak przesyłek.")
                return
            for t in data:
                self.mount(Button(f"{t['number']} ({t['carrier']})", id=f"num-{t['number']}"))
        except Exception as e:
            self.update(f"[rad]Bład:[/] {e}")

    def on_button_pressed(self, event: Button.Pressed):
       raw_id = event.button.id # np. num-4
       if raw_id.startswith("num-"):
           tracking_number = int(raw_id.split("-")[1])
           self.app.push_screen(TrackingStatusView(tracking_number))
        

class TrackingStatusView(Screen):
    def __init__(self, tracking_id: int):
        super().__init__()
        self.tracking_id = tracking_id
        
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Status przesyłki:", classes="title", id="title")
        yield Static("Ładowanie...", id="status_area")
        yield Button("Odświez", id="refresh")
        yield Button("Powrót", id="back")
        yield Footer()
        
    def load_status(self):
        try:
            resp = httpx.get(f"{API_URL}/trackings/{self.tracking_id}/status")
            data = resp.json()
            
            title = f"{data['tracking_number']} - {data['status']}"
            self.query_one("#title", Static).update(title)
            
            history = data.get("tracking_details", [])
            if not history:
                self.query_one("#status_area", Static).update("Brak historii statusów")
            else:
                lines = [
                    f"[{item['datetime']}] {item['status']}"
                    for item in history
                ]
                self.query_one("#status_area", Static).update("\n".join(lines))
                self.app.notify("Dane zostały zaktualizowane", severity="success", timeout=2.5)
        except Exception as e:
            self.query_one("#status_area", Static).update(f"Błąd: {e}")
    
    def on_mount(self):
       self.load_status()
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "refresh":
            self.load_status()