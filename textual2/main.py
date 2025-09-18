from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

from widgets.menu_panel import MenuPanel
from widgets.package_list import PackageList


from auth import token_extist










class TrackingApp(App):
    CSS_PATH = "styles.css"  # <- Ścieżka do osobnego pliku CSS
    BINDINGS = [Binding("d", "go_to_add", "Dodaj przesyłkę")]


    def compose(self) -> ComposeResult:
        yield Header()

        yield Horizontal(
            Vertical(id="left_panel"),
            Vertical(id="right_panel")
        )
        yield Footer()
        
        
    async def on_mount(self) -> None:
        if not token_extist():
            from widgets.login_panel import LoginPanel
            from widgets.welcome_panel import WelcomePanel
            self.query_one("#left_panel").mount(LoginPanel(id="LoginPanel"))
            self.query_one("#right_panel").mount(WelcomePanel(id="WelcomePanel"))
        else:
            self.query_one("#left_panel").mount(MenuPanel(id="MenuPanel"))
            self.query_one("#right_panel").mount(PackageList(id="PackageList"))




if __name__ == "__main__":
    TrackingApp().run()
