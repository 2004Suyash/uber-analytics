/**
 * dev.js
 * ======
 * Concurrent Development Runner for Uber Analytics.
 * Launches BOTH Frontend (Port 3000) and Backend (Port 5000) concurrently.
 *
 * Usage:
 *   npm run dev
 *   npm run dev:open
 */

const { spawn, exec } = require('child_process');
const path = require('path');

const shouldOpen = process.argv.includes('--open') || process.env.OPEN === 'true';

console.log('\n\x1b[1m\x1b[34m==============================================================\x1b[0m');
console.log('\x1b[1m  UBER ANALYTICS: RUNNING FRONTEND + BACKEND CONCURRENTLY\x1b[0m');
console.log('\x1b[1m\x1b[34m==============================================================\x1b[0m');
console.log('  \x1b[36m[FRONTEND]\x1b[0m Dashboard:  \x1b[4mhttp://localhost:3000/\x1b[0m');
console.log('  \x1b[35m[BACKEND]\x1b[0m  REST API:   \x1b[4mhttp://localhost:5000/api/stats\x1b[0m');
console.log('\x1b[1m\x1b[34m==============================================================\x1b[0m');
console.log('  Press \x1b[33mCtrl + C\x1b[0m to stop both servers at any time.\n');

// 1. Start Backend on Port 5000
const backend = spawn(process.execPath, [path.join(__dirname, 'backend', 'server.js')], {
  env: { ...process.env, PORT: '5000' },
  stdio: ['pipe', 'pipe', 'pipe']
});

backend.stdout.on('data', (data) => {
  process.stdout.write(data.toString());
});

backend.stderr.on('data', (data) => {
  process.stderr.write(`\x1b[31m[BACKEND ERROR]\x1b[0m ${data.toString()}`);
});

// 2. Start Frontend on Port 3000
const frontend = spawn(process.execPath, [path.join(__dirname, 'frontend', 'server.js')], {
  env: { ...process.env, PORT: '3000', BACKEND_PORT: '5000' },
  stdio: ['pipe', 'pipe', 'pipe']
});

frontend.stdout.on('data', (data) => {
  process.stdout.write(data.toString());
});

frontend.stderr.on('data', (data) => {
  process.stderr.write(`\x1b[31m[FRONTEND ERROR]\x1b[0m ${data.toString()}`);
});

// Optional: Auto-open browser
if (shouldOpen) {
  setTimeout(() => {
    const url = 'http://localhost:3000/';
    const cmd = process.platform === 'win32' ? `start "" "${url}"` :
                process.platform === 'darwin' ? `open "${url}"` : `xdg-open "${url}"`;
    exec(cmd);
  }, 800);
}

// Clean shutdown on Ctrl + C
function cleanShutdown() {
  console.log('\n\x1b[33mStopping both Frontend and Backend servers...\x1b[0m');
  try { backend.kill('SIGTERM'); } catch (e) {}
  try { frontend.kill('SIGTERM'); } catch (e) {}
  setTimeout(() => process.exit(0), 300);
}

process.on('SIGINT', cleanShutdown);
process.on('SIGTERM', cleanShutdown);

