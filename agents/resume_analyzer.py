"""
resume_analyzer.py
------------------
ONLY resume analysis functionality.
Imports JobAnalyzerAgent - doesn't duplicate anything!

This file contains ONLY the ResumeAgent class and its methods.
Everything else is imported from previous files.
"""

from job_analyzer import JobAnalyzerAgent  # Import the job analyzer!
import json


class ResumeAgent(JobAnalyzerAgent):
    """
    Resume Analyzer Agent
    
    Inherits from JobAnalyzerAgent which inherits from BaseAgent
    
    This means it automatically has:
    - __init__ from BaseAgent
    - analyze_job_description from JobAnalyzerAgent
    
    We ONLY add resume analysis here!
    """
    
    def analyze_resume(self, resume_text: str) -> dict:
        """
        Analyze resume and extract structured information
        
        Enhanced to extract:
        - GitHub profile
        - Portfolio website
        - Extracurricular activities
        
        Args:
            resume_text (str): The resume content
            
        Returns:
            dict: Structured resume data with all fields
        """
        
        print("📄 Analyzing Resume...")
        print("-" * 60)
        
        prompt = f"""You are a resume analyzer. Extract ALL information from this resume.

Resume:
{resume_text}

Extract and return the following in JSON format:
{{
    "name": "Full name if present",
    "contact_info": {{
        "email": "email if present",
        "phone": "phone if present",
        "location": "location if present",
        "linkedin": "LinkedIn URL if present",
        "github": "GitHub profile URL if present",
        "portfolio": "Portfolio or personal website URL if present"
    }},
    "summary": "Professional summary/objective if present",
    "skills": ["list", "all", "skills", "mentioned"],
    "technical_skills": ["specific", "technical", "skills"],
    "soft_skills": ["communication", "leadership", "etc"],
    "experience": [
        {{
            "title": "Job title",
            "company": "Company name",
            "duration": "Time period",
            "responsibilities": ["what", "they", "did"]
        }}
    ],
    "education": [
        {{
            "degree": "Degree name",
            "institution": "School name",
            "year": "Graduation year",
            "details": "Relevant coursework, GPA, etc if mentioned"
        }}
    ],
    "projects": ["List any projects mentioned"],
    "achievements": ["Notable achievements or awards"],
    "certifications": ["Any certifications"],
    "extracurricular_activities": ["Clubs, volunteering, leadership, sports, hobbies if mentioned"]
}}

IMPORTANT: 
- Extract GitHub link if present (github.com/username)
- Extract portfolio/website if present
- Extract ALL extracurricular activities mentioned
- If any field doesn't exist, use null or empty array

Be thorough. Return ONLY the JSON, no other text."""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.replace('```json', '').replace('```', '').strip()
            resume_data = json.loads(response_text)
            
            # Show what we found
            print("✅ Resume analysis complete!")
            print(f"   Name: {resume_data.get('name', 'Not found')}")
            print(f"   Skills: {len(resume_data.get('skills', []))} found")
            print(f"   Experience: {len(resume_data.get('experience', []))} positions")
            print(f"   Education: {len(resume_data.get('education', []))} entries")
            print(f"   Projects: {len(resume_data.get('projects', []))} listed")
            
            # Highlight new fields if found
            contact = resume_data.get('contact_info', {})
            if contact.get('github'):
                print(f"   ✨ GitHub: {contact['github']}")
            if contact.get('portfolio'):
                print(f"   ✨ Portfolio: {contact['portfolio']}")
            
            extracurriculars = resume_data.get('extracurricular_activities', [])
            if extracurriculars:
                print(f"   ✨ Extracurriculars: {len(extracurriculars)} activities")
            
            print()
            
            return resume_data
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise


