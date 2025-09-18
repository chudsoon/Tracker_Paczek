from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Button

import httpx

API_URL = "http://localhost:8000"


class AdminPanel(Vertical):
    
    def compose(self) -> ComposeResult:
        yield Static("Panel Administratora", classes="title")
        yield Button("Lista uzytkowników", id="userList-btn")
        yield Button("Powrót", id="back-btn")
    
    
    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "userList-btn":
            self.load_user_list()
        elif event.button.id == "back-btn":
            self.app.query_one("#right_panel").remove_children()
            from widgets.package_list import PackageList  
            self.app.query_one("#right_panel").mount(PackageList(id="PackageList"))  
            
            
    def load_user_list(self):
        self.mount(Static("Lista uzytkowników", classes="title"))
        try:
            resp = httpx.get(f"{API_URL}/users/")
            data = resp.json()
            if not data:
                self.mount(Static("Brak uzytkowników"))
                return
            for u in data: 
                self.mount(Button(f"{u['full_name']}"))
        except Exception as e:
            self.mount(Static(f"[red]Błąd:[/] {e}"))
            
    
    