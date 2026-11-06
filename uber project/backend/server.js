/**
 * backend/server.js
 * =================
 * Dedicated Backend REST API Server for Uber Analytics.
 * Default Port: 5000
 *
 * Endpoints:
 *   GET /api/health  - Health & uptime status
 *   GET /api/rides   - Full dataset of 1,154 verified Uber rides
 *   GET /api/stats   - Summary metrics (miles, duration, categories, purposes)
 *   GET /            - API Index & status info
 *
 * Run separately:
 *   cd backend && npm run dev
 *   or: node backend/server.js
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = parseInt(process.env.PORT || '5000', 10);
const DATA_FILE = path.join(__dirname, 'uber_data.json');

// Cache trip data in memory
let cachedData = null;
function getUberData() {
  if (!cachedData && fs.existsSync(DATA_FILE)) {
    try {
      const raw = fs.readFileSync(DATA_FILE, 'utf8');
      cachedData = JSON.parse(raw);
    } catch (err) {
      console.error('[BACKEND] Error reading uber_data.json:', err.message);
    }
  }
  return cachedData || [];
}

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host}`);
  const pathname = parsedUrl.pathname;

  // CORS Headers for cross-origin frontend requests
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Root / API Index Info
  if (pathname === '/' || pathname === '/api') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=UTF-8' });
    res.end(JSON.stringify({
      service: 'Uber Analytics Backend REST API',
      status: 'active',
      port: PORT,
      endpoints: {
        health: `http://localhost:${PORT}/api/health`,
        stats: `http://localhost:${PORT}/api/stats`,
        rides: `http://localhost:${PORT}/api/rides`
      },
      frontendDevUrl: 'http://localhost:3000/'
    }, null, 2));
    return;
  }

  // Health Endpoint
  if (pathname === '/api/health') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=UTF-8' });
    res.end(JSON.stringify({
      status: 'ok',
      service: 'Uber Analytics Backend',
      port: PORT,
      timestamp: new Date().toISOString(),
      uptimeSeconds: Math.floor(process.uptime())
    }));
    return;
  }

  // Rides Data Endpoint
  if (pathname === '/api/rides') {
    const data = getUberData();
    res.writeHead(200, { 'Content-Type': 'application/json; charset=UTF-8' });
    res.end(JSON.stringify({ total: data.length, rides: data }));
    return;
  }

  // Summary Statistics Endpoint
  if (pathname === '/api/stats') {
    const data = getUberData();
    const totalTrips = data.length;
    const totalMiles = data.reduce((acc, r) => acc + (Number(r.Miles) || 0), 0);
    const totalDuration = data.reduce((acc, r) => acc + (Number(r.Duration_Minutes) || 0), 0);
    const categories = {};
    const purposes = {};

    data.forEach(r => {
      const cat = r.Category || 'Unknown';
      categories[cat] = (categories[cat] || 0) + 1;
      const purp = r.Purpose || 'Not Specified';
      purposes[purp] = (purposes[purp] || 0) + 1;
    });

    res.writeHead(200, { 'Content-Type': 'application/json; charset=UTF-8' });
    res.end(JSON.stringify({
      totalTrips,
      totalMiles: Math.round(totalMiles * 10) / 10,
      totalDurationMinutes: Math.round(totalDuration),
      avgMilesPerTrip: totalTrips ? Math.round((totalMiles / totalTrips) * 10) / 10 : 0,
      categoryBreakdown: categories,
      topPurposes: purposes
    }));
    return;
  }

  // 404 for unknown endpoints
  res.writeHead(404, { 'Content-Type': 'application/json; charset=UTF-8' });
  res.end(JSON.stringify({ error: 'Endpoint not found', path: pathname }));
});

server.listen(PORT, () => {
  console.log(`[BACKEND] 🚀 REST API Server running on \x1b[35mhttp://localhost:${PORT}\x1b[0m`);
  console.log(`[BACKEND]    • Health: http://localhost:${PORT}/api/health`);
  console.log(`[BACKEND]    • Stats:  http://localhost:${PORT}/api/stats`);
  console.log(`[BACKEND]    • Rides:  http://localhost:${PORT}/api/rides`);
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`[BACKEND] ❌ Port ${PORT} is in use. Run with PORT=${PORT + 1}`);
  } else {
    console.error('[BACKEND] Server error:', err);
  }
});
