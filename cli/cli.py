import typer
import requests
import time
import httpx
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.panel import Panel
from pathlib import Path
import json
from cli_models import User
from typing import Optional


USER_FILE = Path.home() / ".tracker_user"

def save_current_user(user: User) -> None:
    USER_FILE.write_text(user.model_dump_json())

def load_current_user() -> Optional[User]:
    if USER_FILE.exists():
        #Pydantic potwierdzi, ze struktura w pliku pasuje do modelu
        return User.model_validate_json(USER_FILE.read_text())
    return None

app = typer.Typer()
console = Console()

API_URL = "http://localhost:8000"

@app.command()
def add_user(email: str, full_name: str):
    """Dodaj nowego uzytkownika"""
    resp = requests.post(f"{API_URL}/users/", json={
        "email": email,
        "full_name": full_name
    })
    console.print(resp.json(), style="green")
    

@app.command()
def login(email: str):
    """Zaloguj się jako istniejący uzytkownik za pomocą e-email"""
    resp = requests.get(f"{API_URL}/users")
    resp.raise_for_status()
    user = [User(**u) for u in resp.json()]
    
    found = next((u for u in user if u.email == email), None)
    if not found: 
        console.print(f"Nie znaleziono e-mail {email}", style="red")
        raise typer.Exit()
    
    save_current_user(found)
    console.print(f"Zalogowano jako {found.full_name}", style="green")

@app.command()
def list_trackings(user_id: int):
    """Wyświetl listę przesyłek danego uzytkowanika"""
    resp = requests.get(f"{API_URL}/trackings/", params={"user_id": user_id})
    if resp.status_code != 200:
        console.print("Błąd!", style="bold red")
        return
    
    trackings = resp.json()
    table = Table(title=f"Przesyłki uzytkownika {user_id}")
    table.add_column("ID", style="cyan")
    table.add_column("Numer", style="green")
    table.add_column("Kurier", style="magenta")
    
    for t in trackings:
        table.add_row(str(t["id"]), t["number"], t["carrier"])
    
    console.print(table)
    
@app.command()
def add_tracking(user_id: int, number: str, carrier: str):
    """Dodaj przesyłkę jako aktualnie zalogowany uzytkownik"""
    
    user = load_current_user()
    if not user:
        console.print("Najpierw wykonaj: python cli.py login <email>", style="red")
        raise typer.Exit()
    
    payload = {
        "number": number,
        "carrier": carrier,
        "user_id": user.id
    }
    
    resp = requests.post(f"{API_URL}/trackings/", json=payload)
    if resp.ok:
        console.print("Przesyłka dodana", style="green")
    else:
        console.print(f"Błąd: {resp.text}", style="red")
        
@app.command()
def delete_tracking(tracking_id: int):
    """Usuń przesyłkę po ID"""
    resp = requests.delete(f"{API_URL}/trackings/{tracking_id}")
    if resp.ok: 
        console.print(f"Przesyłka {tracking_id} usunięta", style="bold green")
    else:
        console.print(f"Błąd {resp.status_code} - {resp.text}", style="red")

@app.command()
def delete_all_trackings(user_id: int):
    """Usuń wszystkie przesyłki danego uzytkownika"""
    resp = requests.get(f"{API_URL}/trackings/", params={"user_id": user_id})
    if resp.status_code != 200:
        console.print(f"Nie udało się pobrać przesyłek {resp.status_code}", style="red")
        return
    
    trackings = resp.json()
    if not trackings:
        console.print("Brak przesyłek do usunięcia", style="green")
        return
    
    console.print(f"Znaleziono {len(trackings)} przesyłek do usunięcia.", style="yellow")
    confirm = input("Czy na pewo chcesz je wszystkie usunąc? (y/N): ")
    
    if confirm.lower() != 'y':
        console.print("Operacja anulowana", style="dim")
        return

    for t in trackings:
        del_res = requests.delete(f"{API_URL}/trackings/{t['id']}")
        if del_res.ok:
            console.print(f"Usnięteo {t['number']} ({t['carrier']})", style="green")
        else:
            console.print(f"Bład usuwania ID {t['id']}: {del_res.status_code}", style="red")
            
        
SIMULATED_STATUSES = [
    "Przesyłka zarejestrowana",
    "Przekazana do nadania",
    "W trasie",
    "Wydana do doręczenia",
    "Dostarczona"
]

@app.command()
def show_status(tracking_number: str):
    """Symulowany status przesyłki (dla demo/debugowania)"""
    console.print(Panel.fit(f"Śledzenie przesyłki: [bold]{tracking_number}[/]"))
    
    resp = requests.get(f"{API_URL}/trackings/{tracking_number}/status")
    data = resp.json()
    console.print(f"Numer przesyłki: [bold]{data.get('tracking_number', 'Brak danych')}[/]")
    console.print(f"Aktualny status: [bold green]{data.get('status', 'Brak danych')}[/]")
    
    tracking_details = data.get("tracking_details", [])
    if tracking_details:
        table = Table(title="Historia statusów")
        table.add_column("Data", style="dim")
        table.add_column("Status")
        for detail in tracking_details:
            table.add_row(detail.get("datetime", "Brak danych"), detail.get("status", "Brak danych"))
        console.print(table)
    else:
        console.print("Brak historii statusów dla tej przesyłki.", style="yellow")
    
    
    
    console.print(Panel.fit(f"[bold green] Przesyłka {tracking_number} została dostarczona![/]"))
    
    

if __name__ == "__main__":
    app()    