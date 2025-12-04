# 🚀 How to Start AlignAI - Complete Guide

## ⚡ **Quick Start (3 Easy Steps)**

### **Step 1: Start Servers**

**Double-click this file:**
```
START_SERVERS.bat
```

This will open **two terminal windows**:
- ✅ Backend Server (Port 5000)
- ✅ Frontend Server (Port 8000)

**Keep both windows open!**

---

### **Step 2: Open Browser**

**Open this URL in your browser:**
```
http://localhost:8000/index.html
```

**⚠️ IMPORTANT:** Must use `http://localhost:8000/` (not file://)

---

### **Step 3: Login**

1. Click "Start Aligning Now"
2. Login or Sign Up
3. Enjoy your dashboard! ✨

---

## 📋 **Manual Start (Alternative)**

If batch file doesn't work, start manually:

### **Terminal 1 - Backend:**
```powershell
cd C:\Users\monib\Desktop\resumetailoring
python auth.py
```

Keep this window open! You should see:
```
✅ PostgreSQL connection successful!
✅ Database tables created successfully!
🔐 AlignAI Authentication Server with PostgreSQL
📍 Server: http://localhost:5000
```

---

### **Terminal 2 - Frontend:**

**Open a NEW terminal window**, then:

```powershell
cd C:\Users\monib\Desktop\resumetailoring
python start_frontend.py
```

Keep this window open too! You should see:
```
🌐 AlignAI Frontend Server
📍 Server running at: http://localhost:8000
```

---

## 🌐 **URLs to Use**

| Page | URL |
|------|-----|
| **Homepage** | http://localhost:8000/index.html |
| **Login** | http://localhost:8000/login.html |
| **Dashboard** | http://localhost:8000/dashboard.html |

---

## ✅ **Verification Checklist**

Before using the app, verify:

- [ ] Backend running (you see terminal with port 5000)
- [ ] Frontend running (you see terminal with port 8000)
- [ ] PostgreSQL running (started earlier)
- [ ] Browser opened to http://localhost:8000/

---

## 🐛 **Troubleshooting**

### **Problem: "Port already in use"**

**Solution:** Kill existing processes

```powershell
# Kill backend (port 5000)
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | 
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

# Kill frontend (port 8000)
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | 
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

Then start again with `START_SERVERS.bat`

---

### **Problem: "Can't connect to database"**

**Solution:** Start PostgreSQL

```powershell
& "C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" start
```

---

### **Problem: Still redirected to login after signin**

**Check:**
1. ✅ Using http://localhost:8000/ (not file://)
2. ✅ Both servers running
3. ✅ Not in incognito/private mode

**Full reset:**
```powershell
# 1. Stop all servers
taskkill /F /IM python.exe

# 2. Start PostgreSQL
& "C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" start

# 3. Start servers
.\START_SERVERS.bat

# 4. Open browser
start http://localhost:8000/index.html
```

---

## 📊 **What Each Server Does**

### **Backend Server (Port 5000)**
- File: `auth.py`
- Purpose:
  - Handles login/signup
  - Manages sessions
  - Connects to PostgreSQL
  - API endpoints

### **Frontend Server (Port 8000)**
- File: `start_frontend.py`
- Purpose:
  - Serves HTML/CSS/JS files
  - Enables cookies (HTTP protocol)
  - Provides proper CORS headers

### **Why Two Servers?**

**Browsers block cookies on `file://` protocol!**

❌ `file:///C:/Users/.../login.html` - No cookies  
✅ `http://localhost:8000/login.html` - Cookies work!

Without cookies → No sessions → Can't stay logged in!

---

## 🎯 **Complete Startup Sequence**

```
1. Start PostgreSQL
   ↓
2. Start Backend (auth.py)
   ↓
3. Start Frontend (start_frontend.py)
   ↓
4. Open http://localhost:8000/index.html
   ↓
5. Login/Signup
   ↓
6. Dashboard loads ✅
```

---

## 💡 **Pro Tips**

### **Tip 1: Keep Terminals Open**

Don't close the terminal windows! The servers are running there.

### **Tip 2: Check Server Status**

**Backend:**
```powershell
curl http://localhost:5000/api/admin/stats
```

**Frontend:**
```powershell
curl http://localhost:8000/
```

### **Tip 3: View Logs**

Watch the terminal windows for:
- Login attempts
- Errors
- Database queries

### **Tip 4: Stop Servers**

Press `Ctrl+C` in each terminal window

Or close the terminal windows

---

## 📚 **Files Created**

| File | Purpose |
|------|---------|
| `START_SERVERS.bat` | Start both servers |
| `start_frontend.py` | Frontend HTTP server |
| `auth.py` | Backend API server |
| `dashboard.html` | Dashboard page |
| `login.html` | Login/signup page |
| `index.html` | Homepage |

---

## 🎉 **Success!**

If you see:
- ✅ Your name in dashboard navbar
- ✅ Welcome message
- ✅ Stats showing your account
- ✅ Logout button works

**Your authentication system is working perfectly!** 🎊

---

## 📞 **Need More Help?**

Check these guides:
- `Guides/SESSION_COOKIE_FIX.md` - Why we need two servers
- `Guides/POSTGRESQL_QUICK_SETUP.md` - Database setup
- `Guides/RESET_POSTGRES_PASSWORD.md` - Password issues
- `Guides/README.md` - All documentation

---

## ⚡ **Remember:**

**Always use:** `http://localhost:8000/`  
**Never use:** `file:///...`

**Keep both server windows open while using the app!**

---

**Happy coding!** 🚀✨

