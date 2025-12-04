# 🚀 API Integration Guide - Clean Code Structure

## What We Changed

### ✅ **Before:** Hardcoded sample data inside functions
```python
def test_complete_pipeline():
    # 200+ lines of hardcoded sample data here
    job_description = """..."""
    resume_text = """..."""
```

### ✅ **After:** Clean, API-ready functions
```python
def generate_tailored_resume(job_description: str, resume_text: str, 
                             output_filename: str = "tailored_resume.tex") -> dict:
    """Main API function - accepts parameters, returns structured results"""
```

---

## New File Structure

```
resumetailoring/
├── base_agent.py              # Tool #0 - Gemini API
├── job_analyzer.py            # Tool #1 - Job Analysis
├── resume_analyzer.py         # Tool #2 - Resume Analysis
├── strategy_creator.py        # Tool #3 - Strategy Creation
├── resume_generator.py        # Tool #4 - Resume Generation
├── resume_template.tex        # LaTeX template
│
├── main.py                    # ← CLEAN API-ready functions (no hardcoded data!)
└── sample_data.py             # ← Test data separated out
```

---

## 🔌 Core API Functions in main.py

### Function 1: `generate_tailored_resume()` - MAIN ENDPOINT

```python
from main import generate_tailored_resume

result = generate_tailored_resume(
    job_description="Your job posting text",
    resume_text="Candidate's resume text",
    output_filename="tailored_resume.tex"
)

# Returns:
{
    'success': True,
    'output_file': 'tailored_resume.tex',
    'analysis_file': 'tailored_resume_analysis.json',
    'match_score': 85,
    'message': 'Resume generated successfully with 85/100 match score'
}
```

**Use this for:** Full resume generation (all 4 tools)

---

### Function 2: `analyze_job_and_resume()` - Quick Analysis

```python
from main import analyze_job_and_resume

result = analyze_job_and_resume(
    job_description="Job posting text",
    resume_text="Candidate's resume text"
)

# Returns:
{
    'success': True,
    'job_analysis': {...},
    'resume_data': {...},
    'strategy': {...},
    'match_score': 85,
    'message': 'Analysis completed successfully'
}
```

**Use this for:** Quick match score without generating the full resume

---

### Function 3: `test_individual_tools()` - Debugging

```python
from main import test_individual_tools

test_individual_tools(
    job_description="Job text",
    resume_text="Resume text"
)
```

**Use this for:** Testing/debugging each tool separately

---

## 🌐 Example Flask API Integration

Here's how to integrate with Flask:

```python
# api.py - Your Flask backend
from flask import Flask, request, jsonify, send_file
from main import generate_tailored_resume, analyze_job_and_resume

app = Flask(__name__)

@app.route('/api/generate-resume', methods=['POST'])
def api_generate_resume():
    """Generate tailored resume endpoint"""
    data = request.json
    
    job_description = data.get('job_description')
    resume_text = data.get('resume_text')
    
    if not job_description or not resume_text:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Call your main function
    result = generate_tailored_resume(
        job_description=job_description,
        resume_text=resume_text,
        output_filename=f"resume_{data.get('user_id', 'test')}.tex"
    )
    
    return jsonify(result)


@app.route('/api/quick-analysis', methods=['POST'])
def api_quick_analysis():
    """Quick match score endpoint"""
    data = request.json
    
    result = analyze_job_and_resume(
        job_description=data.get('job_description'),
        resume_text=data.get('resume_text')
    )
    
    return jsonify(result)


@app.route('/api/download-resume/<filename>', methods=['GET'])
def api_download_resume(filename):
    """Download generated resume"""
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🎯 Example FastAPI Integration

```python
# api.py - Your FastAPI backend
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import generate_tailored_resume, analyze_job_and_resume

app = FastAPI()

class ResumeRequest(BaseModel):
    job_description: str
    resume_text: str
    user_id: str = "test"

@app.post("/api/generate-resume")
async def generate_resume_endpoint(request: ResumeRequest):
    """Generate tailored resume"""
    result = generate_tailored_resume(
        job_description=request.job_description,
        resume_text=request.resume_text,
        output_filename=f"resume_{request.user_id}.tex"
    )
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['message'])
    
    return result

