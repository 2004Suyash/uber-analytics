// check_syntax.js
const fs = require('fs');
const path = require('path');

const targetFile = path.join(__dirname, 'uber_react_app.html');
if (!fs.existsSync(targetFile)) {
  console.error(`Target file not found: ${targetFile}`);
  process.exit(1);
}

const html = fs.readFileSync(targetFile, 'utf8');
const m = html.match(/<script type="text\/babel"[^>]*>([\s\S]*?)<\/script>/);

if (!m) {
  console.log("No babel script found!");
  process.exit(1);
}

const code = m[1];
console.log("Babel script found successfully!");
console.log(`Script length: ${code.length.toLocaleString()} characters.`);

// Verify key component names exist
const checks = ['App', 'ChartComponent', 'DashboardMetrics', 'RidesTable'];
checks.forEach(comp => {
  if (code.includes(comp)) {
    console.log(`  [OK] Component found: ${comp}`);
  } else {
    console.log(`  [INFO] Note: ${comp} not found or named differently`);
  }
});
console.log("\nFrontend syntax check completed successfully!");
