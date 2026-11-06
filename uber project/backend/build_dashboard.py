"""
build_dashboard.py
==================
Builds the standalone React application by injecting uber_data.json
into app_template.html and saving to frontend/uber_react_app.html and frontend/index.html.
Can be executed from project root or backend folder.
"""

from pathlib import Path
import shutil

# Resolve base directories
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name.lower() == "backend" else SCRIPT_DIR
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# File paths
TEMPLATE_PATH = FRONTEND_DIR / "app_template.html"
if not TEMPLATE_PATH.exists():
    TEMPLATE_PATH = SCRIPT_DIR / "app_template.html"

DATA_PATH = BACKEND_DIR / "uber_data.json"
if not DATA_PATH.exists():
    DATA_PATH = SCRIPT_DIR / "uber_data.json"

OUTPUT_HTML_PATH = FRONTEND_DIR / "uber_react_app.html"
INDEX_HTML_PATH = FRONTEND_DIR / "index.html"

print(f"Reading template from: {TEMPLATE_PATH}")
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template = f.read()

print(f"Reading data from:     {DATA_PATH}")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = f.read()

output = template.replace("/*__UBER_DATA_PLACEHOLDER__*/", data)

print(f"Writing dashboard to:  {OUTPUT_HTML_PATH}")
with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(output)

# Also update index.html entry point
with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(output)

print(f"SUCCESS: Generated uber_react_app.html & index.html successfully! Size: {len(output):,} bytes.")
