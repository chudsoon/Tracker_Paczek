from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical

from widgets.user_panel import UserPanel
from widgets.package_list import PackageList


from auth import token_extist










class TrackingApp(App):
    CSS_PATH = "styles.css"  # <- Ścieżka do osobnego pliku CSS

    def compose(self) -> ComposeResult:
        
        yield Horizontal(
            Vertical(id="left_panel"),
            Vertical(id="right_panel")
        )
        
        
    async def on_mount(self) -> None:
        if not token_extist():
            from widgets.login_panel import LoginPanel
            from widgets.welcome_panel import WelcomePanel
            self.query_one("#left_panel").mount(LoginPanel(id="LoginPanel"))
            self.query_one("#right_panel").mount(WelcomePanel(id="WelcomePanel"))
        else:
            self.query_one("#left_panel").mount(UserPanel(id="UserPanel"))
            self.query_one("#right_panel").mount(PackageList(id="PackageList"))




if __name__ == "__main__":
    TrackingApp().run()
