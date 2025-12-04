# 🤖 AI Agents - AlignAI

This folder contains all AI agents and tools used for resume analysis and generation.

---

## 📁 Files Overview

### **Core Agent**
- **`resume_generator.py`** - Main agent that orchestrates the complete resume alignment process

### **Tool Agents**
- **`base_agent.py`** - Base class for all agents with common functionality
- **`job_analyzer.py`** - Analyzes job descriptions to extract requirements and keywords
- **`resume_analyzer.py`** - Analyzes resumes to extract skills, experience, and content
- **`strategy_creator.py`** - Creates tailoring strategies for resume optimization

---

## 🔄 How They Work Together

```
User Input (Job Description + Resume)
         ↓
   [resume_generator.py]
         ↓
    ┌────┴────┐
    ↓         ↓
[job_analyzer] [resume_analyzer]
    ↓         ↓
    └────┬────┘
         ↓
  [strategy_creator]
         ↓
  Optimized Resume
```

---

## 📝 Individual Agent Details

### 1. **resume_generator.py** (Main Orchestrator)

**Purpose:** Coordinates all agents to create tailored resumes

**Key Methods:**
- `generate_tailored_resume()` - Complete pipeline
- `run_complete_pipeline()` - Step-by-step execution

**Input:**
- Job description (text)
- Resume content (text)

**Output:**
- Analysis results
- Tailoring strategy
- Generated resume

---

### 2. **base_agent.py** (Base Class)

**Purpose:** Provides common functionality for all agents

**Features:**
- Tool initialization
- Error handling
- Logging
- Common utilities

**Usage:**
```python
from base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        # Your initialization
```

---

### 3. **job_analyzer.py** (Job Analysis Tool)

**Purpose:** Extract requirements from job descriptions

**What it extracts:**
- Required skills
- Preferred qualifications
- Keywords and phrases
- Experience requirements
- Technical requirements
- Soft skills needed

**Example Output:**
```json
{
  "required_skills": ["Python", "SQL", "React"],
  "preferred_skills": ["AWS", "Docker"],
  "experience_years": "3-5",
  "keywords": ["agile", "team player", "problem solving"]
}
```

---

### 4. **resume_analyzer.py** (Resume Analysis Tool)

**Purpose:** Parse and analyze resume content

**What it extracts:**
- Current skills
- Work experience
- Education
- Projects
- Certifications
- Keywords present
- Missing keywords

**Example Output:**
```json
{
  "skills": ["Python", "JavaScript", "SQL"],
  "experience": [
    {
      "title": "Software Engineer",
      "company": "Tech Corp",
      "duration": "2 years",
      "responsibilities": [...]
    }
  ],
  "education": [...]
}
```

---

### 5. **strategy_creator.py** (Strategy Generation Tool)

**Purpose:** Create actionable tailoring strategies

**What it generates:**
- Skills to emphasize
- Keywords to add
- Sections to reorder
- Content to expand
- Content to minimize
- ATS optimization tips

**Example Output:**
```json
{
  "add_keywords": ["microservices", "CI/CD"],
  "emphasize_skills": ["Python", "API Development"],
  "reorder_sections": ["Move projects above education"],
  "expand_content": ["Add more details about AWS experience"],
  "ats_score": 85
}
```

---

## 🚀 Usage

### **Option 1: Use the Main Generator**

```python
from agents.resume_generator import ResumeGeneratorAgent

agent = ResumeGeneratorAgent()
result = agent.generate_tailored_resume(
    job_description="...",
    resume_text="..."
)
```

### **Option 2: Use Individual Agents**

```python
from agents.job_analyzer import JobAnalyzer
from agents.resume_analyzer import ResumeAnalyzer
from agents.strategy_creator import StrategyCreator

# Analyze job
job_agent = JobAnalyzer()
job_analysis = job_agent.analyze(job_description)

# Analyze resume
resume_agent = ResumeAnalyzer()
resume_analysis = resume_agent.analyze(resume_text)

# Create strategy
strategy_agent = StrategyCreator()
strategy = strategy_agent.create_strategy(
    job_analysis,
    resume_analysis
)
```

---

## 🔧 Configuration

### **Environment Variables**

Create a `.env` file in the project root:

```env
# OpenAI API (if using GPT models)
OPENAI_API_KEY=your_key_here

# Anthropic API (if using Claude models)
ANTHROPIC_API_KEY=your_key_here

# Model Selection
DEFAULT_MODEL=gpt-4
FALLBACK_MODEL=gpt-3.5-turbo
```

### **Agent Configuration**

Each agent can be configured with:
- Model selection (GPT-4, Claude, etc.)
- Temperature (creativity level)
- Max tokens
- Timeout settings

---

## 🧪 Testing

Test the agents using the test files:

```bash
cd tests
python main.py
```

This will run through:
1. Job analysis
2. Resume analysis
3. Strategy creation
4. Resume generation

Sample outputs will be saved in `tests/sample_outputs/`

---

## 📊 Agent Dependencies

```
resume_generator.py
    ├── base_agent.py
    ├── job_analyzer.py
    ├── resume_analyzer.py
    └── strategy_creator.py
```

All tools inherit from `BaseAgent` for consistency.

---

## 🔍 Output Formats

### **JSON Output**
All agents can output results in JSON format for easy integration:
```json
{
  "success": true,
  "data": {...},
  "metadata": {
    "timestamp": "...",
    "agent": "job_analyzer",
    "version": "1.0"
  }
}
```

### **LaTeX Output**
The resume generator can create LaTeX templates:
- Professional formatting
- ATS-friendly design
- Customizable sections

---

## 🐛 Troubleshooting

### **"Module not found" errors**

Make sure you're running from the project root:
```bash
cd C:\Users\monib\Desktop\resumetailoring
python -c "from agents.resume_generator import ResumeGeneratorAgent"
```

### **API Key errors**

Check your `.env` file and ensure API keys are set:
```bash
# Windows
$env:OPENAI_API_KEY="your_key"

# Or add to .env file
```

### **Import errors**

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## 📚 Further Reading

- **LangChain Documentation:** https://python.langchain.com/
- **OpenAI API:** https://platform.openai.com/docs
- **Anthropic Claude:** https://www.anthropic.com/

---

## 🔄 Adding New Agents

To create a new agent:

1. **Create a new file:** `agents/my_agent.py`

2. **Inherit from BaseAgent:**
```python
from base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "MyAgent"
    
    def process(self, input_data):
        # Your logic here
        return result
```

3. **Integrate with main generator:**
```python
# In resume_generator.py
from my_agent import MyAgent

class ResumeGeneratorAgent:
    def __init__(self):
        self.my_agent = MyAgent()
```

---

## 🎯 Best Practices

1. **Always validate inputs** before processing
2. **Use try-except blocks** for API calls
3. **Log important events** for debugging
4. **Return consistent formats** (JSON recommended)
5. **Include metadata** in outputs (timestamp, version, etc.)
6. **Test with sample data** before production use
7. **Handle rate limits** for API calls

---

## 📈 Performance Tips

- **Cache job analyses** for repeated uses
- **Use batch processing** when analyzing multiple resumes
- **Implement retry logic** for API failures
- **Set appropriate timeouts** to avoid hanging
- **Monitor token usage** to control costs

---

**Built with ❤️ for better resumes and better matches**

