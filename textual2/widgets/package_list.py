from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static,Label, Button, Footer, RadioButton
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
                self.mount(RadioButton(f"{t['number']} ({t['carrier']})", id=f"num-{t['number']}"))
        except Exception as e:
            self.mount(Static(f"[red]Błąd:[/] {e}"))
        self.mount(Button("Szczegóły przesyłki", id="btn-parcel-deatails"))
            
    def get_user_id(self):
        if token_extist():
            resp_me = httpx.get(f"{API_URL}/users/me", headers={"Authorization": f"Bearer {get_access_token()}"})
            data = resp_me.json()
            return int(data['id'])  
        return None         
            
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-parcel-deatails":
            tracking_number = self.get_selected()
            if tracking_number:
                tracking_number
                self.remove()
                from widgets.tracking_status import TrackingStatus
                self.app.query_one("#right_panel").mount(TrackingStatus(tracking_number))
            
    @on(RadioButton.Changed)
    def only_one_checked(self, event: RadioButton.Changed) -> None:
        # Ensuring that only one RadioButton is checked
        if event.radio_button.value: #checked
            event.radio_button.value = True 
            # Unchecked all other radio buttons
            for rb in self.query(RadioButton):
                if rb is not event.radio_button:
                    rb.value = False
    
    def get_selected(self):
        # Returns the number of the parcel
        for rb in self.query(RadioButton):
            if rb.value:
                return rb.id.split("-")[1]
        return None
            
            
            
            
        