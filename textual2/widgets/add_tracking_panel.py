from textual.app import ComposeResult
from textual.widgets import Header, Input, Static, Button, Footer
from textual.containers import Vertical
    
    
class AddTrackingPanel(Vertical):   
    
    def compose(self) -> ComposeResult:
        yield Static("Dodaj przesyłkę", classes="title")
        yield Input(placeholder="Numer przesyłki", id="tracking_input")
        yield Input(placeholder="Kurier", id="carrier_input")
        yield Button("Dodaj przesyłkę", id="add_button")
        yield Button("Anuluj", id="cancel_button")
        yield Static("", id="message")
        
    
    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "cancel_button":
            self.app.query_one("#right_panel").remove_children()
            from widgets.package_list  import PackageList
            self.app.query_one("#right_panel").mount(PackageList(id="PackageList"))
            