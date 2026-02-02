# =========================================================
# AI-DRIVEN COMPLAINT IMAGE VALIDATION SYSTEM
# Author  : Piyush Ladukar
# Purpose : Smart City / Municipal AI Validation
# Tech    : FastAPI + Image Hashing + Rule-based AI
# =========================================================

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import uvicorn
import os
import random
import math
from PIL import Image
import imagehash

# =========================================================
# APP CONFIG
# =========================================================

app = FastAPI(
    title="AI Complaint Validation System",
    description="AI-powered image validation for municipal complaints",
    version="1.0.0"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================================================
# AI / LOGIC LAYER
# =========================================================

def simulate_fake_probability() -> float:
    """
    Simulates AI probability that image is fake or irrelevant.
    Lower value = more trustworthy image.
    """
    return round(random.uniform(0.05, 0.40), 2)


def detect_issue_objects(issue_type: str) -> list:
    """
    Simulated object detection based on issue type
    """
    ISSUE_DB = {
        "garbage": ["plastic", "trash", "waste"],
        "road": ["pothole", "crack", "road-damage"],
        "water": ["leak", "pipe", "overflow"]
    }
    return random.sample(ISSUE_DB.get(issue_type, []), k=1)


def calculate_location_score(lat: float, lon: float) -> int:
    """
    Dummy geo validation logic
    """
    if 8 <= lat <= 37 and 68 <= lon <= 97:
        return 20   # Inside India
    return 5


def check_duplicate_image(new_image_path: str) -> bool:
    """
    Detects duplicate images using perceptual hashing
    """
    try:
        new_img = Image.open(new_image_path)
        new_hash = imagehash.phash(new_img)

        for file in os.listdir(UPLOAD_DIR):
            existing_path = os.path.join(UPLOAD_DIR, file)
            if existing_path == new_image_path:
                continue

            try:
                old_img = Image.open(existing_path)
                old_hash = imagehash.phash(old_img)

                if abs(old_hash - new_hash) <= 5:
                    return True
            except:
                continue

        return False
    except:
        return False


def calculate_trust_score(fake_prob, objects, location_score, duplicate) -> int:
    """
    Final AI scoring logic (0 - 100)
    """
    score = 0

    score += int((1 - fake_prob) * 40)      # Image authenticity
    score += 25 if objects else 0            # Object relevance
    score += location_score                  # Geo validation
    score += 10 if not duplicate else 0      # Duplicate penalty

    return min(score, 100)


def final_decision(score: int) -> str:
    """
    Decision engine
    """
    if score >= 75:
        return "✅ AUTO APPROVED"
    elif score >= 50:
        return "⚠️ MANUAL REVIEW REQUIRED"
    else:
        return "❌ REJECTED"


# =========================================================
# FRONTEND UI
# =========================================================

@app.get("/", response_class=HTMLResponse)
def home_page():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI Complaint Validator</title>
<style>
body {
    background:#020617;
    font-family:Arial;
    color:white;
    display:flex;
    justify-content:center;
}
.container {
    width:420px;
    background:#0f172a;
    padding:25px;
    margin-top:40px;
    border-radius:12px;
}
input, select, button {
    width:100%;
    padding:10px;
    margin-top:10px;
    border-radius:6px;
}
button {
    background:#2563eb;
    border:none;
    color:white;
    font-weight:bold;
    cursor:pointer;
}
button:hover {
    background:#1d4ed8;
}
</style>
</head>

<body>
<div class="container">
<h2>🧠 AI Complaint Image Validation</h2>

<form action="/analyze" method="post" enctype="multipart/form-data">
    <label>Upload Image</label>
    <input type="file" name="file" required>

    <label>Issue Type</label>
    <select name="issue">
        <option value="garbage">Garbage</option>
        <option value="road">Road</option>
        <option value="water">Water</option>
    </select>

    <label>Latitude</label>
    <input type="number" step="any" name="lat" required>

    <label>Longitude</label>
    <input type="number" step="any" name="lon" required>

    <button type="submit">Run AI Validation</button>
</form>
</div>
</body>
</html>
"""


# =========================================================
# BACKEND API
# =========================================================

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_image(
    file: UploadFile = File(...),
    issue: str = Form(...),
    lat: float = Form(...),
    lon: float = Form(...)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    fake_prob = simulate_fake_probability()
    objects = detect_issue_objects(issue)
    location_score = calculate_location_score(lat, lon)
    duplicate = check_duplicate_image(file_path)

    trust_score = calculate_trust_score(
        fake_prob,
        objects,
        location_score,
        duplicate
    )

    decision = final_decision(trust_score)

    return f"""
<!DOCTYPE html>
<html>
<body style="background:#020617;color:white;font-family:Arial;">
<div style="width:420px;margin:40px auto;background:#0f172a;padding:25px;border-radius:12px;">

<h2>📊 AI Validation Result</h2>

<p><b>Detected Objects:</b> {objects}</p>
<p><b>Fake Probability:</b> {fake_prob * 100}%</p>
<p><b>Duplicate Image:</b> {"Yes" if duplicate else "No"}</p>
<p><b>Location Score:</b> {location_score}</p>

<h3>Trust Score: {trust_score}%</h3>
<h2>{decision}</h2>

<a href="/" style="color:#3b82f6;">🔁 Validate Another Image</a>

</div>
</body>
</html>
"""


# =========================================================
# SERVER RUN
# =========================================================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
