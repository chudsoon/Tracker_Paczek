from fastapi import FastAPI
from app.api import tracking, user, system
from app.models import User, Tracking

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# POZWAŁAJ Angularowi (localhost:4200) na dostęp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tracking.router, prefix="/trackings")
app.include_router(user.router, prefix="/users")
app.include_router(system.router, prefix="/api")


