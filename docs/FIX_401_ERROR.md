# 🔧 Fix 401 Unauthorized Error - Complete Guide

## 🎯 The Problem

You're getting these errors:
```
GET http://localhost:5001/api/resume/list 401 (UNAUTHORIZED)
POST http://localhost:5001/api/resume/upload 401 (UNAUTHORIZED)
```

This happens because the **API server (port 5001)** cannot verify your authentication from the **Auth server (port 5000)**.

---

## ✅ The Solution - Step by Step

### Step 1: Stop All Running Servers

**Option A: Use PowerShell Script (RECOMMENDED)**
```powershell
.\restart_servers.ps1
```
This script will:
- Kill all Python processes using ports 5000, 5001, 8000
- Clear the ports
- Restart all servers in the correct order

**Option B: Manual Method**
1. Open PowerShell as Administrator
2. Run these commands:
```powershell
# Find processes using the ports
netstat -ano | findstr "5000"
netstat -ano | findstr "5001"
netstat -ano | findstr "8000"

# Kill each process (replace PID with actual number from above)
taskkill /PID [PID] /F
```

---

### Step 2: Verify PostgreSQL is Running

```powershell
Get-Service -Name postgresql*
```

If it says "Stopped", start it:
```powershell
Start-Service -Name postgresql-x64-16
```

---

### Step 3: Start Servers in Correct Order

**Open 3 separate PowerShell windows:**

**Window 1 - Auth Server:**
```powershell
cd C:\Users\monib\Desktop\resumetailoring
python auth.py
```
Wait for: `Running on http://127.0.0.1:5000`

**Window 2 - API Server:**
```powershell
cd C:\Users\monib\Desktop\resumetailoring
python api.py
```
Wait for: `Running on http://127.0.0.1:5001`

**Window 3 - Frontend:**
```powershell
cd C:\Users\monib\Desktop\resumetailoring
python start_frontend.py
```
Wait for: `Serving HTTP on 0.0.0.0 port 8000`

---

### Step 4: Clear Browser Data

**CRITICAL: You must clear cookies for the fix to work!**

1. Open Chrome/Edge
2. Press `Ctrl + Shift + Delete`
3. Select:
   - ✅ Cookies and other site data
   - ✅ Cached images and files
4. Time range: **All time**
5. Click "Clear data"

**OR** Use our tool:
1. Go to: `http://localhost:8000/clear-session.html`
2. Click "Clear Everything"

---

### Step 5: Test Authentication

1. Open: `http://localhost:8000/test-auth.html`
2. Click each button in order:
   - "🔍 Check All Servers" - All should show ONLINE
   - "🍪 Check Cookies" - Should show NO COOKIES (normal before login)
   - "🔐 Test Auth Server" - Will show NOT AUTHENTICATED
   - "📡 Test API Server" - Will show NOT AUTHENTICATED

3. Click "🔑 Go to Login"
4. Login with your credentials
5. After successful login, go back to test page
6. Run tests again - ALL should show ✅ AUTHENTICATED

---

### Step 6: Test Resume Upload

1. Go to: `http://localhost:8000/dashboard.html`
2. Try uploading a resume in the top-right panel
3. Watch the **PowerShell window running api.py** for logs
4. You should see:
```
📤 UPLOAD REQUEST RECEIVED

============================================================
🔐 AUTHENTICATION CHECK
============================================================
📨 Cookies received: ['alignai_session']
📡 Verifying with auth server...
📊 Auth server status: 200
✅ Authenticated user: your@email.com
✅ User found in database: ID 1
============================================================
```

---

## 🐛 Troubleshooting

### Problem: "Cannot connect to auth server"
**Solution:** Auth server (port 5000) is not running
```powershell
# In a new PowerShell window:
cd C:\Users\monib\Desktop\resumetailoring
python auth.py
```

### Problem: "Auth server returned 401"
**Solution:** Your session expired or cookies not sent
1. Clear browser cookies (Step 4)
2. Login again
3. Test again

### Problem: "User email not found in database"
**Solution:** User exists in auth but not in API database
```powershell
# Connect to PostgreSQL
psql -U postgres -d alignai_db

# Check users table
SELECT id, email, full_name FROM users;
```

### Problem: Ports already in use
**Solution:** Run the PowerShell script
```powershell
.\restart_servers.ps1
```

### Problem: "CORS error" in browser console
**Solution:** Make sure you're accessing via `http://localhost:8000`, NOT `file:///`

---

## 📊 Understanding the Fix

### What Changed?

1. **Shared Configuration**: Both servers now use the same `SECRET_KEY` from `shared_config.py`
2. **Better Cookie Handling**: CORS properly configured to allow cookies between ports
3. **Auth Verification**: API server now always verifies with Auth server
4. **Better Debugging**: Detailed logs show exactly what's happening

### How It Works Now:

```
User -> Login Page (localhost:8000)
         ↓
      Auth Server (localhost:5000)
         ↓ [Sets cookie: alignai_session]
      Dashboard (localhost:8000)
         ↓ [Sends cookie]
      API Server (localhost:5001)
         ↓ [Verifies cookie with Auth Server]
      Auth Server (localhost:5000)
         ↓ [Returns user info]
      API Server (localhost:5001)
         ↓ [Allows request]
      Success! ✅
```

---

## 🎯 Quick Test Commands

**Test if all servers are running:**
```powershell
# Should return "OK"
curl http://localhost:5000/api/health
curl http://localhost:5001/api/health
curl http://localhost:8000/
```

**Check what's using ports:**
```powershell
netstat -ano | findstr "5000 5001 8000"
```

**View auth server logs:**
Look at the PowerShell window running `auth.py`

**View API server logs:**
Look at the PowerShell window running `api.py`

---

## ✅ Success Checklist

- [ ] All 3 servers running (auth, api, frontend)
- [ ] PostgreSQL service started
- [ ] Browser cookies cleared
- [ ] Logged in successfully
- [ ] Test page shows all green ✅
- [ ] Resume upload works without 401 error

---

## 🆘 Still Not Working?

1. Take screenshots of:
   - All 3 PowerShell windows showing server logs
   - Browser console (F12 -> Console tab)
   - Test page results (`test-auth.html`)

2. Check the API server logs when you upload - it will tell you exactly what's wrong:
   - "No cookies received" = Browser not sending cookies
   - "Auth server returned 401" = Session expired
   - "Cannot connect to auth server" = Auth server not running
   - "User not found in database" = Database issue

3. Try the nuclear option:
```powershell
# Kill everything
taskkill /F /IM python.exe
taskkill /F /IM pythonw.exe

# Restart PostgreSQL
Restart-Service postgresql-x64-16

# Start fresh
.\restart_servers.ps1

# Clear browser completely
# Use the clear-session.html page

# Login again
```

---

## 📚 Related Files

- `shared_config.py` - Shared configuration for session keys
- `auth.py` - Authentication server (port 5000)
- `api.py` - API server with file upload (port 5001)
- `start_frontend.py` - Frontend server (port 8000)
- `restart_servers.ps1` - Automated restart script
- `test-auth.html` - Authentication testing tool
- `clear-session.html` - Cookie clearing tool

---

**Last Updated:** November 26, 2025

