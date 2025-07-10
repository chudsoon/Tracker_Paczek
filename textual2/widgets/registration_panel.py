from textual.app import ComposeResult
from textual.widgets import Header, Input, Static, Button, Footer
from textual.containers import Vertical

class RegistrationPanel(Vertical):
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Zarejestruj się", classes="title")
        yield Input(placeholder="Podaj nazwę uzytkownika...", id="full_name_input")
        yield Input(placeholder="Podaj adres email...", id="email_input")
        yield Input(placeholder="Podaj hasło...", id="password_input", password=True)
        yield Input(placeholder="Powtórz hasło...", id="password_confirm_input", password=True)
        yield Button("Zarejestruj", id="register_button")
        yield Button("Anuluj", id="cancel_button")
        yield Static("", id="message")
        yield Footer()
        
        
    async def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "cancel_button":
            self.remove()
            from widgets.login_panel import LoginPanel
            self.app.query_one("#left_panel").mount(LoginPanel(id="LoginPanel"))
        