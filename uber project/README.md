# Uber Ride Analytics & Intelligence Platform

A modular fullstack data intelligence application with fully separated **Frontend** and **Backend** architectures.

---

## ⚡ Developer Execution Commands

### 1. Run Both Together (Concurrently)
From the project root:
```bash
npm run dev
```
*(Or auto-open browser: `npm run dev:open`)*

| Service | Port | Local URL |
| :--- | :--- | :--- |
| **Frontend UI** | `3000` | [http://localhost:3000/](http://localhost:3000/) |
| **Backend REST API** | `5000` | [http://localhost:5000/api/stats](http://localhost:5000/api/stats) |

---

### 2. Run Separately (In Different Terminals)

#### Option A: Run from Project Root
- **Frontend Only (Port 3000):**
  ```bash
  npm run dev:frontend
  ```
- **Backend Only (Port 5000):**
  ```bash
  npm run dev:backend
  ```

#### Option B: Run Inside Their Respective Folders
- **Terminal 1 (Frontend):**
  ```bash
  cd frontend
  npm run dev
  ```
- **Terminal 2 (Backend):**
  ```bash
  cd backend
  npm run dev
  ```

---

## 📁 Project Architecture

```
d:\uber project\
│
├── frontend/                                   # All Frontend UI & Client Assets
│   ├── server.js                               # Dedicated Frontend server (Port 3000)
│   ├── package.json                            # Frontend npm scripts
│   ├── index.html                              # Primary web entry point (React 18 Dashboard)
│   ├── uber_react_app.html                     # Interactive React 18 single-page dashboard
│   ├── uber_powerbi_dashboard.html             # Power BI operational report view
│   ├── Uber_Analysis_Executive_Report.html     # Executive report launcher
│   ├── app_template.html                       # HTML template for automated dashboard builds
│   ├── uber_data.js                            # Client-side trip data script
│   ├── check_syntax.js                         # React component & syntax validator
│   └── README.md                               # Frontend documentation
│
├── backend/                                    # All Backend Analytics, Data & Services
│   ├── server.js                               # Dedicated REST API server (Port 5000)
│   ├── server.py                               # Lightweight Python alternative server (Port 5000)
│   ├── package.json                            # Backend npm scripts
│   ├── uber_analysis.py                        # Python data cleaning, feature engineering & EDA
│   ├── build_dashboard.py                      # Automated dashboard builder script
│   ├── update_logo.py                          # Branding / UI updater script
│   ├── uberproject (1).ipynb                   # Jupyter Notebook exploratory data analysis
│   ├── requirements.txt                        # Python dependencies
│   ├── UberDataset (1).csv                     # Raw Uber ride records dataset
│   ├── Uber_Cleaned_PowerBI.csv                # Cleaned dataset for Power BI analytics
│   ├── Uber_Analysis_Concluded_Datasheet.csv   # Consolidated analytical datasheet
│   ├── uber_data.json                          # JSON formatted dataset for web applications
│   ├── uber_analysis_charts.png                # Visual EDA chart figures
│   └── README.md                               # Backend documentation
│
├── dev.js                                      # Root orchestrator: runs Frontend + Backend concurrently
├── index.html                                  # Root launcher redirecting to frontend/
├── package.json                                # Master package.json with developer runners
├── .gitignore                                  # Git ignore rules
└── README.md                                   # This file
```

---

## 🌐 API Reference (Backend)

When the backend is running on `http://localhost:5000`:
- **`GET /api/health`** — Backend status and uptime.
- **`GET /api/stats`** — High-level metrics (total trips, miles, categories, top purposes).
- **`GET /api/rides`** — Complete list of 1,154 verified Uber ride objects.
