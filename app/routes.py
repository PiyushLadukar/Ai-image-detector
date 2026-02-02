from fastapi import UploadFile, File, Form
from fastapi.responses import HTMLResponse
import os

from app.config import UPLOAD_DIR
from app.templates import HOME_PAGE, result_page
from app.ai_engine import (
    fake_probability,
    detect_objects,
    is_duplicate,
    trust_score,
    decision
)

def register_routes(app):

    @app.get("/", response_class=HTMLResponse)
    def home():
        return HOME_PAGE

    @app.post("/analyze", response_class=HTMLResponse)
    async def analyze(
        file: UploadFile = File(...),
        issue: str = Form(...)
    ):
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # AI processing
        fake = fake_probability()
        objects = detect_objects(issue)
        duplicate = is_duplicate(file_path, UPLOAD_DIR)

        score = trust_score(fake, objects, duplicate)
        result = decision(score)

        # Return result page
        return result_page(objects, fake, duplicate, score, result)
