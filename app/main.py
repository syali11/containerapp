import os
from datetime import datetime, timezone
from fastapi import FastAPI

app = FastAPI(title="Pipeline Test App")

# Bumped on each deploy to prove a new revision went live.
VERSION = os.getenv("APP_VERSION", "v1")


@app.get("/")
def root():
    return {
        "message": "Hello from the self-hosted runner pipeline!",
        "version": VERSION,
        "time": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
def health():
    return {"status": "healthy", "version": VERSION}
