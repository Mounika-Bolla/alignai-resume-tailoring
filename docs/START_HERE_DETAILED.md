# 🚀 START HERE - Complete AlignAI Startup Guide

## ✅ **Follow These Steps EXACTLY - Don't Skip Any!**

---

## 📍 **STEP 1: Open Your Project Folder**

1. Press `Windows Key + E` (opens File Explorer)
2. Navigate to:
   ```
   C:\Users\monib\Desktop\resumetailoring
   ```
3. **You should see these files:**
   - auth.py
   - start_frontend.py
   - oauth_config.py
   - login.html
   - dashboard.html
   - index.html
   - START_SERVERS.bat

✅ **If you see these files, you're in the right place!**

---

## 📍 **STEP 2: Install Required Software (One-Time Setup)**

### **Check if Python is installed:**

1. Press `Windows Key`
2. Type: `cmd`
3. Press `Enter`
4. Type: `python --version`
5. Press `Enter`

**Expected Result:** `Python 3.11.x` or `Python 3.12.x`

❌ **If you see "python is not recognized":**
- Download Python from: https://www.python.org/downloads/
- During installation, CHECK THE BOX: "Add Python to PATH"
- After installation, restart computer

---

### **Install Required Libraries:**

In the Command Prompt window, type this **EXACTLY**:

```cmd
pip install flask flask-sqlalchemy flask-cors psycopg2-binary werkzeug requests python-dotenv
```

Press `Enter` and **wait** until it finishes (may take 1-2 minutes).

✅ **You should see:** "Successfully installed..." messages

---

## 📍 **STEP 3: Start PostgreSQL Database**

### **Check if PostgreSQL is running:**

In Command Prompt, type:
```cmd
"C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" status
```

**Expected Result:** `server is running (PID: xxxxx)`

❌ **If you see "no server running":**

**Start PostgreSQL:**
```cmd
"C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" start
```

**Wait for:** `server started`

✅ **PostgreSQL is now running!**

---

## 📍 **STEP 4: Start Backend Server (Terminal 1)**

### **Open PowerShell Window 1:**

1. Press `Windows Key`
2. Type: `powershell`
3. Press `Enter`

### **Navigate to project folder:**

Type this **EXACTLY** (copy and paste):
```powershell
cd C:\Users\monib\Desktop\resumetailoring
```

Press `Enter`

### **Start Backend Server:**

Type:
```powershell
python auth.py
```

Press `Enter`

### **✅ SUCCESS looks like this:**

You should see:
```
✅ PostgreSQL connection successful!
✅ Database tables created successfully!
📊 Database: alignai_db
🔗 Host: localhost:5432
👤 User: postgres

🔐 AlignAI Authentication Server with PostgreSQL
====================================================================
📍 Server: http://localhost:5000
💾 Database: PostgreSQL (alignai_db)
```

### **❌ If you see ERRORS instead:**

**ERROR: "No module named 'requests'"**
```powershell
pip install requests
```
Then run `python auth.py` again.

**ERROR: "No module named 'oauth_config'"**
```powershell
dir oauth_config.py
```
If file doesn't exist, tell me and I'll recreate it.

**ERROR: "database connection failed"**
- Go back to STEP 3 and start PostgreSQL
- Then run `python auth.py` again

**ERROR: "Port 5000 already in use"**
```powershell
Get-NetTCPConnection -LocalPort 5000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```
Then run `python auth.py` again.

### **⚠️ IMPORTANT:**
**DO NOT CLOSE THIS WINDOW!** 

Minimize it if you want, but keep it running.

---

## 📍 **STEP 5: Start Frontend Server (Terminal 2)**

### **Open PowerShell Window 2 (NEW WINDOW):**

1. Press `Windows Key` again
2. Type: `powershell`
3. Press `Enter`

**You should now have TWO PowerShell windows open!**

### **Navigate to project folder:**

In the **NEW** window, type:
```powershell
cd C:\Users\monib\Desktop\resumetailoring
```

Press `Enter`

### **Start Frontend Server:**

Type:
```powershell
python start_frontend.py
```

Press `Enter`

### **✅ SUCCESS looks like this:**

You should see:
```
============================================================
🌐 AlignAI Frontend Server
============================================================

📍 Server running at: http://localhost:8000

🔗 Open in browser:
   Homepage:  http://localhost:8000/index.html
   Login:     http://localhost:8000/login.html
   Dashboard: http://localhost:8000/dashboard.html

💡 Make sure backend is running on port 5000
   (python auth.py)

============================================================

Press Ctrl+C to stop the server
```

### **❌ If you see ERRORS instead:**

**ERROR: "Port 8000 already in use"**

Edit `start_frontend.py`:
- Change line that says `PORT = 8000`
- Change it to `PORT = 8080`
- Save file
- Run `python start_frontend.py` again
- Then use `http://localhost:8080/` instead of 8000

### **⚠️ IMPORTANT:**
**DO NOT CLOSE THIS WINDOW EITHER!**

