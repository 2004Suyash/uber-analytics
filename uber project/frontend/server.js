/**
 * frontend/server.js
 * ==================
 * Dedicated Frontend HTTP Server for Uber Analytics Dashboard.
 * Default Port: 3000
 *
 * Serves the React 18 single-page dashboard and static assets.
 * Automatically proxies any '/api/*' requests to the Backend server on port 5000.
 *
 * Run separately:
 *   cd frontend && npm run dev
 *   or: node frontend/server.js
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PORT = parseInt(process.env.PORT || '3000', 10);
const BACKEND_PORT = parseInt(process.env.BACKEND_PORT || '5000', 10);
const FRONTEND_DIR = __dirname;
const shouldOpen = process.argv.includes('--open') || process.env.OPEN === 'true';

const MIME_TYPES = {
  '.html': 'text/html; charset=UTF-8',
  '.js': 'application/javascript; charset=UTF-8',
  '.json': 'application/json; charset=UTF-8',
  '.css': 'text/css; charset=UTF-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

function openBrowser(url) {
  const cmd = process.platform === 'win32' ? `start "" "${url}"` :
              process.platform === 'darwin' ? `open "${url}"` : `xdg-open "${url}"`;
  exec(cmd, (err) => {
    if (err) console.log(`[FRONTEND] Open your browser to ${url}`);
  });
}

// Proxy API requests to backend server on port 5000
function proxyToBackend(req, res) {
  const options = {
    hostname: 'localhost',
    port: BACKEND_PORT,
    path: req.url,
    method: req.method,
    headers: req.headers
  };

  const proxyReq = http.request(options, (backendRes) => {
    res.writeHead(backendRes.statusCode, backendRes.headers);
    backendRes.pipe(res, { end: true });
  });

  proxyReq.on('error', () => {
    res.writeHead(503, { 'Content-Type': 'application/json; charset=UTF-8' });
    res.end(JSON.stringify({
      error: 'Backend API unavailable',
      message: `Backend server is not running on port ${BACKEND_PORT}. Run 'npm run dev:backend' to start it.`,
      fallback: 'Frontend is running using local embedded dataset.'
    }));
  });

  req.pipe(proxyReq, { end: true });
}

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host}`);
  const pathname = parsedUrl.pathname;

  // Route API calls to backend proxy
  if (pathname.startsWith('/api/')) {
    proxyToBackend(req, res);
    return;
  }

  // Determine requested static file
  let filePath;
  if (pathname === '/' || pathname === '/index.html') {
    filePath = path.join(FRONTEND_DIR, 'uber_react_app.html');
    if (!fs.existsSync(filePath)) {
      filePath = path.join(FRONTEND_DIR, 'index.html');
    }
  } else {
    const safePath = path.normalize(pathname).replace(/^(\.\.[\/\\])+/, '');
    filePath = path.join(FRONTEND_DIR, safePath);
  }

  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath).toLowerCase();
    const mime = MIME_TYPES[ext] || 'application/octet-stream';
    res.writeHead(200, {
      'Content-Type': mime,
      'Cache-Control': 'no-cache, no-store, must-revalidate'
    });
    fs.createReadStream(filePath).pipe(res);
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=UTF-8' });
    res.end('404 Not Found: ' + pathname);
  }
});

server.listen(PORT, () => {
  const localUrl = `http://localhost:${PORT}/`;
  console.log(`[FRONTEND] 🌐 UI Dashboard Server running on \x1b[36m${localUrl}\x1b[0m`);
  console.log(`[FRONTEND]    • Connected API proxy -> http://localhost:${BACKEND_PORT}/api/*`);

  if (shouldOpen) {
    openBrowser(localUrl);
  }
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`[FRONTEND] ❌ Port ${PORT} is in use. Run with PORT=${PORT + 1}`);
  } else {
    console.error('[FRONTEND] Server error:', err);
  }
});

