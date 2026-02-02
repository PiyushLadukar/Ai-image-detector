

HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Image Validator</title>

<style>
:root {
    --bg-main: #020617;
    --bg-card: #0f172a;
    --primary: #2563eb;
    --accent: #38bdf8;
    --text: #e5e7eb;
}

* {
    box-sizing: border-box;
    font-family: "Segoe UI", Arial, sans-serif;
}

body {
    margin: 0;
    min-height: 100vh;
    background: radial-gradient(circle at top, #020617, #000);
    display: flex;
    justify-content: center;
    align-items: center;
    color: var(--text);
}

.card {
    width: 430px;
    background: var(--bg-card);
    padding: 28px;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
}

h2 {
    text-align: center;
    margin-bottom: 6px;
}

.subtitle {
    text-align: center;
    font-size: 14px;
    opacity: 0.75;
    margin-bottom: 22px;
}

label {
    font-size: 14px;
    margin-top: 14px;
    display: block;
}

input, select {
    width: 100%;
    padding: 12px;
    margin-top: 6px;
    border-radius: 10px;
    border: none;
    background: #020617;
    color: white;
}

button {
    width: 100%;
    padding: 13px;
    margin-top: 22px;
    border-radius: 12px;
    border: none;
    font-weight: bold;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    color: white;
    cursor: pointer;
}
</style>
</head>

<body>
<div class="card">
    <h2>🧠 AI Image Validator</h2>
    <div class="subtitle">Upload image and analyze with AI</div>

    <form action="/analyze" method="post" enctype="multipart/form-data">
        <label>📷 Upload Image</label>
        <input type="file" name="file" accept="image/*" required>

        <label>⚠️ Issue Type</label>
        <select name="issue" required>
            <option value="garbage">Garbage</option>
            <option value="road">Road</option>
            <option value="water">Water</option>
        </select>

        <button type="submit">🚀 Analyze</button>
    </form>
</div>
</body>
</html>
"""



def result_page(objects, fake, duplicate, score, decision):
    color = "#22c55e" if score >= 75 else "#facc15" if score >= 50 else "#ef4444"

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Result</title>

<style>
body {{
    margin: 0;
    min-height: 100vh;
    background: #020617;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: Arial;
    color: white;
}}

.card {{
    width: 430px;
    background: #0f172a;
    padding: 28px;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
}}

.stat {{
    background: #020617;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
}}

.score {{
    margin-top: 18px;
    font-size: 26px;
    text-align: center;
    color: {color};
}}

a {{
    display: block;
    margin-top: 22px;
    text-align: center;
    text-decoration: none;
    font-weight: bold;
    color: #38bdf8;
}}
</style>
</head>

<body>
<div class="card">
    <h2>📊 AI Analysis Result</h2>

    <div class="stat"><b>Detected Objects:</b> {objects}</div>
    <div class="stat"><b>Fake Probability:</b> {round(fake * 100, 2)}%</div>
    <div class="stat"><b>Duplicate Image:</b> {"Yes" if duplicate else "No"}</div>

    <div class="score">Trust Score: {score}%</div>
    <h3 style="text-align:center;">{decision}</h3>

    <a href="/">🔁 Analyze Another Image</a>
</div>
</body>
</html>
"""
