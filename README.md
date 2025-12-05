# 🎯 AlignAI - AI-Powered Resume Tailoring System

**Intelligent Resume Optimization using RAG (Retrieval-Augmented Generation) + 4-Tool Agent Pipeline**

Transform your resume with AI that learns and adapts to your needs. AlignAI uses Google Gemini, advanced RAG technology, and a 4-tool agent pipeline to create perfectly tailored LaTeX resumes for any job.

![AlignAI Dashboard](frontend/assets/logo.png)

---

## ✨ Key Features

🧠 **RAG-Powered Intelligence** - Retrieves relevant context from your resume and generates tailored content  
🤖 **4-Tool Agent Pipeline** - Job Analyzer → Resume Analyzer → Strategy Creator → Resume Generator  
📚 **FAISS Vector Database** - Fast semantic search (Windows-friendly, no C++ build required)  
💾 **Session Persistence** - Chat history and resume saved like ChatGPT  
📄 **LaTeX Resume Generation** - Download professional `.tex` files for Overleaf  
💬 **Claude-Style Interface** - Beautiful beige/brown themed chat UI  
🔄 **Continuous Learning** - System improves from your feedback

---

## 🤖 The 4-Tool Agent Pipeline

AlignAI uses a sophisticated multi-agent system:

| Tool | Agent File | Description |
|------|------------|-------------|
| **Tool 1** | `job_analyzer.py` | Analyzes job descriptions, extracts skills, keywords, requirements |
| **Tool 2** | `resume_analyzer.py` | Parses your resume, extracts skills, experience, education |
| **Tool 3** | `strategy_creator.py` | Creates matching strategy with score, gaps, action items |
| **Tool 4** | `resume_generator.py` | Generates tailored LaTeX resume following the strategy |

**Inheritance Chain:** `BaseAgent` → `JobAnalyzerAgent` → `ResumeAgent` → `StrategyAgent` → `ResumeGeneratorAgent`

---

## 📁 Project Structure

```
resumetailoring/
├── frontend/                  # Web interface
│   ├── index.html            # Landing page
│   ├── login.html            # Authentication
│   ├── dashboard.html        # Main app (Claude-style UI)
│   └── assets/               # Images, logo
├── backend/                   # Flask API server
│   └── server.py             # All endpoints (auth, resume, RAG, agents)
├── agents/                    # AI agents (4 tools + RAG)
│   ├── base_agent.py         # Gemini setup
│   ├── job_analyzer.py       # Tool 1: Job analysis
│   ├── resume_analyzer.py    # Tool 2: Resume parsing
│   ├── strategy_creator.py   # Tool 3: Strategy creation
│   ├── resume_generator.py   # Tool 4: LaTeX generation
│   ├── rag_engine.py         # RAG system with FAISS
│   └── rag_resume_agent.py   # Combines RAG + agents
├── tests/
│   ├── templates/            # LaTeX templates
│   │   └── resume_template.tex
│   └── sample_data.py
├── docs/                      # Documentation
│   ├── RAG_ARCHITECTURE.md
│   └── PROJECT_STRUCTURE.md
├── start.py                   # One-command startup
├── requirements.txt           # Dependencies
└── .env                       # API keys (create this)
```

---

## 🚀 Quick Start

### **1. Clone & Install**

```bash
git clone https://github.com/Mounika-Bolla/alignai-resume-tailoring.git
cd alignai-resume-tailoring
pip install -r requirements.txt
```

### **2. Setup PostgreSQL**

```powershell
# Check if running
Get-Service postgresql*

# Start if needed (run as Admin)
Start-Service postgresql-x64-16

# Create database
psql -U postgres -c "CREATE DATABASE alignai_db;"
```

### **3. Configure `.env` File**

Create a `.env` file in the project root:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=alignai_db

# Google Gemini API (FREE!)
# Get your key: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your-gemini-api-key-here

# Security
SECRET_KEY=your-secret-key-here
```

### **4. Run the Application**

```bash
python start.py
```

### **5. Open in Browser**

| Page | URL |
|------|-----|
| 🏠 Homepage | http://localhost:8000/index.html |
| 🔐 Login | http://localhost:8000/login.html |
| 📊 Dashboard | http://localhost:8000/dashboard.html |

---

## 🎮 How to Use

### **Basic Flow:**

1. **Upload Resume** - Click "Upload" → Select PDF/DOCX → Paste job description
2. **Analyze with RAG** - Creates vector database, shows AI suggestions
3. **Use Agent Tools** - Click individual tools or run full pipeline
4. **Generate Resume** - Get tailored LaTeX file → Download → Open in Overleaf

### **Available Actions:**

```
💡 Quick Actions:
[Emphasize my technical skills] [Add quantifiable metrics] [Make it ATS-friendly]

