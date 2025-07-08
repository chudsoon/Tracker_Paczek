from textual.app import ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button
from textual.containers import VerticalScroll, Horizontal
from textual.screen import Screen

from widgets.tracking_list import TrackingList
from widgets.user_info import UserInfoPanel


import httpx
from pathlib import Path


API_URL = "http://localhost:8000"
TOKEN_FILE = Path("token.json")

class TrackingListView(Screen):
    BINDINGS = [("d", "go_to_add", "Dodaj przesyłkę")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            UserInfoPanel(),
            VerticalScroll(TrackingList())
        )
        yield Footer()
    
    def action_go_to_add(self):
        self.app.push_screen(AddTrackingView())
        

class AddTrackingView(Screen): 
    BINDINGS = [("escape", "app.pop_scren", "Powrót")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Dodaj nową przesyłkę", classes="title")
        yield Input(placeholder="Numer przesyłki", id="number")
        yield Input(placeholder="Kurier (np. inpost)", id="carrier")
        yield Button("Zapisz", id="save")
        yield Footer()
        
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        number = self.query_one("#number", Input).value.strip()
        carrier = self.query_one("#carrier", Input).value.strip()
        if not number or not carrier:
            self.app.bell()
            return
        
        payload = {
            "number": number,
            "carrier": carrier,
            "user_id": 1 # mozna tu wczytaywac zalogowanego uzytkownika
        }
        
        try:
            resp =  httpx.post(f"{API_URL}/trackings/", json=payload)
            if resp.status_code == 200:
                self.app.pop_screen() #wróc do listy
            else:
                self.app.bell()
        except Exception:
            self.app.bell()    
    
    