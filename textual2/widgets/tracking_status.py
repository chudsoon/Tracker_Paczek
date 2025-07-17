from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, Button

import json
import httpx

API_URL = "http://localhost:8000"


class TrackingStatus(Vertical):
    def __init__(self, tracking_id: int):
        super().__init__()
        self.tracking_id = tracking_id
    
    def compose(self) -> ComposeResult:
        yield Static("Status przesyłki:", classes="title")
        yield Static("Status przesyłki:", id="status")
        yield Static("Paczkomat:", classes="title")
        yield Static("Paczkomat:", id="target-machine")
        yield Static("Lokalizacja:", classes="title")
        yield Static("Lokalizacja:", id="location")
        yield Static("Historia nadania:", classes="title")
        yield Static("Ładowanie...", id="status-area")
        yield Button("Odświez", id="refresh-btn")
        yield Button("Wróć do listy przesyłek", id="return-btn")
        
    async def _on_mount(self) -> None:
        self.load_status()

        
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "return-btn":
            self.remove()
            from widgets.package_list import PackageList
            self.app.query_one("#right_panel").mount(PackageList(id="PackageList"))
        

    def load_status(self):
  
        
        try:
            resp = httpx.get(f"{API_URL}/trackings/{self.tracking_id}/status")
            data = resp.json()
            
            status = f"{data['tracking_number']} - {data['status']}"
            target_machine = f"{data['custom_attributes']['target_machine_id']}"
            location = f"{data['custom_attributes']['target_machine_detail']['location_description']}"
            self.app.query_one("#status", Static).update(status)
            self.app.query_one("#target-machine", Static).update(target_machine)
            self.app.query_one("#location", Static).update(location)
            
            
            history = data.get("tracking_details", [])
            if not history:
                self.query_one("#status-area", Static).update("Brak historii przesyłki")
            else:
                lines = [
                    f"[{item['datetime']}] {item['status']}"
                    for item in history
                ]
                self.app.query_one("#status-area", Static).update("\n".join(lines))
                self.app.notify("Dane zostały zaktualizowane", severity="success", timeout=2.5)
        except Exception as e:
            self.app.notify(f"Błąd: {e}", severity="error")
            
            
            

        