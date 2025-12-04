# 🚀 AlignAI Dashboard - Quick Start Guide

## ✅ What We Just Built

Your AlignAI dashboard now has **FULL backend integration**!

### **Features Now Working:**
- ✅ File Upload & Parsing (PDF/DOCX)
- ✅ Resume Text Extraction
- ✅ Resume Library (Save/Load/Delete/Rename)
- ✅ AI Chat Integration
- ✅ Real-time AI Responses
- ✅ Database Storage (PostgreSQL)

---

## 🎯 How to Start Everything

You need **3 servers** running:

### **Terminal 1: Auth Server (Port 5000)**
```bash
python auth.py
```
- Handles login/signup/sessions
- **Must keep running!**

### **Terminal 2: Resume API Server (Port 5001)**
```bash
python api.py
```
- Handles file uploads, resume storage, AI chat
- **Must keep running!**

### **Terminal 3: Frontend Server (Port 8000)**
```bash
python start_frontend.py
```
- Serves the HTML/CSS/JS files
- **Must keep running!**

---

## 🌐 Access Your Dashboard

Once all 3 servers are running:

1. **Open browser:** http://localhost:8000
2. **Click "Start Aligning Now"**
3. **Login** (or create account)
4. **You're in the dashboard!** 🎉

---

## 🧪 Test the Features

### **1. Upload Resume**
- Drag & drop a PDF or DOCX file
- OR click the upload area to browse
- Wait for parsing to complete
- You'll see: "✅ Resume parsed successfully!"

### **2. Paste Job Description**
- Click in the "Job Description" text area
- Paste a job posting
- Character count updates automatically

### **3. Chat with AI**
Try these commands:
- "Analyze the skills in this job description"
- "Create a tailoring strategy"
- "Generate a tailored resume"
- "What skills am I missing?"

### **4. Save Resume to Library**
- After uploading, click "Save to Library"
- Give it a name (e.g., "Tech Resume 2024")
- It appears in the left sidebar!

### **5. Load Saved Resume**
- Click any resume in the sidebar
- It loads instantly!
- No need to re-upload

### **6. Manage Resumes**
- **Rename:** Click the edit icon
- **Delete:** Click the trash icon

---

## 📊 Server Status Check

### **Check if servers are running:**

**PowerShell:**
```powershell
netstat -ano | findstr "LISTENING" | findstr -E "5000|5001|8000"
```

**Should see:**
- `0.0.0.0:5000` - Auth server ✅
- `0.0.0.0:5001` - API server ✅
- `0.0.0.0:8000` - Frontend server ✅

---

## 🔧 Troubleshooting

### **Problem: "Backend server not running"**
**Solution:** Start all 3 servers (see above)

### **Problem: "Database error"**
**Solution:** Make sure PostgreSQL is running:
```powershell
Get-Service postgresql-x64-16
```
If stopped, start it:
```powershell
Start-Service postgresql-x64-16
```

### **Problem: "File upload fails"**
**Solution:** 
1. Check file is PDF or DOCX
2. Check file is under 10MB
3. Make sure `api.py` is running on port 5001

### **Problem: "AI responses not working"**
**Solution:** Check if `ResumeGeneratorAgent` is imported correctly in `api.py`

---

## 🗄️ Database Tables Created

When you first run `api.py`, it creates these tables:
- `users` - User accounts (from auth.py)
- `saved_resumes` - Saved resume library
- `chat_sessions` - AI chat conversations
- `chat_messages` - Individual chat messages
- `generated_resumes` - AI-generated tailored resumes

### **View in pgAdmin:**
1. Open pgAdmin
2. Connect to PostgreSQL 16
3. Database: `alignai_db`
4. Schemas > public > Tables

---

## 📝 API Endpoints (Port 5001)

### **Resume Operations:**
- `POST /api/resume/upload` - Upload & parse file
- `POST /api/resume/save` - Save to library
- `GET /api/resume/list` - List all resumes
- `GET /api/resume/<id>` - Get specific resume
- `DELETE /api/resume/<id>` - Delete resume
- `PUT /api/resume/<id>/rename` - Rename resume

### **Chat Operations:**
- `POST /api/chat/message` - Send chat message, get AI response

### **Utility:**
- `GET /api/health` - Check API status

---

## 🎨 Technology Stack

### **Frontend:**
- HTML5
- CSS3 (Grid, Flexbox, Animations)
- Vanilla JavaScript (ES6+)
- Font Awesome Icons

### **Backend:**
- Flask (Python web framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)

### **AI:**
- ResumeGeneratorAgent (your existing AI)
- Google Gemini (via google-generativeai)

---

## 💡 Next Steps

1. ✅ **Test file upload** with your resume
2. ✅ **Try the AI chat** with real job descriptions
3. ✅ **Build up your resume library**
4. 🔜 **Test AI generation** with different JDs
5. 🔜 **Download generated resumes** (feature coming)

---

## 🚨 Important Notes

- **Keep all 3 servers running** while using the app
- **Don't close terminal windows** where servers are running
- **PostgreSQL must be running** for database operations
- **Session expires** if you close browser (normal behavior)

---

## ✨ You're All Set!

Your AlignAI dashboard is fully functional with:
- 🎯 Real file parsing
- 💾 Database storage
- 🤖 AI integration
- 📚 Resume library
- 💬 Interactive chat

**Happy aligning!** 🚀✨

---

## 🆘 Need Help?

If something's not working:
1. Check all 3 servers are running
2. Check PostgreSQL is running
3. Check browser console for errors (F12)
4. Check terminal output for error messages
5. Restart all servers and try again

