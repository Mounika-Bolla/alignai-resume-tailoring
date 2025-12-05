# 🧠 RAG Architecture - AlignAI

**Complete Guide to Retrieval-Augmented Generation System**

---

## 📋 Table of Contents

1. [What is RAG?](#what-is-rag)
2. [Architecture Overview](#architecture-overview)
3. [Tech Stack](#tech-stack)
4. [How It Works](#how-it-works)
5. [API Endpoints](#api-endpoints)
6. [Usage Examples](#usage-examples)
7. [Continuous Learning](#continuous-learning)

---

## 🎯 What is RAG?

**RAG (Retrieval-Augmented Generation)** combines two powerful AI capabilities:

1. **Retrieval**: Finding relevant information from a knowledge base
2. **Generation**: Using LLM to create intelligent responses based on retrieved context

### Why RAG for Resume Tailoring?

Traditional chatbots forget context. RAG systems:
- ✅ **Remember** your entire resume and job requirements
- ✅ **Retrieve** relevant sections when generating content
- ✅ **Generate** contextually accurate, tailored responses
- ✅ **Learn** from your feedback continuously

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AlignAI RAG System                       │
└─────────────────────────────────────────────────────────────┘

                    USER UPLOADS
                    ┌──────────┐
                    │ Resume   │
                    │    +     │
                    │   JD     │
                    └────┬─────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  Document Processing   │
            │  - PDF/DOCX Parser     │
            │  - Text Extraction     │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │   Text Chunking        │
            │   (1000 chars/chunk)   │
            │   200 char overlap     │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │  Embedding Generation  │
            │  Google Gemini         │
            │  embedding-001         │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │   Vector Database      │
            │   ChromaDB (Local)     │
            │   Stores embeddings    │
            └────────┬───────────────┘
                     │
                     ▼
       ┌─────────────────────────────────┐
       │        RAG PIPELINE             │
       │                                 │
       │  1. User Query/Instruction      │
       │          ↓                      │
       │  2. Semantic Search (Top 5)     │
       │          ↓                      │
       │  3. Context Retrieval           │
       │          ↓                      │
       │  4. LLM Generation (Gemini)     │
       │          ↓                      │
       │  5. Tailored Content            │
       └─────────────┬───────────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │   User Feedback        │
            │   Rating + Comments    │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │  Continuous Learning   │
            │  Store in Vector DB    │
            │  Improve Future Gens   │
            └────────────────────────┘
```

---

## 🛠️ Tech Stack

### Core Components

| Component | Technology | Purpose | Free? |
|-----------|-----------|---------|-------|
| **LLM** | Google Gemini Pro | Text generation | ✅ Yes |
| **Embeddings** | Gemini embedding-001 | Vector embeddings | ✅ Yes |
| **Vector DB** | FAISS | Store/retrieve vectors | ✅ Yes |
| **Framework** | LangChain | Orchestration | ✅ Yes |
| **Text Processing** | NLTK | Tokenization | ✅ Yes |

### Dependencies

```python
# Core RAG
google-generativeai==0.3.2     # Gemini LLM
langchain==0.1.6               # Orchestration
langchain-google-genai==0.0.6  # Gemini integration
faiss-cpu                      # Vector database (Windows-friendly)
sentence-transformers==2.3.1   # Embeddings
tiktoken==0.5.2                # Token counting
```

---

## 🔄 How It Works

### Step-by-Step Process

#### 1. **Document Ingestion**

```python
# User uploads resume + job description
POST /api/rag/analyze
{
    "resume_text": "...",
    "job_description": "..."
}
```

**What happens:**
- Documents are split into chunks (1000 chars each, 200 overlap)
- Each chunk is converted to a vector embedding
- Vectors are stored in ChromaDB with metadata
- Creates a searchable knowledge base

#### 2. **Semantic Search**

When user asks: *"Emphasize my Python experience"*

```python
POST /api/rag/tailor
{
    "instruction": "Emphasize my Python experience"
}
```

**What happens:**
- Instruction is converted to embedding
- System finds top 5 most similar chunks
- These chunks contain relevant resume sections

#### 3. **Context-Aware Generation**

```python
# System builds prompt:
CONTEXT: [Retrieved resume sections mentioning Python]
USER REQUEST: Emphasize my Python experience
JOB REQUIREMENTS: [Relevant JD sections]

# Gemini generates tailored content
```

#### 4. **Continuous Learning**

```python
POST /api/rag/feedback
{
    "instruction": "Emphasize Python",
    "generated_content": "...",
    "feedback": "Good but add Flask",
    "rating": 4
}
```

**What happens:**
- Feedback is embedded and stored
- Future generations consider past feedback
- System learns user preferences

---

## 🌐 API Endpoints

### 1. Analyze & Ingest

**Endpoint:** `POST /api/rag/analyze`

**Purpose:** Analyze resume + JD and create vector database

```json
Request:
{
    "resume_text": "Full resume text",
    "job_description": "Full JD text"
}

Response:
{
    "success": true,
    "result": {
        "resume_analysis": {...},
        "job_analysis": {...},
        "rag_ingestion": {
            "chunks_created": 15,
            "collection": "alignai_resumes_123"
        },
        "ai_suggestions": [
            "Add quantifiable metrics",
            "Emphasize cloud technologies",
            "..."
        ]
    }
}
```

### 2. Tailor Content

**Endpoint:** `POST /api/rag/tailor`

**Purpose:** Generate tailored content from instruction

```json
Request:
{
    "instruction": "Rewrite my experience to match data scientist role"
}

Response:
{
    "success": true,
    "result": {
        "tailored_content": "• Developed machine learning models...",
        "source_documents": ["chunk1", "chunk2"],
        "instruction": "..."
    }
}
```

### 3. Get Suggestions

**Endpoint:** `POST /api/rag/suggestions`

**Purpose:** Get AI-powered improvement suggestions

```json
Request:
{
    "resume_text": "...",
    "job_description": "..."
}

Response:
{
    "success": true,
    "suggestions": [
        "Add Python to technical skills section",
        "Quantify achievements with metrics",
        "Include cloud technologies experience",
        "..."
    ]
}
```

### 4. Submit Feedback

**Endpoint:** `POST /api/rag/feedback`

**Purpose:** Learn from user feedback

```json
Request:
{
    "instruction": "Emphasize Python",
    "generated_content": "...",
    "feedback": "Add more Flask examples",
    "rating": 4
}

Response:
{
    "success": true,
    "result": {
        "learning_status": "stored",
        "refined_content": "Improved version...",
        "improvement_applied": true
    }
}
```

### 5. RAG Chat

**Endpoint:** `POST /api/rag/chat`

**Purpose:** Natural conversation for resume tailoring

```json
Request:
{
    "message": "How can I make my resume better for this job?"
}

Response:
{
    "success": true,
    "response": "Based on your resume and the JD, I suggest..."
}
```

---

## 💡 Usage Examples

### Example 1: Upload & Analyze

```javascript
// Frontend code
const analyzeResume = async () => {
    const response = await fetch('/api/rag/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            resume_text: resumeText,
            job_description: jdText
        })
    });
    
    const data = await response.json();
    console.log('Suggestions:', data.result.ai_suggestions);
};
```

### Example 2: Interactive Tailoring

```javascript
const tailorContent = async (instruction) => {
    const response = await fetch('/api/rag/tailor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instruction })
    });
    
    const data = await response.json();
    displayTailoredContent(data.result.tailored_content);
};

// Usage
tailorContent("Emphasize my machine learning experience");
tailorContent("Add quantifiable metrics to all achievements");
tailorContent("Rewrite experience for senior engineer role");
```

### Example 3: Learning Loop

```javascript
const submitFeedback = async (content, userFeedback) => {
    const response = await fetch('/api/rag/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            instruction: currentInstruction,
            generated_content: content,
            feedback: userFeedback,
            rating: 4
        })
    });
    
    const data = await response.json();
    if (data.result.improvement_applied) {
        displayRefinedContent(data.result.refined_content);
    }
};
```

---

## 🔄 Continuous Learning

### How the System Learns

1. **Initial Generation**
   - System generates content based on resume + JD

2. **User Feedback**
   - User rates content (1-5)
   - Provides specific feedback text
   - Accepts/rejects/modifies output

3. **Storage**
   - Feedback is embedded as new document
   - Stored in same vector database
   - Tagged with rating and metadata

4. **Future Improvements**
   - When similar requests come in
   - System retrieves past feedback
   - Incorporates learned preferences
   - Generates better content

### Feedback Loop Diagram

```
User Request → Generate → User Feedback → Store → Next Request
       ↑                                               ↓
       └──────────── Improved Generation ←────────────┘
