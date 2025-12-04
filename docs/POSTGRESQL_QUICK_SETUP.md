# ⚡ PostgreSQL Quick Setup - 5 Minutes

## 🎯 **Goal: Get PostgreSQL Authentication Working**

---

## 📋 **Prerequisites**

✅ Windows 10/11  
✅ Python installed  
✅ Project files ready  

---

## 🚀 **Step-by-Step Setup**

### **Step 1: Install PostgreSQL (5 minutes)**

1. **Download PostgreSQL:**
   - Go to: https://www.postgresql.org/download/windows/
   - Download the latest version (16.x)
   - Run the installer

2. **During Installation:**
   - Click "Next" through most screens
   - **IMPORTANT:** Set password for `postgres` user
   - Write it down! (e.g., `postgres`)
   - Keep default port: `5432`
   - Install all components

3. **Verify Installation:**
   ```powershell
   psql --version
   ```
   Should show: `psql (PostgreSQL) 16.x`

---

### **Step 2: Create Database (1 minute)**

1. **Open Command Prompt or PowerShell**

2. **Connect to PostgreSQL:**
   ```powershell
   psql -U postgres
   ```
   Enter password when prompted

3. **Create Database:**
   ```sql
   CREATE DATABASE alignai_db;
   ```
   Should show: `CREATE DATABASE`

4. **Verify:**
   ```sql
   \l
   ```
   You should see `alignai_db` in the list

5. **Exit:**
   ```sql
   \q
   ```

---

### **Step 3: Update Password in Code (30 seconds)**

**If your PostgreSQL password is NOT "postgres":**

**Option A: Edit auth.py directly**

Find this line in `auth.py`:
```python
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
```

Change `'postgres'` to your actual password:
```python
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'your_actual_password')
```

**Option B: Create .env file (Better for security)**

Create file `.env` in project root:
```env
POSTGRES_PASSWORD=your_actual_password
```

---

### **Step 4: Install Python Dependencies (1 minute)**

```powershell
pip install flask flask-sqlalchemy flask-cors psycopg2-binary werkzeug python-dotenv
```

---

### **Step 5: Start Backend Server (30 seconds)**

```powershell
python auth.py
```

**Success looks like:**
```
✅ PostgreSQL connection successful!
✅ Database tables created successfully!
📊 Database: alignai_db
🔗 Host: localhost:5432
👤 User: postgres

🔐 AlignAI Authentication Server with PostgreSQL
📍 Server: http://localhost:5000
```

**If you see error:**
- Check PostgreSQL is running
- Check password is correct
- See troubleshooting below

---

### **Step 6: Test Signup (1 minute)**

1. **Open `login.html` in your browser**

2. **Click "Sign Up" tab**

3. **Fill in form:**
   - Full Name: Your Name
   - Email: your@email.com
   - Password: test123
   - Confirm: test123

4. **Click "Sign Up"**

5. **Should see:** "Account created successfully!"

---

### **Step 7: Verify in Database (30 seconds)**

```powershell
# Connect to database
psql -U postgres -d alignai_db

# View users
SELECT * FROM users;

# You should see your user!

# Exit
\q
```

---

## ✅ **Success Checklist**

- [ ] PostgreSQL installed
- [ ] `alignai_db` database created
- [ ] Password configured in `auth.py` or `.env`
- [ ] Python dependencies installed
- [ ] Backend server running (port 5000)
- [ ] Signup works on `login.html`
- [ ] User data visible in PostgreSQL

---

## 🐛 **Troubleshooting**

### **Problem: "password authentication failed"**

**Solution:**
```python
# In auth.py, update this line:
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'YOUR_ACTUAL_PASSWORD')
```

---

### **Problem: "database 'alignai_db' does not exist"**

**Solution:**
```powershell
psql -U postgres
CREATE DATABASE alignai_db;
\q
```

---

### **Problem: "could not connect to server"**

**Solution - Start PostgreSQL:**
```powershell
# Check if running
Get-Service -Name postgresql*

# Start if not running
net start postgresql-x64-16
```

---

### **Problem: "psql is not recognized"**

**Solution - Add to PATH:**

1. Find PostgreSQL bin folder (usually):
   ```
   C:\Program Files\PostgreSQL\16\bin
   ```

2. Add to System PATH:
   - Search Windows for "Environment Variables"
   - Edit "Path" variable
   - Add PostgreSQL bin folder
   - Restart terminal

---

### **Problem: "Signup not working - email already registered"**

**Solution - Delete test user:**
```powershell
psql -U postgres -d alignai_db

# Delete specific user
DELETE FROM users WHERE email = 'test@example.com';

# Or clear all users
TRUNCATE TABLE users RESTART IDENTITY;

\q
```

---

### **Problem: "No module named 'psycopg2'"**

**Solution:**
```powershell
pip install psycopg2-binary
```

---

### **Problem: "Port 5000 already in use"**

**Solution - Use different port:**

In `auth.py`, change last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

Then access at: http://localhost:5001

---

## 🔍 **Useful Commands**

### **PostgreSQL Commands:**

```powershell
# Connect to database
psql -U postgres -d alignai_db

# List databases
\l

# List tables
\dt

# View users
SELECT * FROM users;

# Count users
SELECT COUNT(*) FROM users;

# Delete all users
TRUNCATE TABLE users RESTART IDENTITY;

# Exit
\q
```

### **Backend Commands:**

```powershell
# Start server
python auth.py

# Check if running
curl http://localhost:5000/api/admin/stats

# Stop server
# Press Ctrl+C in terminal
```

---

## 📊 **What Was Created**

### **Database Structure:**

```
PostgreSQL Server (localhost:5432)
└── Database: alignai_db
    └── Table: users
        ├── id (Primary Key, auto-increment)
        ├── full_name (VARCHAR 100)
        ├── email (VARCHAR 120, UNIQUE)
        ├── password_hash (VARCHAR 255)
        ├── created_at (TIMESTAMP)
        ├── last_login (TIMESTAMP)
        └── is_active (BOOLEAN)
```

### **API Endpoints:**

| Method | URL | Purpose |
|--------|-----|---------|
| POST | `/api/auth/signup` | Create account |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/check-session` | Check if logged in |
| GET | `/api/auth/user` | Get user info |
| GET | `/api/admin/users` | List all users |
| GET | `/api/admin/stats` | Database stats |

---

## 🎯 **Next Steps**

1. ✅ PostgreSQL setup - Done!
2. ✅ Backend running - Done!
3. ✅ Signup working - Done!
4. 🔜 Create dashboard page
5. 🔜 Integrate resume alignment
6. 🔜 Add password reset
7. 🔜 Deploy to production

---

## 📚 **Full Documentation**

For detailed concepts and explanations, see:
**`Guides/POSTGRESQL_AUTHENTICATION_GUIDE.md`**

That guide explains:
- What is PostgreSQL?
- How does authentication work?
- What is ORM?
- Password hashing explained
- Database sessions
- ACID properties
- Security best practices
- Production deployment

---

## 🎉 **You're Done!**

Your authentication system is ready! 🚀

**Test it now:**
1. Open `login.html`
2. Create an account
3. Login
4. Check database: `psql -U postgres -d alignai_db`

**Questions?** See full guide: `Guides/POSTGRESQL_AUTHENTICATION_GUIDE.md`

