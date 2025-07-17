from textual.app import ComposeResult
from textual.widgets import Header, Input, Static, Button, Footer
from textual.containers import Vertical

from auth import get_access_token

import json
import httpx

API_URL = "http://localhost:8000"
    
class User():
    id: int
    full_name: str
    email: str
    
    
class AddTrackingPanel(Vertical):   
    
    user = User ()
    
    def compose(self) -> ComposeResult:
        yield Static("Dodaj przesyłkę", classes="title")
        yield Input(placeholder="Numer przesyłki", id="tracking_input")
        yield Input(placeholder="Kurier", id="carrier_input")
        yield Button("Dodaj przesyłkę", id="add_button")
        yield Button("Anuluj", id="cancel_button")
        yield Static("", id="message")
        
    
    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_button":
            self.get_user_info()
            user_id = self.user.id
            number = self.query_one("#tracking_input", Input).value.strip()
            carrier = self.query_one("#carrier_input", Input).value.strip()
            if not number or not carrier:
                self.app.bell()
                return
            
          
            
            
            
            payload = {
                "number": number,
                "carrier": carrier,
                "user_id": user_id
            }
            
            try:
                resp = httpx.post(f"{API_URL}/trackings/", json=payload)
                if resp.status_code == 200:
                    self.remove()
                    from widgets.package_list import PackageList
                    self.query_one("#right_panel").mount(PackageList(id="PackageList"))
                else: 
                    self.app.bell()
            except Exception:
                self.app.bell()
            
        elif event.button.id == "cancel_button":
            self.app.query_one("#right_panel").remove_children()
            from widgets.package_list  import PackageList
            self.app.query_one("#right_panel").mount(PackageList(id="PackageList"))
    
    def get_user_info(self) -> User:
        resp_me = httpx.get(f"{API_URL}/users/me", headers={"Authorization": f"Bearer {get_access_token()}"})
        if resp_me.status_code == 200:
            data = resp_me.json()
            self.user.id = data['id']
            self.user.full_name = data['full_name']
            self.user.email = data['email']
            return self.user
            
        else:
            self.app.notify("Niezalogowano", severity="error")    