Now you have TWO windows running:
- Window 1: Backend (port 5000)
- Window 2: Frontend (port 8000)

**Both must stay open!**

---

## 📍 **STEP 6: Open Your Browser**

1. Open Google Chrome, Microsoft Edge, or Firefox

2. In the address bar, type **EXACTLY**:
   ```
   http://localhost:8000/index.html
   ```

3. Press `Enter`

### **✅ SUCCESS looks like:**

You should see your AlignAI homepage with:
- Logo at the top
- "Resume Aligner" heading
- Beautiful beige design
- "Start Aligning Now" button
- Animated background

### **❌ If you see ERROR instead:**

**"This site can't be reached" or "ERR_CONNECTION_REFUSED"**

Reasons:
1. Frontend server not running
   - Go back to STEP 5
   - Check if you see the frontend server output
   
2. Wrong URL
   - Make sure it's EXACTLY: `http://localhost:8000/index.html`
   - Don't use `file://` 
   - Don't open the HTML file directly

3. Port 8000 was changed
   - If you used port 8080, use: `http://localhost:8080/index.html`

---

## 📍 **STEP 7: Test Login**

1. On the homepage, click **"Start Aligning Now"** button

2. You should be redirected to: `http://localhost:8000/login.html`

3. Try signing up:
   - Full Name: Your name
   - Email: your@email.com
   - Password: test123
   - Confirm Password: test123
   - Click "Sign Up"

4. You should be redirected to: `http://localhost:8000/dashboard.html`

5. You should see your dashboard with your name in the navbar!

### **✅ SUCCESS!** Your app is fully working!

### **❌ If redirected back to login:**

- Check that both servers are still running
- Check the PowerShell windows - look for error messages
- Tell me what errors you see

---

## 📍 **STEP 8: Stop the Servers (When Done)**

### **To stop servers:**

1. Go to PowerShell Window 1 (Backend)
2. Press `Ctrl + C`
3. Go to PowerShell Window 2 (Frontend)
4. Press `Ctrl + C`

**OR**

Just close both PowerShell windows.

---

## 🔄 **QUICK RESTART (Next Time You Use the App)**

**Every time you want to use AlignAI:**

### **Method 1: Use Batch File (Easiest)**

1. Go to: `C:\Users\monib\Desktop\resumetailoring`
2. Double-click: `START_SERVERS.bat`
3. Wait for windows to open
4. Open browser: `http://localhost:8000/index.html`

### **Method 2: Manual Start**

1. Open PowerShell Window 1:
   ```powershell
   cd C:\Users\monib\Desktop\resumetailoring
   python auth.py
   ```

2. Open PowerShell Window 2:
   ```powershell
   cd C:\Users\monib\Desktop\resumetailoring
   python start_frontend.py
   ```

3. Open browser: `http://localhost:8000/index.html`

---

## ✅ **CHECKLIST - Everything Should Be:**

- [ ] PostgreSQL running
- [ ] Backend server running (Window 1 - port 5000)
- [ ] Frontend server running (Window 2 - port 8000)
- [ ] Both windows still open (not closed)
- [ ] Browser at `http://localhost:8000/index.html`
- [ ] Homepage loads correctly
- [ ] Can login/signup
- [ ] Dashboard shows after login

---

## 🆘 **STILL HAVING PROBLEMS?**

### **Option 1: Full Reset**

```powershell
# Stop everything
taskkill /F /IM python.exe

# Start PostgreSQL
"C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" start

# Wait 5 seconds, then start servers again from STEP 4
```

### **Option 2: Check What's Running**

```powershell
# Check if servers are running
netstat -ano | findstr "5000 8000"
```

**Should show:**
```
TCP    0.0.0.0:5000    ...    LISTENING
TCP    0.0.0.0:8000    ...    LISTENING
```

### **Option 3: Tell Me:**

If nothing works, tell me:

1. **What step are you stuck on?** (Which step number?)

2. **What do you see?** Copy and paste the exact text/error

3. **Which window has the error?** (PowerShell 1 or 2?)

---

## 📱 **CONTACT FOR HELP**

If you're still stuck, tell me:
- "I'm stuck at STEP X"
- Copy the error message
- Tell me what you tried

I'll help you fix it immediately!

---

## 🎯 **SUMMARY - What Each Part Does:**

| Component | Port | What it Does |
|-----------|------|--------------|
| **PostgreSQL** | 5432 | Stores user accounts |
| **Backend (auth.py)** | 5000 | Handles login, signup, database |
| **Frontend (start_frontend.py)** | 8000 | Serves website files |
| **Browser** | - | Shows the website |

**All 4 must be running for the app to work!**

---

## ✨ **YOU'RE DONE!**

Follow these steps **in order**, and everything will work!

**Most common mistake:** Closing one of the PowerShell windows - keep both open!

**Remember:** Use `http://localhost:8000/` NOT `file://`

**Good luck!** 🚀

