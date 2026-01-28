# AlignAI — AI-Powered Resume Tailoring

AlignAI is a resume tailoring system that combines retrieval-augmented generation (RAG) with a multi-agent pipeline to generate professionally formatted LaTeX resumes tailored to specific job descriptions.

This repository includes a web interface, a Flask API backend, an agent-based pipeline for parsing and analyzing resumes and job descriptions, a FAISS-backed vector store for semantic search, and LaTeX resume generation for use with Overleaf.

## Key Features

- RAG-enabled contextual retrieval for precise content generation
- Four-agent pipeline:
  - Job Analyzer — extracts requirements and keywords from job descriptions
  - Resume Analyzer — parses and structures resume content
  - Strategy Creator — matches resume content to job requirements and identifies gaps
  - Resume Generator — produces tailored LaTeX resumes
- FAISS vector database for semantic search and fast retrieval
- Session persistence for chat history and resume drafts
- LaTeX output compatible with Overleaf
- Extensible architecture designed for iterative improvement

## Architecture and Components

Top-level structure:

```
resumetailoring/
├── frontend/                  # Web interface (HTML/CSS/JS)
├── backend/                   # Flask API server
├── agents/                    # Agent implementations and RAG engine
├── tests/                     # Test templates and sample data
├── docs/                      # Design and architecture documentation
├── start.py                   # Startup script
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables (not checked in)
```

Agent files (agents/):
- base_agent.py — LLM and common agent utilities
- job_analyzer.py — job description analysis
- resume_analyzer.py — resume parsing and extraction
- strategy_creator.py — matching strategy and action items
- resume_generator.py — LaTeX generation
- rag_engine.py — vector store and retrieval
- rag_resume_agent.py — orchestrates RAG with agents

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Mounika-Bolla/alignai-resume-tailoring.git
cd alignai-resume-tailoring
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure PostgreSQL (example for Windows PowerShell):
```powershell
# Start the service if needed (run as Administrator)
Start-Service postgresql-x64-16

# Create the database
psql -U postgres -c "CREATE DATABASE alignai_db;"
```

4. Create a `.env` file in the project root with the following variables:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=alignai_db

GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-secret-key-here
```

5. Start the application:
```bash
python start.py
```

6. Open the UI in a browser:
- Homepage: http://localhost:8000/index.html
- Login:    http://localhost:8000/login.html
- Dashboard: http://localhost:8000/dashboard.html

## Usage Overview

- Upload a resume (PDF or DOCX) and provide a job description.
- The system ingests both into the FAISS vector store for retrieval.
- Run individual agents or the full pipeline:
  - Analyze job — extracts required skills and keywords
  - Analyze resume — extracts skills, experience, and education
  - Create strategy — computes match score, identifies gaps, suggests actions
  - Generate resume — produces a tailored LaTeX file
- Download the generated `.tex` file and open in Overleaf to compile to PDF.

## API Endpoints

Agent endpoints:
- POST /api/agent/analyze-job — Analyze job description
- POST /api/agent/analyze-resume — Parse resume
- POST /api/agent/create-strategy — Build matching strategy
- POST /api/agent/full-pipeline — Run the full pipeline

RAG endpoints:
- POST /api/rag/analyze — Ingest resume + job description into vector store
- POST /api/rag/tailor — Generate content using retrieved context
- POST /api/rag/suggestions — Get improvement suggestions
- POST /api/rag/chat — Conversational interface with RAG context

Authentication:
- POST /api/auth/signup
- POST /api/auth/login
- POST /api/auth/logout
- GET  /api/auth/check-session

Resume management:
- POST   /api/resume/upload
- POST   /api/resume/save
- GET    /api/resume/list
- DELETE /api/resume/{id}

## LaTeX Resume Output

Generated resumes use a clean, ATS-friendly LaTeX template suitable for Overleaf:

```latex
\documentclass[letterpaper,11pt]{article}
% ATS-optimized formatting
```

Workflow:
1. Generate tailored resume
2. Download the `.tex` file
3. Upload to Overleaf and compile to PDF

## Persistence and Sessions

- Resume text and job descriptions are cached in the browser for session continuity.
- Chat history is preserved and reloaded for convenience.
- Auto re-ingest is performed on page refresh.

## Troubleshooting

- Module not found:
  ```bash
  pip install -r requirements.txt
  ```

- PostgreSQL not running (Windows example):
  ```powershell
  Start-Service postgresql-x64-16
  ```

- Port in use:
  ```powershell
  netstat -ano | findstr "5000"
  taskkill /PID [PID] /F
  ```

- GEMINI_API_KEY issues:
  1. Obtain a key: https://makersuite.google.com/app/apikey
  2. Add to `.env`
  3. Restart the application

- Vector store empty after refresh:
  - The system auto re-ingests; check server logs for confirmation.

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- Database: PostgreSQL
- Vector store: FAISS
- LLM: Google Gemini (configurable)
- RAG framework: LangChain
- Embeddings: Google Generative AI

## Database Schema (summary)

- users (id, full_name, email, password_hash, created_at, last_login)
- saved_resumes (id, user_id, name, content, file_type, created_at)
- chat_sessions (id, user_id, created_at)
- chat_messages (id, session_id, role, content, created_at)

## Security & Production Notes

- Use strong, unique values for SECRET_KEY and other sensitive settings in production.
- Serve the application behind HTTPS and a production WSGI server (e.g., Gunicorn).
- Configure database backups and credentials via environment variables or a secrets manager.
- Implement rate limiting and authentication hardening as needed.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a pull request

Please include tests and update documentation when adding or changing functionality.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

Repository: [AlignAI on GitHub](https://github.com/Mounika-Bolla/alignai-resume-tailoring)
