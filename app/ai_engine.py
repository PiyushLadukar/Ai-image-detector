import random
import imagehash
import os
from PIL import Image

def fake_probability():
    return round(random.uniform(0.05, 0.40), 2)

def detect_objects(issue):
    ISSUE_DB = {
        "garbage": ["plastic", "trash", "waste"],
        "road": ["pothole", "crack"],
        "water": ["leak", "pipe"]
    }
    return random.sample(ISSUE_DB.get(issue, []), 1)

def location_score(lat, lon):
    return 20 if 8 <= lat <= 37 and 68 <= lon <= 97 else 5

def is_duplicate(image_path, upload_dir):
    new_hash = imagehash.phash(Image.open(image_path))

    for file in os.listdir(upload_dir):
        path = os.path.join(upload_dir, file)
        if path == image_path:
            continue
        try:
            old_hash = imagehash.phash(Image.open(path))
            if abs(old_hash - new_hash) <= 5:
                return True
        except:
            continue
    return False

def trust_score(fake_prob, objects, duplicate):
    score = int((1 - fake_prob) * 50)   
    score += 30 if objects else 0       
    score += 20 if not duplicate else 0 
    return min(score, 100)

def decision(score):
    if score >= 75:
        return "✅ AUTO APPROVED"
    elif score >= 50:
        return "⚠️ MANUAL REVIEW"
    else:
        return "❌ REJECTED"
