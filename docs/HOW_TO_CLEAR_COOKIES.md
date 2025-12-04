# 🧹 How to Clear Cookies & Fix 401 Errors

You're getting: **401 UNAUTHORIZED** - This means authentication cookies aren't working.

---

## ⚡ **FASTEST METHOD: Use Clear Session Page**

1. Go to: **http://localhost:8000/clear-session.html**
2. Click **"🗑️ Clear All Data"**
3. Wait 2 seconds
4. You'll be redirected to login
5. **Login again**
6. **Try uploading** - Should work! ✅

---

## 🔴 **METHOD 2: Use the Clear Session Button**

1. Go to dashboard
2. Look at top right corner
3. Click the **red "Clear Session"** button
4. You'll be redirected to login
5. **Login again**
6. **Try uploading**

---

## 🌐 **METHOD 3: Clear Cookies Manually (Chrome/Edge)**

### Step-by-Step:

1. **Open Developer Tools**
   - Press `F12`
   - Or right-click → "Inspect"

2. **Go to Application Tab**
   - Click "Application" at the top
   - If you don't see it, click the `>>` arrows

3. **Clear Cookies**
   - On left side, expand "Cookies"
   - Click on "http://localhost:8000"
   - You'll see cookies listed on right
   - **Right-click** anywhere → **"Clear"**

4. **Clear Storage (Optional but recommended)**
   - On left side, click "Storage"
   - Click **"Clear site data"** button
   - Confirm

5. **Close Developer Tools**
   - Press `F12` again or click the X

6. **Refresh Page**
   - Press `F5` or `Ctrl+R`

7. **Login Again**

8. **Try Upload**

---

## 🦊 **METHOD 4: Clear Cookies (Firefox)**

1. Press `F12`
2. Click **"Storage"** tab
3. Expand **"Cookies"**
4. Click **"http://localhost:8000"**
5. Right-click → **"Delete All"**
6. Close Dev Tools
7. Refresh (`F5`)
8. Login again

---

## 🔒 **METHOD 5: Private/Incognito Mode**

Sometimes the easiest way:

1. **Open Private Window**
   - Chrome/Edge: `Ctrl+Shift+N`
   - Firefox: `Ctrl+Shift+P`

2. **Go to http://localhost:8000**

3. **Login**

4. **Try uploading**

5. If it works in private mode:
   - Close private window
   - Go back to normal browser
   - Clear cookies using Method 1, 2, or 3
   - Try again

---

## 💻 **METHOD 6: Using Browser Console**

1. Press `F12`
2. Go to **"Console"** tab
3. Copy and paste this code:
```javascript
// Clear all cookies
document.cookie.split(";").forEach(c => { 
    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
});

// Clear storage
localStorage.clear();
sessionStorage.clear();

// Reload
alert('Cookies cleared! Click OK to reload.');
location.reload();
```
4. Press `Enter`
5. Click OK on alert
6. Login again

---

## 🔄 **METHOD 7: Complete Browser Reset**

If nothing else works:

### Chrome/Edge:
1. Settings → Privacy and security
2. Click "Clear browsing data"
3. Select:
   - ✅ Cookies and other site data
   - ✅ Cached images and files
4. Time range: **Last hour**
5. Click "Clear data"
6. Close and reopen browser
7. Go to http://localhost:8000
8. Login

### Firefox:
1. Options → Privacy & Security
2. Cookies and Site Data → "Clear Data"
3. Select both options
4. Click "Clear"
5. Close and reopen browser
6. Go to http://localhost:8000
7. Login

---

## 🎯 **After Clearing Cookies:**

### Important Steps:

1. ✅ **Make sure all 3 servers are running:**
   ```powershell
   Get-NetTCPConnection -LocalPort 5000,5001,8000 -State Listen
   ```
   Should show all 3 ports listening

2. ✅ **Fresh login** - Don't use any saved passwords or autofill

3. ✅ **Check you're on http://localhost:8000** - Not file://

4. ✅ **Try uploading immediately** after login

---

## 🔍 **Verify Cookies Are Working:**

After logging in, check cookies exist:

1. Press `F12`
2. Go to "Application" tab
3. Expand "Cookies" → "http://localhost:8000"
4. **You should see:** `alignai_session` cookie
5. **Value should be:** A long encrypted string

**If you DON'T see this cookie:**
- The login didn't work properly
- Try clearing and logging in again

---

## ⚠️ **Common Issues:**

### Issue: "Can't find Application tab"
**Solution:** 
- Look for `>>` arrows at top of DevTools
- Click them to see more tabs
- Or try Ctrl+Shift+I instead of F12

### Issue: "Clear doesn't do anything"
**Solution:**
- Try Method 1 (clear-session.html page)
- Or use private/incognito mode

### Issue: "Cookies come back"
**Solution:**
- You're still logged in
- Click "Clear Session" button first
- THEN clear cookies

### Issue: "Still 401 after clearing"
**Solution:**
- Check both auth.py and api.py are running
- Restart BOTH servers:
  ```powershell
  Get-Process python | Stop-Process -Force
  python auth.py  # Terminal 1
  python api.py   # Terminal 2
  ```
- Clear cookies AGAIN
- Fresh login

---

## ✅ **Success Checklist:**

After clearing cookies and logging in:

- [ ] Can see dashboard
- [ ] See "Clear Session" button (red) at top right
- [ ] Can open Developer Tools (F12)
- [ ] Can see `alignai_session` cookie in Application tab
- [ ] Try uploading a file
- [ ] Should work! ✅

---

## 🆘 **Still Not Working?**

If you've tried everything and still get 401:

1. **Use Method 1** (clear-session.html) - This is the most reliable
2. **Restart ALL servers** (stop all Python processes, start fresh)
3. **Try private/incognito mode** to rule out browser issues
4. **Check server logs** when you try to upload - share the output

---

## 💡 **Pro Tip:**

**Bookmark this page:** http://localhost:8000/clear-session.html

Whenever you have authentication issues, just visit that page and click the button!

---

**After clearing cookies, upload should work!** 🎉✨