```

---

## 🚀 Getting Started

### 1. Get Google Gemini API Key (Free)

Visit: https://makersuite.google.com/app/apikey

1. Sign in with Google account
2. Click "Get API Key"
3. Copy the key

### 2. Configure Environment

```bash
# Copy template
cp env.template .env

# Edit .env and add:
GEMINI_API_KEY=your-gemini-api-key-here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test RAG System

```python
from agents.rag_engine import get_rag_engine

# Initialize
engine = get_rag_engine()

# Ingest documents
result = engine.ingest_documents(
    resume_text="My resume...",
    job_description="Job requirements...",
    user_id="test_user"
)

# Generate content
output = engine.generate_tailored_content(
    instruction="Emphasize Python experience",
    user_id="test_user"
)

print(output['tailored_content'])
```

---

## 📊 Performance & Limits

### Google Gemini Free Tier

- **60 requests per minute**
- **1500 requests per day**
- Sufficient for development and testing

### ChromaDB

- **Local storage** (no limits)
- **Fast retrieval** (<100ms)
- **Persistent** between sessions

### Scalability

For production:
- Upgrade to Gemini Pro paid (higher limits)
- Switch to Pinecone for cloud vector DB
- Implement caching layer

---

## 🎯 Key Benefits

1. **Context-Aware**: Never forgets resume content
2. **Personalized**: Learns individual preferences
3. **Fast**: Semantic search in milliseconds
4. **Free**: Uses Google Gemini free tier
5. **Scalable**: Easy to upgrade components

---

## 🔍 Troubleshooting

### "API Key not found"
- Check .env file has `GEMINI_API_KEY`
- Restart server after adding key

### "Vector store not initialized"
- Must call `/api/rag/analyze` first
- Creates user-specific collection

### "Rate limit exceeded"
- Gemini free tier: 60 req/min
- Wait or upgrade to paid tier

---

**Built with ❤️ using Google Gemini + LangChain + ChromaDB**

