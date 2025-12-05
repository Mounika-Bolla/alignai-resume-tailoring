# 🚀 RAG System - Quick Setup Guide

## ✅ What's Been Added

Your AlignAI project now has a complete **RAG (Retrieval-Augmented Generation)** system!

### New Files Created:
- ✅ `agents/rag_engine.py` - Core RAG engine with Gemini + ChromaDB
- ✅ `agents/rag_resume_agent.py` - RAG-powered resume agent
- ✅ `docs/RAG_ARCHITECTURE.md` - Complete RAG documentation
- ✅ `env.template` - Environment configuration template
- ✅ Updated `requirements.txt` - Added RAG dependencies
- ✅ Updated `backend/server.py` - Added 5 new RAG API endpoints
- ✅ Updated `README.md` - Added RAG features documentation

---

## 🔧 Setup in 3 Steps

### Step 1: Get Free Google Gemini API Key

1. Visit: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy the key (starts with `AIza...`)

### Step 2: Configure Environment

```bash
# Copy template to .env
cp env.template .env

# Edit .env and paste your API key
# GEMINI_API_KEY=AIzaSy... (your actual key)
```

### Step 3: Install New Dependencies

```bash
# Activate virtual environment
& c:/Users/monib/Desktop/resumetailoring/resume/Scripts/Activate.ps1

# Install RAG packages
pip install -r requirements.txt
```

---

## 🎯 How to Use RAG System

### From Frontend (JavaScript)

```javascript
// 1. Upload and analyze resume
const analyzeResponse = await fetch('/api/rag/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        resume_text: resumeText,
        job_description: jdText
    })
});

// 2. Get AI suggestions
const suggestions = await analyzeResponse.json();
console.log(suggestions.result.ai_suggestions);

// 3. Tailor content with natural language
const tailorResponse = await fetch('/api/rag/tailor', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        instruction: "Emphasize my Python and machine learning experience"
    })
});

const tailored = await tailorResponse.json();
console.log(tailored.result.tailored_content);
```

### From Python (Backend Testing)

```python
from agents.rag_engine import get_rag_engine

# Initialize
rag = get_rag_engine()

# Ingest documents
result = rag.ingest_documents(
    resume_text="Your resume...",
    job_description="Job description...",
    user_id="123"
)

# Generate tailored content
output = rag.generate_tailored_content(
    instruction="Emphasize Python skills",
    user_id="123"
)

print(output['tailored_content'])
```

---

## 📡 New API Endpoints

### 1. Analyze & Create Vector Database
```bash
POST /api/rag/analyze
{
    "resume_text": "...",
    "job_description": "..."
}
```

### 2. Tailor with Instructions
```bash
POST /api/rag/tailor
{
    "instruction": "Emphasize Python experience"
}
```

### 3. Get Smart Suggestions
```bash
POST /api/rag/suggestions
{
    "resume_text": "...",
    "job_description": "..."
}
```

### 4. Submit Feedback (Learning)
```bash
POST /api/rag/feedback
{
    "instruction": "...",
    "generated_content": "...",
    "feedback": "Add more Flask examples",
    "rating": 4
}
```

### 5. Natural Chat
```bash
POST /api/rag/chat
{
    "message": "How can I improve my resume?"
}
```

---

## 🧠 RAG Architecture

```
User Input → Document Processing → Chunking → Embeddings
                                                  ↓
                                           Vector Database
                                                  ↓
User Query → Semantic Search → Context Retrieval
                                   ↓
                         LLM Generation (Gemini)
                                   ↓
                         Tailored Content
                                   ↓
                         User Feedback → Learning
```

---

## 🔍 Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| LLM | Google Gemini Pro | 🆓 Free |
| Embeddings | Gemini embedding-001 | 🆓 Free |
| Vector DB | FAISS (Windows-friendly) | 🆓 Free |
| Framework | LangChain | 🆓 Free |

**Total Cost: $0** ✅

---

## 📚 Documentation

- **Complete Guide**: `docs/RAG_ARCHITECTURE.md`
- **API Reference**: `docs/RAG_ARCHITECTURE.md#api-endpoints`
- **Examples**: `docs/RAG_ARCHITECTURE.md#usage-examples`

---

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not found"
→ Check `.env` file exists and contains valid key

### "RAG system not initialized"
→ Make sure Gemini API key is correct

### "Vector store not initialized"
→ Call `/api/rag/analyze` first to create database

### "Module not found: langchain"
→ Run `pip install -r requirements.txt`

---

## 🎉 What's Next?

1. **Test the System**:
   ```bash
   python start.py
   ```

2. **Upload Resume + JD**: Visit http://localhost:8000/dashboard.html

3. **Try Natural Language**:
   - "Make my resume ATS-friendly"
   - "Emphasize leadership experience"
   - "Add quantifiable metrics"

4. **Watch It Learn**: System improves from your feedback!

---

## 📊 Benefits

✅ **Context-Aware**: Never forgets your resume content  
✅ **Personalized**: Learns your preferences  
✅ **Fast**: Millisecond semantic search  
✅ **Free**: Uses Gemini free tier  
✅ **Scalable**: Easy to upgrade components  

---

## 🚀 Push to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Add complete RAG system with Google Gemini, ChromaDB, and LangChain"

# Push to GitHub
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

---

**Your resume tailoring system is now powered by cutting-edge RAG technology! 🎯**

