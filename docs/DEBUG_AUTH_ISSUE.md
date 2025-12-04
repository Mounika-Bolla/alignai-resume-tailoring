# 🔍 DEBUG AUTHENTICATION ISSUE - Step by Step

## Current Situation
You're getting: **"❌ Error parsing resume: Not authenticated"**

I've added extensive debugging to find the exact problem. Follow these steps:

---

## 🚀 STEP 1: Restart Everything

### A. Stop All Servers
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### B. Start Auth Server First
```powershell
python auth.py
```

**Wait** until you see:
```
✅ Database connection successful!
* Running on http://0.0.0.0:5000
```

### C. Start API Server Second  
```powershell
python api.py
```

**Wait** until you see:
```
🚀 AlignAI API Server Starting...
✅ Database tables created successfully!
Server running on http://localhost:5001
```

### D. Start Frontend Third
```powershell
python start_frontend.py
```

---

## 🧪 STEP 2: Test Authentication

### A. Clear Everything in Browser
1. Press `F12` (Developer Tools)
2. Go to **"Application"** tab
3. Click **"Storage"** → **"Clear site data"**
4. Click **"Clear site data"** button
5. Close Developer Tools

### B. Fresh Login
1. Go to: http://localhost:8000
2. Click **"Start Aligning Now"**
3. **Login** with your credentials
4. You should land on dashboard

### C. Test Session (Before Upload)
In browser console (F12 → Console), run:
```javascript
fetch('http://localhost:5001/api/debug/session', {
  credentials: 'include'
}).then(r => r.json()).then(d => console.log(d))
```

**Look at the output:**

**GOOD (Working):**
```json
{
  "authenticated": true,
  "user": {"id": 1, "email": "your@email.com"},
  "session_data": {"user_id": 1},
  "cookies_received": ["alignai_session"]
}
```

**BAD (Not Working):**
```json
{
  "authenticated": false,
  "user": null,
  "session_data": {},
  "cookies_received": []
}
```

---

## 🔍 STEP 3: Look at Server Logs

### When You Upload a File:

**Check the API Server Terminal (port 5001)**

You should see output like this:

```
==================================================
📤 UPLOAD REQUEST RECEIVED
==================================================
Request Cookies: {'alignai_session': 'long-encrypted-string'}
Session Data: {'user_id': 1}
User ID in session: 1
==================================================

✅ AUTHENTICATED - User: your@email.com (ID: 1)
```

**If you see this instead:**
```
==================================================
📤 UPLOAD REQUEST RECEIVED
==================================================
Request Cookies: {}
Session Data: {}
User ID in session: Not found
==================================================

📡 Checking authentication with auth server...
Auth server response status: 200
✅ User authenticated via auth server: your@email.com
```

This means the cookie isn't being sent, but auth server verification works.

**If you see this:**
```
❌ AUTHENTICATION FAILED - No user found in session
Available cookies: []
Session contents: {}
```

This means NO cookies are being sent at all.

---

## 🛠️ STEP 4: Fixes Based on Output

### If NO COOKIES are being sent:

**Problem:** Browser is blocking cookies

**Solution:**
1. Check browser is accessing via **http://localhost:8000** (not file://)
2. Try incognito/private mode
3. Check browser cookie settings aren't blocking localhost
4. Try different browser (Chrome/Edge/Firefox)

### If cookies are sent but session is empty:

**Problem:** SECRET_KEY mismatch

**Solution:**
1. Check both servers started successfully
2. Verify `shared_config.py` exists
3. Restart auth.py FIRST, then api.py
4. Clear cookies and re-login

### If "Auth server verification works":

**Problem:** Cookies work, but api.py can't read them directly

**This should actually WORK** - The code now falls back to auth server verification.

Try uploading again - it should work even with this message.

---

## 📊 STEP 5: Manual Verification

### Check if both servers share the same database:

**In pgAdmin:**
1. Connect to PostgreSQL 16
2. Open `alignai_db` database
3. Browse `users` table
4. You should see your user account

### Check if SECRET_KEY is consistent:

**Run this in both server terminals:**

**In auth.py terminal:**
```python
python -c "from shared_config import SECRET_KEY; print(SECRET_KEY[:20])"
```

**In api.py terminal:**
```python
python -c "from shared_config import SECRET_KEY; print(SECRET_KEY[:20])"
```

**Both should print the SAME value!**

---

## 🎯 STEP 6: Try Upload with Debugging

1. Make sure all 3 servers are running
2. Make sure you're logged in
3. Open Browser Console (F12 → Console)
4. Try uploading a resume
5. **Watch the API server terminal** for debug output
6. **Copy all the output** from the API terminal and share it

---

## 💡 Common Issues & Solutions

### Issue 1: "Connection refused" on localhost:5001
**Solution:** API server not running - start it with `python api.py`

### Issue 2: Cookies not being sent
**Solution:** 
- Must access via http://localhost:8000 (not file://)
- Frontend server must be running

### Issue 3: "Auth server timeout"
**Solution:**
- Auth server (port 5000) must be running
- Check with: `Get-NetTCPConnection -LocalPort 5000`

### Issue 4: Session works for a moment then stops
**Solution:**
- Don't restart servers without clearing cookies
- Always clear cookies after restarting

---

## 🆘 If Still Not Working

Please share:
1. ✅ Output from browser console when testing `/api/debug/session`
2. ✅ Output from API server terminal when you try to upload
3. ✅ Screenshot of cookies in browser (F12 → Application → Cookies)
4. ✅ Confirmation that all 3 servers are running

---

## 🎯 Expected Flow (When Working)

```
1. Login at localhost:8000
   ↓
2. Auth server (5000) creates session
   ↓
3. Browser stores cookie: "alignai_session"
   ↓
4. Upload file to API server (5001)
   ↓
5. API server receives cookie
   ↓
6. API server verifies with auth server
   ↓
7. Upload succeeds ✅
```

---

Let me know what you see in the logs! 🔍

