# 🏗️ AlignAI - Clean Architecture Overview

**Last Updated:** November 26, 2025

---

## 🎯 What Changed?

### **Before (Messy):**
```
❌ TWO separate backend servers
- auth.py (port 5000) - Authentication
- api.py (port 5001) - Resume & Chat
- Shared config files
- Session synchronization issues
- Complex to manage
```

### **After (Clean):**
```
✅ ONE unified backend server
- backend/server.py (port 5000) - Everything
- No session sync issues
- Easy to start and manage
- Professional folder structure
```

---

## 📁 New Project Structure

```
resumetailoring/
│
├── 🌐 frontend/           All HTML, CSS, JavaScript
│   ├── index.html        Landing page with animations
│   ├── login.html        Authentication
│   ├── dashboard.html    Main AI playground
│   ├── test-auth.html    Debug tool
│   ├── clear-session.html Cookie clearing tool
│   └── assets/           Images (logo, before, after)
│
├── 🔧 backend/            Single unified server
│   └── server.py         Complete backend (auth + resume + chat)
│
├── 🤖 agents/             AI agents and tools
│   └── resume_generator.py  Main AI agent
│
├── 🧪 tests/              Testing files
│   ├── main.py           Agent testing
│   └── sample_data.py    Sample resumes and JDs
│
├── 📚 docs/               All documentation
│   └── *.md              Guides and references
│
├── 🚀 start.py            ONE command to start everything
├── 📦 requirements.txt   Python dependencies
├── 📖 README.md          Main project documentation
└── 🔐 .env               Environment variables (optional)
```

---

## 🗄️ Database Structure

**One PostgreSQL Database: `alignai_db`**

### Tables:

1. **users** - User accounts and authentication
   - id, full_name, email, password_hash
   - created_at, last_login, is_active

2. **saved_resumes** - User's resume library
   - id, user_id, name, content, file_type
   - created_at, updated_at

3. **chat_sessions** - AI chat sessions
   - id, user_id, created_at

4. **chat_messages** - Individual chat messages
   - id, session_id, role, content, created_at

---

## 🚀 How to Start the Application

### **Method 1: One Command (Recommended)**

```bash
python start.py
```

This starts:
- Backend server on port 5000
- Frontend server on port 8000

### **Method 2: Manual (Two Terminals)**

**Terminal 1 - Backend:**
```bash
python backend/server.py
```

**Terminal 2 - Frontend:**
```bash
python -m http.server 8000 --directory frontend
```

---

## 🌐 URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Homepage** | http://localhost:8000/index.html | Landing page |
| **Login** | http://localhost:8000/login.html | Authentication |
| **Dashboard** | http://localhost:8000/dashboard.html | AI playground |
| **Test Tool** | http://localhost:8000/test-auth.html | Debug authentication |
| **Clear Cookies** | http://localhost:8000/clear-session.html | Clear session |
| **Backend API** | http://localhost:5000/api | Backend server |
| **Health Check** | http://localhost:5000/api/health | Server status |

---

## 🔌 API Endpoints

### **Authentication** (`/api/auth/*`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| GET | `/api/auth/check-session` | Check if authenticated |

### **Resume Management** (`/api/resume/*`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/resume/upload` | Upload & parse resume file |
| POST | `/api/resume/save` | Save to library |
| GET | `/api/resume/list` | Get all user's resumes |
| GET | `/api/resume/<id>` | Get specific resume |
| PUT | `/api/resume/<id>/rename` | Rename resume |
| DELETE | `/api/resume/<id>` | Delete resume |

### **AI Chat** (`/api/chat/*`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/chat/message` | Send message to AI |

---

## 🛠️ Backend Technology Stack

- **Framework:** Flask 3.0
- **Database:** PostgreSQL + SQLAlchemy ORM
- **Security:** Werkzeug password hashing
- **File Parsing:** pypdf, python-docx
- **CORS:** flask-cors for cross-origin requests
- **Sessions:** Flask sessions with secure cookies

---

## 🎨 Frontend Technology Stack

- **HTML5** - Semantic structure
- **CSS3** - Modern animations, gradients, glassmorphism
- **JavaScript (ES6+)** - Async/await, Fetch API
- **No frameworks** - Pure vanilla JS for performance

### Key Features:
- ✅ Drag & drop file upload
- ✅ Real-time chat interface
- ✅ Animated backgrounds
- ✅ Responsive design
- ✅ Custom scrollbars
- ✅ Loading animations

