from textual.app import App, ComposeResult

from widgets.user_panel import UserPanel
from widgets.package_list import PackageList


from auth import token_extist










class TrackingApp(App):
    CSS_PATH = "styles.css"  # <- Ścieżka do osobnego pliku CSS

    def compose(self) -> ComposeResult:
        if  token_extist():
            yield UserPanel()
            yield PackageList()
        else: 
            from widgets.login_panel import LoginPanel
            from widgets.welcome_panel import WelcomePanel
            yield LoginPanel(id="LoginPanel")
            yield WelcomePanel(id="WelcomePanel")




if __name__ == "__main__":
    TrackingApp().run()
