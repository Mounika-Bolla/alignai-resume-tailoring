# 🎯 Quick Reference - Clean Code Structure

## 📁 File Structure

```
BEFORE (Old):
main.py (268 lines)
├── Import ResumeAgent
├── test_complete_agent()
│   └── 200+ lines of hardcoded sample data ❌
└── Run tests

AFTER (New):
main.py (256 lines, cleaner!)
├── Import ResumeGeneratorAgent
├── generate_tailored_resume() ✅ API-ready function
├── analyze_job_and_resume() ✅ Quick analysis function
├── test_individual_tools() ✅ Accepts parameters
├── test_complete_pipeline() ✅ Accepts parameters
└── Test mode (imports sample_data.py only for tests)

sample_data.py (NEW!)
├── SAMPLE_JOB_DESCRIPTION ✅
├── SAMPLE_RESUME ✅
├── MINIMAL_JOB ✅
└── MINIMAL_RESUME ✅
```

---

## 🔌 Main Functions

### 1️⃣ **Full Resume Generation**
```python
from main import generate_tailored_resume

result = generate_tailored_resume(
    job_description="...",
    resume_text="...",
    output_filename="resume.tex"
)
# Returns: {'success': bool, 'match_score': int, ...}
```

### 2️⃣ **Quick Analysis Only**
```python
from main import analyze_job_and_resume

result = analyze_job_and_resume(
    job_description="...",
    resume_text="..."
)
# Returns: {'success': bool, 'match_score': int, ...}
```

---

## 🧪 Testing

```bash
python main.py
```

**Options:**
1. Complete pipeline (full test)
2. Individual tools (learning mode)
3. Quick analysis (fast test)
4. API function test (backend dev)

---

## 🌐 Backend Integration

### Flask Example
```python
from flask import Flask, request, jsonify
from main import generate_tailored_resume

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    result = generate_tailored_resume(
        data['job_description'],
        data['resume_text']
    )
    return jsonify(result)
```

### FastAPI Example
```python
from fastapi import FastAPI
from main import generate_tailored_resume

app = FastAPI()

@app.post("/api/generate")
async def generate(job: str, resume: str):
    return generate_tailored_resume(job, resume)
```

---

## 📊 Response Format

### Success Response
```json
{
    "success": true,
    "output_file": "tailored_resume.tex",
    "analysis_file": "tailored_resume_analysis.json",
    "match_score": 85,
    "message": "Resume generated successfully with 85/100 match score"
}
```

### Error Response
```json
{
    "success": false,
    "output_file": null,
    "analysis_file": null,
    "match_score": 0,
    "message": "Error: [error details]"
}
```

---

## 🎨 Frontend Example

```javascript
// Call your API
const response = await fetch('/api/generate-resume', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        job_description: jobText,
        resume_text: resumeText
    })
});

const result = await response.json();

if (result.success) {
    console.log(`Match Score: ${result.match_score}/100`);
    window.location.href = `/download/${result.output_file}`;
}
```

---

## ✅ Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| **Data Location** | Hardcoded in functions | Separated in `sample_data.py` |
| **Function Parameters** | None (hardcoded) | Accept job & resume as params |
| **Return Values** | Prints to console | Returns structured dict |
| **API Ready** | ❌ No | ✅ Yes |
| **Testing** | Hardcoded samples | Flexible test modes |
| **Maintainability** | Hard to change | Easy to modify |
| **Reusability** | Only for testing | Use anywhere |

---

## 🚀 Usage Patterns

### Pattern 1: Direct API Call
```python
# Your backend
from main import generate_tailored_resume

result = generate_tailored_resume(
    job_from_frontend,
    resume_from_frontend
)
```

### Pattern 2: File Input
```python
with open('job.txt') as f:
    job = f.read()
with open('resume.txt') as f:
    resume = f.read()

result = generate_tailored_resume(job, resume)
```

### Pattern 3: Database Integration
```python
# Get from database
job = db.jobs.find_one({'id': job_id})['description']
resume = db.resumes.find_one({'user_id': user_id})['text']

result = generate_tailored_resume(job, resume)

# Save result
db.generated_resumes.insert_one({
    'user_id': user_id,
    'job_id': job_id,
    'match_score': result['match_score'],
    'output_file': result['output_file']
})
```

---

## 💡 Pro Tips

1. **Keep sample_data.py for testing**
   - Update with realistic examples
   - Add edge cases
   - Test different job types

2. **Use type hints**
   ```python
   def generate_tailored_resume(
       job_description: str,
       resume_text: str,
       output_filename: str = "resume.tex"
   ) -> dict:
   ```

3. **Handle errors gracefully**
   ```python
   result = generate_tailored_resume(job, resume)
   if not result['success']:
       log_error(result['message'])
       return error_response()
   ```

4. **Add validation**
   ```python
   if not job_description or len(job_description) < 50:
       return {'success': False, 'message': 'Job description too short'}
   ```

---

## 📋 Checklist for Frontend/Backend Integration

- [ ] Test `main.py` works standalone
- [ ] Create Flask/FastAPI backend
- [ ] Import functions from `main.py`
- [ ] Add API endpoints
- [ ] Test API with Postman/curl
- [ ] Create frontend form
- [ ] Connect frontend to backend
- [ ] Handle file uploads (optional)
- [ ] Add loading states
- [ ] Display match scores
- [ ] Allow resume download
- [ ] Add error handling
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Test end-to-end

---

## 🎓 Learning Path

1. **Understand the structure**
   ```bash
   python main.py  # Choose option 2
   ```

2. **Test API function**
   ```bash
   python main.py  # Choose option 4
   ```

3. **Create simple Flask API**
   ```python
   # Follow API_INTEGRATION_GUIDE.md
   ```

4. **Test with Postman/curl**
   ```bash
   curl -X POST http://localhost:5000/api/generate-resume \
        -H "Content-Type: application/json" \
        -d '{"job_description": "...", "resume_text": "..."}'
   ```

5. **Build frontend**
   ```javascript
   // Use React, Vue, or vanilla JS
   ```

---

## 🆘 Common Issues

### Issue 1: Import Error
```python
# If you get: ModuleNotFoundError: No module named 'sample_data'
# Make sure sample_data.py is in the same directory as main.py
```

### Issue 2: API Returns Error
```python
# Check the error message in result['message']
# Common causes:
# - Missing Gemini API key
# - Invalid input format
# - Template file not found
```

### Issue 3: File Not Found
```python
# Make sure resume_template.tex exists
# Check file paths in resume_generator.py
```

---

## 📞 Support Files

- **API_INTEGRATION_GUIDE.md** - Full integration examples
- **MAIN_PY_GUIDE.md** - Detailed explanation of changes
- **sample_data.py** - Test data repository
- **main.py** - Core API functions

---

**Quick Start:**
```bash
# 1. Test it works
python main.py

# 2. Create your API
# (Use examples from API_INTEGRATION_GUIDE.md)

# 3. Build your frontend
# (Connect to your API endpoints)

# 4. Deploy and launch! 🚀
```

