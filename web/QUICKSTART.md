# Quick Start Guide - QKD Simulator Web App

## ⚡ Fastest Way to Get Started

### 1. Install Node.js (if not already installed)
Download from: https://nodejs.org/
- Choose LTS version (recommended)
- Install with default settings
- Verify: Open command prompt and type `node --version`

### 2. Run Setup (One Time Only)
```bash
cd web
setup.bat
```
This automatically installs all dependencies for both frontend and backend.

### 3. Start the Application
```bash
cd web
start.bat
```
This opens two terminals automatically:
- Backend server (port 3001)
- Frontend server (port 3000)

Your browser should open automatically to `http://localhost:3000`

---

## 🎯 What You'll See

1. **Web Interface Opens** - Beautiful gradient interface with QKD Simulator
2. **Enter Parameters** - Same parameters as the desktop GUI
3. **Click "Run Simulations"** - Runs all 4 protocols at once
4. **View Results** - See side-by-side comparison of BB84, B92, E91, BBM92

---

## 🔧 Manual Setup (Alternative)

### Backend Setup
```bash
cd web/backend
npm install
npm start
```

### Frontend Setup (in a new terminal)
```bash
cd web/frontend
npm install
npm start
```

---

## 📱 Accessing the Application

**Development:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001/api

**Production:**
After building (`npm run build` in frontend):
- Everything: http://localhost:3001

---

## ❓ Common Issues

### Port Already in Use
**Problem:** "Port 3000 (or 3001) is already in use"

**Solution:**
```bash
# Kill the process using the port
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

### Cannot Find Module
**Problem:** "Cannot find module 'express'" or similar

**Solution:**
```bash
cd web/backend
rm -rf node_modules
npm install
```

### Python Simulator Not Found
**Problem:** Backend can't find `qkd_simulator.py`

**Solution:** Make sure your folder structure is:
```
QKD Simulator Code/
├── qkd_simulator.py  ← Must be here
├── web/
│   ├── backend/
│   └── frontend/
```

---

## 🎨 Features

✅ All 4 QKD protocols (BB84, B92, E91, BBM92)  
✅ Real-time simulation with actual Python backend  
✅ Responsive design (works on mobile/tablet)  
✅ Beautiful gradient UI  
✅ Side-by-side protocol comparison  
✅ Detailed metrics for each protocol  

---

## 🚀 Next Steps

1. Try running simulations with different parameters
2. Enable/disable eavesdropping to see QBER changes
3. Adjust fiber length to see distance effects
4. Compare protocols side-by-side

---

## 📞 Need Help?

Check the full documentation in `web/README.md`

Enjoy your QKD Simulator! 🔐✨