🤖 Agent Tools:
[📋 Analyze Job]      - Tool 1: Extract requirements, keywords
[📄 Analyze Resume]   - Tool 2: Parse skills, experience
[🧠 Create Strategy]  - Tool 3: Match score, gaps, action plan
[✨ Generate Resume]  - Tool 4: Create LaTeX file

🚀 Full Pipeline:
[🔥 Run All 4 Tools & Generate LaTeX]
```

### **Natural Language Commands:**

Just type in the chat:
- "Emphasize my Python and machine learning experience"
- "Add quantifiable metrics to all achievements"
- "Make my resume ATS-friendly"
- "Generate tailored resume"

---

## 🔧 API Endpoints

### **Agent Tools**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/agent/analyze-job` | Tool 1: Analyze job description |
| POST | `/api/agent/analyze-resume` | Tool 2: Analyze resume |
| POST | `/api/agent/create-strategy` | Tool 3: Create matching strategy |
| POST | `/api/agent/full-pipeline` | Run all 4 tools |
| POST | `/api/resume/generate-tailored` | Generate LaTeX resume |

### **RAG System**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/rag/analyze` | Ingest resume + JD into vector store |
| POST | `/api/rag/tailor` | Generate content from instruction |
| POST | `/api/rag/suggestions` | Get AI improvement suggestions |
| POST | `/api/rag/chat` | Natural language chat |

### **Authentication**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| GET | `/api/auth/check-session` | Check authentication |

### **Resume Management**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/resume/upload` | Upload PDF/DOCX |
| POST | `/api/resume/save` | Save to library |
| GET | `/api/resume/list` | List all resumes |
| DELETE | `/api/resume/<id>` | Delete resume |

---

## 💾 Session Persistence

**Like ChatGPT** - Your data persists across browser sessions:

- ✅ Resume text saved to localStorage
- ✅ Job description saved
- ✅ Chat history preserved
- ✅ Auto re-ingest on page refresh
- ✅ Data persists for 7 days

**Clear Options:**
- "New Chat" - Clears chat, keeps resume
- "Clear History" (user menu) - Clears everything

---

## 📄 LaTeX Resume Output

Generated resumes use a professional LaTeX template:

```latex
\documentclass[letterpaper,11pt]{article}
% ATS-optimized formatting
% Clean, professional layout
% Ready for Overleaf
```

**To use:**
1. Click "Generate tailored resume"
2. Download `.tex` file
3. Open [Overleaf.com](https://overleaf.com)
4. Upload file → Compile → Download PDF

---

## 🛠️ Troubleshooting

### **"Module not found" errors**
```bash
pip install -r requirements.txt
```

### **PostgreSQL not running**
```powershell
# Run as Administrator
Start-Service postgresql-x64-16
```

### **Port already in use**
```powershell
netstat -ano | findstr "5000"
taskkill /PID [PID] /F
```

### **GEMINI_API_KEY error**
1. Get free key: https://makersuite.google.com/app/apikey
2. Add to `.env` file
3. Restart servers

### **Vector store empty after refresh**
- This is normal - auto re-ingest happens after 1 second
- Check console for "✅ RAG system ready!"

---

## 📚 Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python, Flask |
| **Database** | PostgreSQL |
| **AI/LLM** | Google Gemini 2.5 Flash |
| **Vector Store** | FAISS |
| **Embeddings** | Google Generative AI |
| **RAG Framework** | LangChain |

---

## 🗂️ Database Schema

```sql
-- Users table
users (id, full_name, email, password_hash, created_at, last_login)

-- Saved resumes
saved_resumes (id, user_id, name, content, file_type, created_at)

-- Chat history
chat_sessions (id, user_id, created_at)
chat_messages (id, session_id, role, content, created_at)
```

---

## 🔐 Security Notes

⚠️ **Development Setup** - For production:
- Change `SECRET_KEY` to strong random value
- Use environment variables for secrets
- Enable HTTPS
- Use proper WSGI server (Gunicorn)
- Set up database backups
- Implement rate limiting

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📝 License

MIT License - Feel free to use and modify

---

## 🆘 Need Help?

1. Check `docs/` folder
2. Review console logs (F12)
3. Check server terminal output
4. Open an issue on GitHub

---

**Built with ❤️ for better resumes and better jobs**

🔗 **GitHub:** https://github.com/Mounika-Bolla/alignai-resume-tailoring
