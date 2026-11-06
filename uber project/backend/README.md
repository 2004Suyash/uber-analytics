# Backend - Uber Analytics REST API & Pipelines

Dedicated REST API server running on **Port 5000**.

## 🚀 Running Backend Separately

### Node.js REST API Server:
```bash
# From backend folder:
npm run dev

# Or from project root:
npm run dev:backend
```

Opens at: [http://localhost:5000/api/stats](http://localhost:5000/api/stats)

### Python Alternative Server:
```bash
python server.py
# Or from project root:
npm run start:backend:py
```

## 🌐 Endpoints
- `GET /api/health`
- `GET /api/stats`
- `GET /api/rides`
