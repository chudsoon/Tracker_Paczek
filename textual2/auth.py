from pathlib import Path
import json

TOKEN_FILE = Path("token.json")


def token_extist() -> bool:
    if  TOKEN_FILE.exists():
        return True
    
def token_save(data):
    with open (TOKEN_FILE, "w") as file:
        json.dump(data, file, indent=4)
        
def get_access_token():
    if token_extist:
        try:
            with open(TOKEN_FILE, "r") as file:
                token = json.load(file)
            access_token = token['access_token']
            return access_token
        except(json.JSONDecodeError, KeyError):
            access_token = None
    else:
        access_token = None

  