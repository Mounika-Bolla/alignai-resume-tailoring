"""
strategy_creator.py
-------------------
ONLY strategy creation functionality.
Imports ResumeAgent - doesn't duplicate anything!

This is the "BRAIN" of the agent - where strategic decisions are made!
"""

from resume_analyzer import ResumeAgent
import json


class StrategyAgent(ResumeAgent):
    """
    Strategy Creator Agent
    
    Inherits from ResumeAgent which has:
    - __init__ from BaseAgent
    - analyze_job_description from JobAnalyzerAgent  
    - analyze_resume from ResumeAgent
    
    We ONLY add strategy creation here!
    
    This is the BRAIN - where intelligent decisions happen!
    """
    
    def create_matching_strategy(self, job_analysis: dict, resume_data: dict) -> dict:
        """
        Create strategic plan for resume tailoring
        
        This is the KEY method - where the agent "thinks"!
        
        What happens here:
        ------------------
        1. Agent compares job requirements vs your background
        2. Identifies what matches strongly
        3. Spots what's missing or weak
        4. Makes strategic decisions about emphasis
        5. Creates a detailed optimization plan
        
        Why this is "agentic":
        ----------------------
        The agent doesn't just format text - it REASONS:
        - "They want Python? You have 4 years - emphasize this!"
        - "They want AWS? You used Azure - mention cloud skills!"
        - "They want leadership? You led a team - highlight this!"
        - "GitHub important? Show your profile prominently!"
        
        This decision-making is what makes it an agent!
        
        Args:
            job_analysis: Structured job requirements
            resume_data: Structured resume information
            
        Returns:
            dict: Strategic plan with specific recommendations
        """
        
        print("🧠 Creating Strategic Matching Plan...")
        print("-" * 60)
        
        # Create a comprehensive prompt for strategic analysis
        prompt = f"""You are an expert resume strategist. Your job is to create a detailed strategy for tailoring a resume to maximize the match with a job posting.

JOB REQUIREMENTS:
{json.dumps(job_analysis, indent=2)}

CANDIDATE'S BACKGROUND:
{json.dumps(resume_data, indent=2)}

Analyze the match and create a strategic plan in JSON format:
{{
    "overall_match_score": "Rate 0-100 how well candidate matches",
    "match_summary": "Brief summary of the match quality",
    
    "strong_matches": [
        {{
            "skill_or_experience": "What matches strongly",
            "evidence": "Where in resume this is shown",
            "strategy": "How to emphasize this"
        }}
    ],
    
    "partial_matches": [
        {{
            "requirement": "What partially matches",
            "candidate_has": "What candidate actually has",
            "strategy": "How to position this positively"
        }}
    ],
    
    "gaps": [
        {{
            "missing": "What's required but missing",
            "severity": "critical/moderate/minor",
            "mitigation": "How to address or downplay this gap"
        }}
    ],
    
    "skills_to_emphasize": [
        {{
            "skill": "Skill name",
            "reason": "Why emphasize",
            "how": "Where and how to highlight"
        }}
    ],
    
    "experience_to_highlight": [
        {{
            "experience": "Which job/project",
            "why": "Why relevant to this position",
            "key_achievements": ["What to emphasize from this role"]
        }}
    ],
    
    "keywords_to_add": ["ATS-friendly keywords to incorporate"],
    
    "structural_recommendations": {{
        "summary_focus": "What to emphasize in summary",
        "skills_section": "How to organize skills",
        "experience_order": "Any reordering needed",
        "what_to_deemphasize": ["What to minimize or remove"]
    }},
    
    "enhanced_elements": {{
        "github_strategy": "How to leverage GitHub profile if present",
        "portfolio_strategy": "How to leverage portfolio if present",
        "extracurriculars_strategy": "Which activities to highlight and why"
    }},
    
    "differentiation_strategy": "How to stand out from other candidates",
    
    "specific_actions": [
        "Concrete action item 1",
        "Concrete action item 2"
    ]
}}

IMPORTANT: 
- Be specific and actionable
- Consider ATS optimization
- Identify transferable skills even if not exact match
- Leverage ALL enhanced fields (GitHub, portfolio, extracurriculars)
- Think strategically about positioning

Return ONLY the JSON, no other text."""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.replace('```json', '').replace('```', '').strip()
            strategy = json.loads(response_text)
            
            # Display strategy summary
            print("✅ Strategy created!")
            print(f"   Overall Match Score: {strategy.get('overall_match_score', 'N/A')}/100")
            print(f"   Strong Matches: {len(strategy.get('strong_matches', []))}")
            print(f"   Partial Matches: {len(strategy.get('partial_matches', []))}")
            print(f"   Gaps Identified: {len(strategy.get('gaps', []))}")
            print(f"   Skills to Emphasize: {len(strategy.get('skills_to_emphasize', []))}")
            print(f"   Keywords to Add: {len(strategy.get('keywords_to_add', []))}")
            print()
            
            return strategy
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
    
    
    def run_complete_analysis(self, job_description: str, resume_text: str) -> dict:
        """
        Run the complete 3-step analysis process
        
        This orchestrates all three tools:
        1. Analyze job (Tool #1)
        2. Analyze resume (Tool #2)
        3. Create strategy (Tool #3)
        
        Returns:
            dict: Complete analysis with all data and strategy
        """
        
        print("\n" + "🤖 "*30)
        print("COMPLETE AGENT ANALYSIS - 3 TOOLS")
        print("🤖 "*30 + "\n")
        
        # Step 1: Analyze Job
        print("="*70)
        print("STEP 1 of 3: Understanding Job Requirements")
        print("="*70)
        job_analysis = self.analyze_job_description(job_description)
        
        # Step 2: Analyze Resume
        print("\n" + "="*70)
        print("STEP 2 of 3: Understanding Your Background")
        print("="*70)
        resume_data = self.analyze_resume(resume_text)
        
        # Step 3: Create Strategy
        print("\n" + "="*70)
        print("STEP 3 of 3: Creating Strategic Plan (THE BRAIN!)")
        print("="*70)
        strategy = self.create_matching_strategy(job_analysis, resume_data)
        
        # Return everything
        return {
            "job_analysis": job_analysis,
            "resume_data": resume_data,
            "strategy": strategy
        }


