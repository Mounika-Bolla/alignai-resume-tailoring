"""
job_analyzer.py
---------------
ONLY job analysis functionality.
Imports BaseAgent - doesn't duplicate it!
"""

from base_agent import BaseAgent  # Import the base!
import json


class JobAnalyzerAgent(BaseAgent):
    """
    Job Analyzer Agent
    
    Inherits from BaseAgent (gets __init__ automatically)
    Adds ONLY job analysis capability
    """
    
    def analyze_job_description(self, job_description: str) -> dict:
        """
        Analyze job description and extract requirements
        
        Returns:
            dict: Job requirements in structured format
        """
        
        print("🔍 Analyzing Job Description...")
        print("-" * 60)
        
        prompt = f"""You are a job requirement analyzer. Analyze this job description.

Job Description:
{job_description}

Extract and return the following in JSON format:
{{
    "required_skills": ["list", "of", "skills"],
    "nice_to_have_skills": ["optional", "skills"],
    "education_required": "degrees or certifications"
    "experience_level": "e.g., 2-3 years",
    "key_responsibilities": ["main", "duties"],
    "important_keywords": ["keywords", "for", "ATS"],
    "company_culture": "brief description of culture if mentioned"
}}

Be thorough. Return ONLY the JSON, no other text."""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.replace('```json', '').replace('```', '').strip()
            job_analysis = json.loads(response_text)
            
            print("✅ Analysis complete!")
            print(f"   Found {len(job_analysis.get('required_skills', []))} required skills")
            print(f"   Experience level: {job_analysis.get('experience_level', 'Not specified')}")
            print(f"   Key responsibilities: {len(job_analysis.get('key_responsibilities', []))}")
            print()
            
            return job_analysis
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise


# Test if this file runs standalone
if __name__ == "__main__":
    print("Testing JobAnalyzerAgent...")
    print()
    
    sample_job = """
   Are you passionate about developing capabilities to protect security and privacy at cloud scale? Are you curious to understand complex systems, their inner workings and how to ensure their compliant operations? We are looking for a Detections Developer who has the right mix of software development experience, machine learning knowhow, and passion for solving complex security-oriented problems. Our team strives to support the business success of our customers by designing and building innovative new solutions to monitor the performance and security of their operations. Your mission will be to design, develop and productize detections capabilities for a broad range of security and privacy compliance. You will engage in the end-to-end process from requirements analysis to development and testing to detections operationalization. We value driven professionals who have passion to learn, enable others and deliver production quality software. 

We offer: 

A world-class team of highly skilled professionals who thrive on new challenges.
Expertise in networking, network and database security, statistical analysis and machine learning, software development and data analytics.
Drive to deliver customer impact while valuing curiosity, commitment, and a mindset to help others.
The resources of a large enterprise and the energy of a start-up.
Exposure to incredibly large-scale network infrastructure and the opportunities for innovation it brings.
A philosophy focuses on personal growth through ongoing training, skills development, and hands on experience.
Responsibilities
Responsibilities

Producing data collection requirements and conducting data quality assessment. 
Conducting various analyses (basic statistics and ML-based ones) on top of network and application logs.
Design and the implementation of monitoring capabilities to track application and network traffic behavior.
Oversee compliance of detections with information security standards and corporate security policies. 
Explore automation methodologies incl. ML/AI-based ones to support investigations and root cause analyses of detections.
We ask for

Bachelor or Master’s Degree in Computer Science, Machine learning or related fields.
1+ years of experience in data analytics, network monitoring, network security or . 
Comfortable with writing non-trivial code in Python, Scala and experience with PySpark. 
Good skills in Java are an advantage.
Background in statistical analysis and ML/AI is an advantage.
Background in distributed systems incl. Spark and automation.
Experience in working in a DevOps model using any of the major cloud providers Azure, AWS, GCP, OCI, is an advantage.
Critical thinking skills and investigative mindset to solve complex problems.
Strong organizational, verbal, and written communication skills.
Strong teamwork and collaboration skills.
    """
    
    try:
        agent = JobAnalyzerAgent()  # Automatically has __init__ from BaseAgent!
        analysis = agent.analyze_job_description(sample_job)
        
        # Show the results in a nice format
        print("\n" + "="*60)
        print("ANALYSIS RESULTS:")
        print("="*60)
        print(json.dumps(analysis, indent=2))
        print("\n✅ Tool #1 is working!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")