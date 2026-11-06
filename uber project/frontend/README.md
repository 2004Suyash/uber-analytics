# Frontend - Uber Analytics Dashboard

Dedicated client-side UI dashboard server running on **Port 3000**.

## 🚀 Running Frontend Separately

```bash
# From frontend folder:
npm run dev

# Or from project root:
npm run dev:frontend
```

Opens at: [http://localhost:3000/](http://localhost:3000/)

- Automatically proxies `/api/*` requests to the Backend server on port `5000`.
- If the backend server is offline, falls back to the embedded data in `uber_data.js`.
