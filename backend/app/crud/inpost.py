import httpx
from typing import Optional

def  get_inpost_status(tracking_number: str) -> Optional[dict]:
    url = f"https://api-shipx-pl.easypack24.net/v1/tracking/{tracking_number}"
    resp = httpx.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()