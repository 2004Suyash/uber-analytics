"""
backend/server.py
=================
Lightweight Python HTTP server using built-in standard library.
Serves frontend dashboard and provides REST API endpoints.

Usage:
    python backend/server.py
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from pathlib import Path
from urllib.parse import urlparse

PORT = int(os.environ.get("PORT", 5000))
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent if BACKEND_DIR.name.lower() == "backend" else BACKEND_DIR
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_FILE = BACKEND_DIR / "uber_data.json"

class UberAnalyticsHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "backend": "Python http.server"}).encode("utf-8"))
            return

        if path == "/api/rides":
            if DATA_FILE.exists():
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"total": len(data), "rides": data}).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
            return

        if path == "/api/stats":
            if DATA_FILE.exists():
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                total_trips = len(data)
                total_miles = sum(float(r.get("Miles", 0) or 0) for r in data)
                total_duration = sum(float(r.get("Duration_Minutes", 0) or 0) for r in data)
                categories = {}
                purposes = {}
                for r in data:
                    cat = r.get("Category", "Unknown")
                    categories[cat] = categories.get(cat, 0) + 1
                    purp = r.get("Purpose", "Not Specified")
                    purposes[purp] = purposes.get(purp, 0) + 1

                stats = {
                    "totalTrips": total_trips,
                    "totalMiles": round(total_miles, 1),
                    "totalDurationMinutes": round(total_duration),
                    "avgMilesPerTrip": round(total_miles / total_trips, 1) if total_trips else 0,
                    "categoryBreakdown": categories,
                    "topPurposes": purposes
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(stats).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()
            return

        # Serve static frontend files
        if path in ("/", "/index.html"):
            target = FRONTEND_DIR / "uber_react_app.html"
            if not target.exists():
                target = FRONTEND_DIR / "index.html"
        else:
            clean_path = path.lstrip("/")
            target = FRONTEND_DIR / clean_path

        if target.exists() and target.is_file():
            ext = target.suffix.lower()
            mime = {
                ".html": "text/html; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
                ".json": "application/json; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".png": "image/png",
            }.get(ext, "application/octet-stream")

            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.end_headers()
            with open(target, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def run():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, UberAnalyticsHandler)
    print("=" * 55)
    print(f"Uber Analytics Python Backend running at:")
    print(f"  Frontend App: http://localhost:{PORT}/")
    print(f"  API Health:   http://localhost:{PORT}/api/health")
    print(f"  API Stats:    http://localhost:{PORT}/api/stats")
    print(f"  API Rides:    http://localhost:{PORT}/api/rides")
    print("=" * 55)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()

if __name__ == "__main__":
    run()

