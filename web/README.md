# QKD Simulator - Web Application

A modern web application for simulating Quantum Key Distribution (QKD) protocols, built with React and Node.js.

## 🚀 Features

- **Interactive Web Interface**: Clean, modern UI for parameter input and result visualization
- **All 4 Protocols**: Simultaneously runs BB84, B92, E91, and BBM92 protocols
- **Real-time Results**: Live simulation results with detailed metrics
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real Python Backend**: Uses the actual QKD simulator engine

## 🏗️ Architecture

```
web/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.js
│   │   │   ├── SimulatorForm.js
│   │   │   └── ResultsDisplay.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
└── backend/           # Node.js Express server
    ├── server.js      # Main server file
    └── package.json
```

## 📋 Prerequisites

1. **Node.js** (v16 or higher)
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify: `node --version`

2. **Python** (3.8 or higher)
   - Already installed with your QKD simulator
   - Verify: `python --version`

3. **npm** (comes with Node.js)
   - Verify: `npm --version`

## 🛠️ Installation

### Step 1: Install Backend Dependencies

```bash
cd web/backend
npm install
```

This installs:
- `express` - Web server framework
- `cors` - Cross-origin resource sharing

### Step 2: Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

This installs:
- `react` & `react-dom` - UI framework
- `axios` - HTTP client
- `recharts` - Charting library

## 🚀 Running the Application

### Option 1: Development Mode (Recommended for Testing)

**Terminal 1 - Start Backend Server:**
```bash
cd web/backend
npm start
```
Backend runs on: `http://localhost:3001`

**Terminal 2 - Start React Development Server:**
```bash
cd web/frontend
npm start
```
Frontend runs on: `http://localhost:3000`

**Open your browser to:** `http://localhost:3000`

### Option 2: Production Mode

**Build the React app:**
```bash
cd web/frontend
npm run build
```

**Start the backend (serves both API and frontend):**
```bash
cd ../backend
npm start
```

**Open your browser to:** `http://localhost:3001`

## 💻 Usage

1. **Enter Parameters**
   - Adjust system parameters (source rate, fiber length, etc.)
   - Configure simulation settings (number of qubits, enables/disables)

2. **Run Simulation**
   - Click "Run Simulations for All Protocols"
   - Wait for all 4 protocols to complete

3. **View Results**
   - Compare results across all protocols
   - Review key metrics (key length, key rate, QBER, etc.)

## 📊 API Endpoints

### `GET /api/health`
Health check endpoint
```json
{ "status": "ok", "message": "Node.js backend is running" }
```

### `POST /api/simulate/all`
Run simulations for all 4 protocols

**Request Body:**
```json
{
  "source_rate": 72.6,
  "source_efficiency": 0.05,
  "fiber_length": 18.0,
  "fiber_loss": 0.53,
  "detector_efficiency": 0.11,
  "perturb_prob": 0.05,
  "sop_deviation": 0.13,
  "n_qubits": 100000,
  "qber_fraction": 0.1,
  "losses_enabled": true,
  "perturb_enabled": true,
  "eavesdropping": false,
  "sop_enabled": true
}
```

**Response:**
```json
{
  "success": true,
  "results": {
    "BB84": { "key_length": 12345, "key_rate": 4321.0, ... },
    "B92": { ... },
    "E91": { ... },
    "BBM92": { ... }
  }
}
```

### `POST /api/simulate/:protocol`
Run simulation for a single protocol (BB84, B92, E91, or BBM92)

## 🔧 Configuration

### Change Backend Port

Edit `web/backend/server.js`:
```javascript
const PORT = process.env.PORT || 3001;
```

### Change Frontend API Proxy

Edit `web/frontend/package.json`:
```json
"proxy": "http://localhost:3001"
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :3001
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3001 | xargs kill -9
```

### Cannot Find Python Module
Make sure the Python simulator is in the parent directory:
```
QKD Simulator Code/
├── qkd_simulator.py
├── web/
│   ├── backend/
│   └── frontend/
```

### CORS Errors
Backend has CORS enabled. Check that:
1. Backend is running on port 3001
2. Frontend proxy is correctly configured

### Installation Errors
Clear npm cache and reinstall:
```bash
npm cache clean --force
rm -rf node_modules
rm package-lock.json
npm install
```

## 📦 Production Deployment

### Build for Production

```bash
# Build frontend
cd web/frontend
npm run build

# The build folder will be created with optimized files
# Backend automatically serves this in production mode
```

### Environment Variables

Create `.env` file in backend folder:
```
PORT=3001
NODE_ENV=production
```

## 🎨 Customization

### Styling
- Edit CSS files in `web/frontend/src/components/`
- Main theme colors in gradient: `#667eea` to `#764ba2`

### Add New Features
- Add components in `web/frontend/src/components/`
- Extend API in `web/backend/server.js`

## 📝 Notes

- **Performance**: Large simulations (>1M qubits) may take several minutes
- **Browser Compatibility**: Tested on Chrome, Firefox, Safari, Edge
- **Mobile Support**: Fully responsive design

## 🤝 Credits

Based on research by Erik Åkerberg & Erik Åsgrim (2023)  
KTH Royal Institute of Technology

## 📄 License

Educational use - Please cite the original research paper.
