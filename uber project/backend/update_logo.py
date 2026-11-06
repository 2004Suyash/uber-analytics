# update_logo.py
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name.lower() == "backend" else SCRIPT_DIR
TARGET_PATH = PROJECT_ROOT / "frontend" / "uber_react_app.html"

if not TARGET_PATH.exists():
    TARGET_PATH = SCRIPT_DIR / "uber_react_app.html"

with open(TARGET_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'\{\/\* Brand Logo & Title \*\/\}[\s\S]*?<nav'

replacement = '''{/* Official Uber Brand Logo & Title (Clean, Subtitle Removed) */}
                <div className="flex items-center space-x-3">
                  {/* Official Uber Black App Badge */}
                  <div className="flex items-center justify-center w-11 h-11 rounded-xl bg-black border border-slate-700/70 shadow-lg shadow-black/40 shrink-0 select-none">
                    <span className="text-white font-black text-sm tracking-tight font-sans">Uber</span>
                  </div>
                  <div className="flex items-center space-x-2.5">
                    <h1 className={`text-lg font-extrabold tracking-tight ${textPrimary}`}>
                      Uber Analytics
                    </h1>
                    <span className="bg-emerald-500/10 text-emerald-500 text-[10px] font-semibold px-2 py-0.5 rounded-full border border-emerald-500/30">
                      React 18 Active
                    </span>
                  </div>
                </div>

                {/* Tab Navigation */}
                <nav'''

new_content = re.sub(pattern, replacement, content)

if new_content != content:
    with open(TARGET_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Brand header updated cleanly!")
else:
    print("Pattern already updated or not matched")
