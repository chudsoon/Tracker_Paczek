from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, Button

import json
import httpx

API_URL = "http://localhost:8000"


class TrackingStatus(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Status przesyłki", classes="title")
        yield Button("Wróć do listy przesyłek", id="return-btn")
        
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "return-btn":
            self.remove()
            from widgets.package_list import PackageList
            self.app.query_one("#right_panel").mount(PackageList(id="PackageList"))
        



        