---

## 🔐 Security Features

### Current (Development):
- ✅ Password hashing (Werkzeug)
- ✅ Secure session cookies
- ✅ CSRF protection (SameSite cookies)
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ File type validation
- ✅ File size limits (10MB)

### For Production:
- ⚠️ Change SECRET_KEY to strong random value
- ⚠️ Enable HTTPS
- ⚠️ Set SESSION_COOKIE_SECURE=True
- ⚠️ Implement rate limiting
- ⚠️ Add input sanitization
- ⚠️ Use environment variables for all secrets
- ⚠️ Deploy with Gunicorn/uWSGI

---

## 📊 Data Flow

### **Login Flow:**
```
User → login.html → POST /api/auth/login
                  ↓
                Backend validates
                  ↓
                Set session cookie
                  ↓
                Redirect to dashboard
```

### **Resume Upload Flow:**
```
User → dashboard.html → Upload file
                      ↓
                    POST /api/resume/upload (with cookie)
                      ↓
                    Backend checks session
                      ↓
                    Parse PDF/DOCX
                      ↓
                    Return text content
```

### **Resume Save Flow:**
```
User → Click "Save to Library"
     ↓
   POST /api/resume/save (with content)
     ↓
   Backend saves to database (saved_resumes table)
     ↓
   Return success + resume ID
```

---

## 🧪 Testing

### **1. Test Authentication**
```
http://localhost:8000/test-auth.html
```
- Check if servers are online
- Verify cookies are set
- Test authentication

### **2. Test Resume Upload**
1. Login
2. Go to dashboard
3. Upload a PDF or DOCX file
4. Check console for logs

### **3. Test AI Agents**
```bash
cd tests
python main.py
```

---

## 🐛 Common Issues & Solutions

### **Port Already in Use**
```bash
# Kill process on port
netstat -ano | findstr "5000"
taskkill /PID [PID] /F
```

### **PostgreSQL Not Running**
```bash
# Start PostgreSQL
Start-Service postgresql-x64-16
```

### **401 Unauthorized Error**
1. Clear cookies: `http://localhost:8000/clear-session.html`
2. Logout and login again
3. Check both servers are running

### **Module Not Found**
```bash
pip install -r requirements.txt
```

---

## 📈 Future Enhancements

### **Planned Features:**
- [ ] Full AI integration with ResumeGeneratorAgent
- [ ] Real-time job matching
- [ ] Resume templates
- [ ] Export to multiple formats
- [ ] ATS score calculator
- [ ] Cover letter generation
- [ ] Interview preparation
- [ ] OAuth social login (Google, LinkedIn, GitHub)

### **Technical Improvements:**
- [ ] WebSocket for real-time chat
- [ ] Redis for caching
- [ ] Celery for background jobs
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Unit & integration tests
- [ ] API documentation (Swagger)

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `NEW_ARCHITECTURE.md` | This file - architecture overview |
| `POSTGRESQL_QUICK_SETUP.md` | Database setup guide |
| `FIX_401_ERROR.md` | Troubleshooting authentication |
| `SESSION_COOKIE_FIX.md` | Cookie/session issues |
| `HOW_TO_CLEAR_COOKIES.md` | Clear browser cookies |

---

## ✅ Benefits of New Architecture

### **Developer Benefits:**
- ✅ Easier to understand
- ✅ Faster to develop features
- ✅ Simpler debugging
- ✅ Better code organization
- ✅ Easier to deploy

### **User Benefits:**
- ✅ Faster page loads
- ✅ No session issues
- ✅ More reliable
- ✅ Better performance

### **Maintenance Benefits:**
- ✅ Single server to monitor
- ✅ One codebase for backend
- ✅ Fewer moving parts
- ✅ Easier updates

---

## 🎓 Learning Resources

### **Flask:**
- Official Docs: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/

### **PostgreSQL:**
- Official Docs: https://www.postgresql.org/docs/
- Tutorial: https://www.postgresqltutorial.com/

### **Frontend:**
- MDN Web Docs: https://developer.mozilla.org/
- JavaScript.info: https://javascript.info/

---

## 🤝 Contributing

1. Keep code clean and documented
2. Test thoroughly before committing
3. Update documentation when adding features
4. Follow Python PEP 8 style guide
5. Use meaningful commit messages

---

**Questions? Check the docs folder or the test tools!**

**Built with ❤️ for better resumes**