@app.post("/api/quick-analysis")
async def quick_analysis_endpoint(request: ResumeRequest):
    """Get quick match score"""
    result = analyze_job_and_resume(
        job_description=request.job_description,
        resume_text=request.resume_text
    )
    
    if not result['success']:
        raise HTTPException(status_code=500, detail=result['message'])
    
    return result

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download generated resume"""
    return FileResponse(filename, media_type='application/x-tex')
```

---

## 🧪 Testing Your Clean Code

### Test Mode 1: Full Pipeline
```bash
python main.py
# Choose option 1
```

### Test Mode 2: Individual Tools (Learning)
```bash
python main.py
# Choose option 2
```

### Test Mode 3: Quick Analysis Only
```bash
python main.py
# Choose option 3
```

### Test Mode 4: API Function Test (Recommended for Backend Dev)
```bash
python main.py
# Choose option 4
```

---

## 📝 Using Custom Data

### Option 1: Edit sample_data.py
```python
# sample_data.py
SAMPLE_JOB_DESCRIPTION = """
Your actual job posting here
"""

SAMPLE_RESUME = """
Your actual resume here
"""
```

### Option 2: Load from Files
```python
# In your API
with open('job_posting.txt', 'r') as f:
    job_description = f.read()

with open('resume.txt', 'r') as f:
    resume_text = f.read()

result = generate_tailored_resume(job_description, resume_text)
```

### Option 3: Direct API Calls
```python
# From your frontend POST request
import requests

response = requests.post('http://localhost:5000/api/generate-resume', json={
    'job_description': 'Job text from user input',
    'resume_text': 'Resume text from user upload',
    'user_id': 'user123'
})

result = response.json()
print(f"Match Score: {result['match_score']}/100")
```

---

## 🎨 Example React Frontend Integration

```javascript
// ResumeGenerator.jsx
import React, { useState } from 'react';

function ResumeGenerator() {
    const [jobDescription, setJobDescription] = useState('');
    const [resumeText, setResumeText] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const generateResume = async () => {
        setLoading(true);
        
        const response = await fetch('/api/generate-resume', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                job_description: jobDescription,
                resume_text: resumeText
            })
        });
        
        const data = await response.json();
        setResult(data);
        setLoading(false);
    };

    return (
        <div>
            <h1>Resume Tailoring System</h1>
            
            <textarea 
                placeholder="Paste job description"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
            />
            
            <textarea 
                placeholder="Paste your resume"
                value={resumeText}
                onChange={(e) => setResumeText(e.target.value)}
            />
            
            <button onClick={generateResume} disabled={loading}>
                {loading ? 'Generating...' : 'Generate Tailored Resume'}
            </button>
            
            {result && result.success && (
                <div>
                    <h2>Match Score: {result.match_score}/100</h2>
                    <a href={`/api/download/${result.output_file}`}>
                        Download Resume (.tex)
                    </a>
                </div>
            )}
        </div>
    );
}

export default ResumeGenerator;
```

---

## ✨ Key Benefits of This Structure

### ✅ Clean Code
- No hardcoded data in main logic
- Easy to read and maintain
- Professional structure

### ✅ API-Ready
- Functions accept parameters
- Return structured JSON responses
- Easy to integrate with any backend

### ✅ Flexible Testing
- Sample data separated in `sample_data.py`
- Multiple test modes
- Easy to add new test cases

### ✅ Production-Ready
- Error handling built-in
- Returns success/failure status
- Includes helpful error messages

---

## 🔍 Quick Comparison

### ❌ OLD WAY (Hardcoded)
```python
def test():
    job = """
    ... 200 lines of hardcoded data ...
    """
    # Can't use this in API!
```

### ✅ NEW WAY (Clean)
```python
def generate_tailored_resume(job_description: str, resume_text: str) -> dict:
    """Ready to call from anywhere!"""
    # From API, from tests, from CLI, etc.
```

---

## 📚 Summary

1. **Separation of Concerns**
   - Logic in `main.py`
   - Test data in `sample_data.py`
   - Agents in separate modules

2. **API-Ready Functions**
   - `generate_tailored_resume()` - Main endpoint
   - `analyze_job_and_resume()` - Quick analysis
   - All return structured JSON

3. **Flexible Usage**
   - Can be called from Flask/FastAPI
   - Can be tested standalone
   - Can be imported anywhere

4. **Production Ready**
   - Error handling
   - Type hints
   - Clear documentation

---

## 🚀 Next Steps

1. **Test the clean code:**
   ```bash
   python main.py
   ```

2. **Create your API:**
   - Use Flask or FastAPI example above
   - Import functions from `main.py`
   - Add your endpoints

3. **Build frontend:**
   - React, Vue, or any framework
   - Call your API endpoints
   - Display results to users

4. **Deploy:**
   - Backend: Heroku, AWS, GCP
   - Frontend: Vercel, Netlify
   - Database for storing resumes (optional)

---

**Your code is now clean, professional, and ready for web integration! 🎉**

