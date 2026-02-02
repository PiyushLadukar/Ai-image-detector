from fastapi import FastAPI
import uvicorn

from app.config import APP_NAME, VERSION
from app.routes import register_routes

app = FastAPI(title=APP_NAME, version=VERSION)

register_routes(app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
