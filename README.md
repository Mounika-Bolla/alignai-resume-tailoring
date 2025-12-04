# 🎯 AlignAI - AI-Powered Resume Alignment System

**Align your resume with job descriptions using AI**

---

## 📁 Project Structure

```
resumetailoring/
├── frontend/              # Web interface (HTML/CSS/JS)
│   ├── index.html        # Landing page
│   ├── login.html        # Authentication page
│   ├── dashboard.html    # Main application
│   ├── test-auth.html    # Debug tool
│   └── assets/           # Images and static files
├── backend/               # Flask API server
│   └── server.py         # Main backend (auth + resume + AI)
├── agents/                # AI agents and tools
│   └── resume_generator.py
├── tests/                 # Test files
│   ├── main.py           # Agent testing
│   └── sample_data.py    # Sample data
├── docs/                  # Documentation
├── start.py              # Single command to start everything
└── requirements.txt      # Python dependencies
```

---

## 🚀 Quick Start

### **1. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **2. Setup PostgreSQL**

Make sure PostgreSQL is installed and running:

```powershell
# Check status
Get-Service postgresql*

# Start if stopped
Start-Service postgresql-x64-16
```

Create database:

```sql
psql -U postgres
CREATE DATABASE alignai_db;
\q
```

### **3. Configure Environment**

Create a `.env` file (optional):

```env
SECRET_KEY=your-secret-key-here
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=alignai_db
```

### **4. Run the Application**

**Option A: One Command (Recommended)**

```bash
python start.py
```

**Option B: Manual (Two Terminals)**

Terminal 1 - Backend:
```bash
python backend/server.py
```

Terminal 2 - Frontend:
```bash
python -m http.server 8000 --directory frontend
```

### **5. Access the Application**

Open your browser:
- 🏠 Homepage: `http://localhost:8000/index.html`
- 🔐 Login: `http://localhost:8000/login.html`
- 📊 Dashboard: `http://localhost:8000/dashboard.html`

---

## 🎯 Features

### ✅ **User Authentication**
- Email/password registration and login
- Secure session management
- Password hashing with Werkzeug

### ✅ **Resume Upload & Parsing**
- Support for PDF and DOCX files
- Automatic text extraction
- File validation and security

### ✅ **Resume Library**
- Save multiple resumes
- Rename, delete, and manage resumes
- Quick access to saved resumes

### ✅ **AI Chat Interface** (Coming Soon)
- Interactive AI assistant
- Resume analysis and suggestions
- Job description matching

### ✅ **Modern UI**
- Responsive design
- Smooth animations
- Professional beige/brown theme
- Drag-and-drop file upload

---

## 🗄️ Database Schema

### **users** Table
- `id` - Primary key
- `full_name` - User's full name
- `email` - Unique email (login)
- `password_hash` - Hashed password
- `created_at` - Registration date
- `last_login` - Last login timestamp

### **saved_resumes** Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `name` - Resume name
- `content` - Extracted text
- `file_type` - pdf/docx
- `created_at`, `updated_at` - Timestamps

### **chat_sessions** Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `created_at` - Session start time

### **chat_messages** Table
- `id` - Primary key
- `session_id` - Foreign key to chat_sessions
- `role` - 'user' or 'assistant'
- `content` - Message text
- `created_at` - Message timestamp

---

## 🔧 API Endpoints

### **Authentication**
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/check-session` - Check if authenticated

### **Resume Management**
- `POST /api/resume/upload` - Upload and parse resume file
- `POST /api/resume/save` - Save resume to library
- `GET /api/resume/list` - Get all user's resumes
- `GET /api/resume/<id>` - Get specific resume
- `PUT /api/resume/<id>/rename` - Rename resume
- `DELETE /api/resume/<id>` - Delete resume

### **AI Chat**
- `POST /api/chat/message` - Send message to AI

### **Utility**
- `GET /api/health` - Health check

---

## 🧪 Testing

### **Test Authentication**
1. Go to `http://localhost:8000/test-auth.html`
2. Click buttons to test each component:
   - Server status
   - Cookie verification
   - Authentication check

### **Test AI Agents**
```bash
cd tests
python main.py
```

---

## 🛠️ Troubleshooting

### **Port Already in Use**

```powershell
# Find process using port
netstat -ano | findstr "5000"

# Kill process (replace PID)
taskkill /PID [PID] /F
```

### **PostgreSQL Connection Error**

```powershell
# Check if running
Get-Service postgresql*

# Start service
Start-Service postgresql-x64-16

# Verify connection
psql -U postgres -d alignai_db
```

### **Cannot Upload Files (401 Error)**

1. Clear browser cookies: `http://localhost:8000/clear-session.html`
2. Logout and login again
3. Check both servers are running
4. Use test page to diagnose: `http://localhost:8000/test-auth.html`

### **Module Not Found Errors**

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific package
pip install pypdf python-docx
```

---

## 📚 Documentation

See the `docs/` folder for detailed guides:
- Database setup
- Authentication flow
- Troubleshooting guides
- API documentation

---

## 🔐 Security Notes

⚠️ **Development Setup** - Not production-ready!

For production deployment:
1. Change `SECRET_KEY` to a strong random value
2. Use environment variables for all secrets
3. Enable HTTPS and set `SESSION_COOKIE_SECURE=True`
4. Use a proper WSGI server (Gunicorn, uWSGI)
5. Set up proper database backups
6. Implement rate limiting
7. Add input validation and sanitization

---

## 🤝 Contributing

1. Test your changes thoroughly
2. Update documentation
3. Follow Python PEP 8 style guide
4. Keep commits atomic and well-described

---

## 📝 License

MIT License - Feel free to use and modify

---

## 🆘 Need Help?

1. Check `docs/` folder for guides
2. Use test tools: `test-auth.html`, `clear-session.html`
3. Check server logs in terminal windows
4. Review this README

---

**Built with ❤️ for better resumes and better jobs**

