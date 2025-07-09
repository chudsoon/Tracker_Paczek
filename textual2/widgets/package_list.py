from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static,Label

class PackageList(Vertical):
    def compose(self) -> ComposeResult:
        yield Static("Śledzenie przesyłek", classes="title")
        yield PackageEntry("123456789", "W drodze")
        yield PackageEntry("987654321", "Dostarczono")
        yield PackageEntry("567890123", "Odebrano")
        yield PackageEntry("246813579", "Odprawa celna")


class PackageEntry(Horizontal):
    def __init__(self, number: str, status: str):
        super().__init__()
        self.number = number
        self.status = status

    def compose(self) -> ComposeResult:
        yield Label(self.number, classes="package_number")
        yield Label(self.status, classes="package_status")