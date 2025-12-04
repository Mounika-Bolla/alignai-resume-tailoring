# 🧪 Tests - AlignAI

This folder contains test files, sample data, and test outputs.

---

## 📁 Folder Structure

```
tests/
├── main.py              # Main test script
├── sample_data.py       # Sample job descriptions and resumes
├── sample_outputs/      # JSON test outputs
│   ├── job_analysis_final.json
│   ├── resume_data_final.json
│   ├── complete_analysis.json
│   └── *.json          # Other test outputs
└── templates/           # LaTeX resume templates
    ├── resume_template.tex
    └── *.tex           # Generated resume templates
```

---

## 🚀 Running Tests

### **Run All Tests**

```bash
cd tests
python main.py
```

### **Interactive Menu**

The test script provides an interactive menu:

```
AlignAI Agent Testing
=====================
1. Test Complete Pipeline
2. Test Individual Tools
3. Test with Custom Data
4. Exit
```

---

## 📝 Test Files

### **1. main.py**

**Purpose:** Main test runner for all agents

**What it tests:**
- Complete pipeline (job → resume → strategy → generation)
- Individual agent functionality
- Error handling
- Output formats

**Usage:**
```bash
python main.py
```

**Options:**
- Test with sample data
- Test with custom input
- Test individual components
- Generate test outputs

---

### **2. sample_data.py**

**Purpose:** Contains sample job descriptions and resumes for testing

**What's included:**
- `SAMPLE_JOB_DESCRIPTION` - Full job posting
- `SAMPLE_RESUME` - Complete resume text
- `MINIMAL_JOB` - Minimal job description for quick tests
- `MINIMAL_RESUME` - Minimal resume for quick tests

**Usage:**
```python
from sample_data import SAMPLE_JOB_DESCRIPTION, SAMPLE_RESUME

result = agent.analyze(SAMPLE_JOB_DESCRIPTION, SAMPLE_RESUME)
```

---

## 📊 Sample Outputs

### **sample_outputs/** folder

Contains JSON outputs from test runs:

#### **job_analysis_final.json**
Output from job analyzer:
```json
{
  "required_skills": [...],
  "preferred_qualifications": [...],
  "keywords": [...],
  "experience_level": "..."
}
```

#### **resume_data_final.json**
Output from resume analyzer:
```json
{
  "skills": [...],
  "experience": [...],
  "education": [...],
  "projects": [...]
}
```

#### **complete_analysis.json**
Complete pipeline output:
```json
{
  "job_analysis": {...},
  "resume_analysis": {...},
  "strategy": {...},
  "match_score": 85
}
```

---

## 📄 Templates

### **templates/** folder

Contains LaTeX resume templates:

#### **resume_template.tex**
Base template for generating resumes:
- Professional formatting
- ATS-friendly design
- Customizable sections
- Multiple layouts

**Compile to PDF:**
```bash
pdflatex resume_template.tex
```

---

## 🧪 Writing New Tests

### **Add to main.py**

```python
def test_my_feature():
    """Test description"""
    print("\n📝 Testing My Feature...")
    
    # Your test code here
    agent = MyAgent()
    result = agent.process(test_data)
    
    # Verify results
    assert result['success'] == True
    print("✅ Test passed!")

# Add to menu
if __name__ == "__main__":
    # In the menu section
    print("5. Test My Feature")
    # ...
```

### **Add Sample Data**

```python
# In sample_data.py
MY_TEST_DATA = """
Your test data here...
"""
```

---

## 📊 Test Coverage

Current tests cover:

### **✅ Functional Tests**
- Job description parsing
- Resume parsing
- Strategy generation
- Resume generation
- Complete pipeline

### **✅ Integration Tests**
- Agent communication
- Data flow between agents
- Error propagation

### **✅ Data Tests**
- Sample job descriptions
- Sample resumes
- Edge cases (minimal data)

### **⏳ TODO: Add More Tests**
- Unit tests for individual functions
- Performance tests
- Load tests
- API endpoint tests
- Frontend tests

---

## 🔍 Debugging Tests

### **Enable Verbose Output**

```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **Save Test Outputs**

All JSON outputs are automatically saved to `sample_outputs/`

### **Check Logs**

```python
# Agents log to console
print(f"Debug: {variable}")
```

---

## 📈 Test Results

### **Expected Behavior**

1. **Job Analysis:**
   - Extracts 10-20 keywords
   - Identifies required vs. preferred skills
   - Returns structured JSON

2. **Resume Analysis:**
   - Extracts all sections correctly
   - Identifies skills accurately
   - Calculates experience years

3. **Strategy Creation:**
   - Provides actionable recommendations
   - Prioritizes changes
   - Calculates match score (0-100)

4. **Resume Generation:**
   - Creates ATS-friendly format
   - Includes all required sections
   - Uses proper LaTeX syntax

---

## 🐛 Common Test Issues

### **Import Errors**

Make sure you're in the tests directory:
```bash
cd tests
python main.py
```

Or run from project root:
```bash
python tests/main.py
```

### **Missing Dependencies**

Install all requirements:
```bash
pip install -r requirements.txt
```

### **API Key Errors**

Set your API keys:
```bash
# In .env file
OPENAI_API_KEY=your_key_here
```

### **File Not Found**

Check paths are relative to project root or tests folder.

---

## 📊 Performance Benchmarks

Typical execution times (approximate):

| Test | Time | Tokens Used |
|------|------|-------------|
| Job Analysis | 2-5s | 500-1000 |
| Resume Analysis | 3-7s | 1000-2000 |
| Strategy Creation | 5-10s | 1500-2500 |
| Complete Pipeline | 15-30s | 3000-5000 |

---

## 🎯 Test Best Practices

1. **Always test with sample data first** before using real data
2. **Save outputs** for comparison and debugging
3. **Test edge cases** (empty inputs, minimal data, etc.)
4. **Verify JSON structure** matches expected schema
5. **Check for errors** in console output
6. **Compare results** across different test runs
7. **Document unexpected behavior**

---

## 🔄 Continuous Testing

### **Before Each Commit**

```bash
# Run tests
python tests/main.py

# Check outputs
ls tests/sample_outputs/

# Verify no errors
echo $?  # Should be 0
```

### **Automated Testing** (TODO)

Set up:
- GitHub Actions for CI/CD
- Automated test runs on push
- Coverage reports
- Performance monitoring

---

## 📚 Related Files

- `../agents/README.md` - Agent documentation
- `../README.md` - Project overview
- `../docs/` - Detailed guides

---

## 🎓 Learning Resources

- **Python Testing:** https://docs.python.org/3/library/unittest.html
- **pytest:** https://docs.pytest.org/
- **Test-Driven Development:** https://testdriven.io/

---

## ✅ Test Checklist

Before deploying:

- [ ] All tests pass
- [ ] No console errors
- [ ] Outputs saved correctly
- [ ] Performance is acceptable
- [ ] Edge cases covered
- [ ] Documentation updated

---

**Happy Testing! 🧪**

