# 🔐 Reset PostgreSQL Password - Step by Step

## 🎯 **Your Situation:**
- ❌ PostgreSQL is running
- ❌ Can't remember the password for `postgres` user
- ✅ We can fix this!

---

## ✅ **Solution: Reset Password (5 minutes)**

### **Step 1: Stop PostgreSQL**

Open **PowerShell as Administrator** and run:

```powershell
& "C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" stop
```

Wait for it to say: `server stopped`

---

### **Step 2: Edit Authentication Config**

**Option A: Using Notepad (Easiest)**

1. Open File Explorer
2. Navigate to: `C:\Program Files\PostgreSQL\16\data`
3. Find file: `pg_hba.conf`
4. Right-click → Open with → Notepad (as Administrator)

**Option B: Using PowerShell**

```powershell
notepad "C:\Program Files\PostgreSQL\16\data\pg_hba.conf"
```

---

### **Step 3: Change Authentication Method**

In the `pg_hba.conf` file:

**Find these lines near the bottom:**
```
# IPv4 local connections:
host    all             all             127.0.0.1/32            scram-sha-256
# IPv6 local connections:
host    all             all             ::1/128                 scram-sha-256
```

**Change them to:**
```
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
```

**Change `scram-sha-256` to `trust`**

**Save the file:** Ctrl+S

---

### **Step 4: Start PostgreSQL**

```powershell
& "C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" start
```

Wait for: `server started`

---

### **Step 5: Connect Without Password**

```powershell
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres
```

**You should connect directly (no password needed)!**

---

### **Step 6: Set New Password**

In the `psql` prompt, run:

```sql
ALTER USER postgres PASSWORD 'postgres';
```

**Or choose your own password:**
```sql
ALTER USER postgres PASSWORD 'your_new_password';
```

**You should see:** `ALTER ROLE`

**Exit psql:**
```sql
\q
```

---

### **Step 7: Restore Security Settings**

**Open `pg_hba.conf` again:**
```powershell
notepad "C:\Program Files\PostgreSQL\16\data\pg_hba.conf"
```

**Change back from `trust` to `scram-sha-256`:**
```
# IPv4 local connections:
host    all             all             127.0.0.1/32            scram-sha-256
# IPv6 local connections:
host    all             all             ::1/128                 scram-sha-256
```

**Save the file**

---

### **Step 8: Restart PostgreSQL**

```powershell
# Stop
& "C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" stop

# Start
& "C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" start
```

---

### **Step 9: Test New Password**

```powershell
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres
```

**Enter your new password:** `postgres` (or whatever you set)

**Success!** ✅

---

## 🚀 **After Password Reset**

### **Update Your auth.py**

If you set password to something other than `postgres`:

**Option A: Edit auth.py directly**

Find this line:
```python
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
```

Change to:
```python
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'your_new_password')
```

**Option B: Use .env file (Better)**

Create `.env` file in project root:
```env
POSTGRES_PASSWORD=your_new_password
```

---

## 📝 **Quick Command Summary**

```powershell
# 1. Stop PostgreSQL
& "C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" stop

# 2. Edit config (change scram-sha-256 to trust)
notepad "C:\Program Files\PostgreSQL\16\data\pg_hba.conf"

# 3. Start PostgreSQL
& "C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" start

# 4. Connect without password
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres

# 5. In psql, set new password
ALTER USER postgres PASSWORD 'postgres';
\q

# 6. Edit config back (change trust to scram-sha-256)
notepad "C:\Program Files\PostgreSQL\16\data\pg_hba.conf"

# 7. Restart
& "C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" restart
```

---

## ⚠️ **Important Notes**

1. **Security:** The `trust` method allows connection without password - only use temporarily!
2. **Always change back to `scram-sha-256`** after resetting password
3. **Remember your new password** this time! 😊
4. **Recommended password:** `postgres` (simple for development)

---

## 🐛 **Troubleshooting**

### **"Cannot open file" when editing pg_hba.conf**

**Solution:** Run Notepad as Administrator:
1. Press Windows Key
2. Type "Notepad"
3. Right-click → Run as administrator
4. File → Open → Navigate to `pg_hba.conf`

### **"Permission denied" when saving**

**Solution:** You need admin rights. Close Notepad and open as Administrator.

### **Server won't start after editing**

**Solution:** Check for typos in `pg_hba.conf`. Must be exactly:
- `trust` (not `Trust` or `TRUST`)
- Spaces, not tabs
- No extra characters

---

## ✅ **Recommended: Set Simple Password**

For development, use simple password:

```sql
ALTER USER postgres PASSWORD 'postgres';
```

**Why?**
- Easy to remember
- Matches the default in `auth.py`
- Fine for local development
- Can always change later

---

## 🎯 **After You Reset**

1. ✅ Password reset to `postgres`
2. ✅ Create database:
   ```sql
   CREATE DATABASE alignai_db;
   ```
3. ✅ Test connection:
   ```bash
   psql -U postgres -d alignai_db
   ```
4. ✅ Start backend:
   ```bash
   python auth.py
   ```

---

**Follow these steps and you'll be back up and running!** 🚀

**Pro tip:** Write down your password this time! 📝

