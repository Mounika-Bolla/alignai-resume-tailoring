"""
resume_generator.py
-------------------
ONLY resume generation functionality.
Imports StrategyAgent and reads LaTeX template from file.

This is Tool #4 - Generates tailored resumes in LaTeX format!
"""

from strategy_creator import StrategyAgent
import json
import os


class ResumeGeneratorAgent(StrategyAgent):
    """
    Resume Generator Agent
    
    Inherits everything from previous agents.
    ONLY adds resume generation capability.
    
    This is the EXECUTOR - generates the final output!
    """
    
    def __init__(self):
        """Initialize and load LaTeX template"""
        super().__init__()
        
        # Load LaTeX template from file
        template_path = os.path.join(os.path.dirname(__file__), 'resume_template.tex')
        with open(template_path, 'r') as f:
            self.latex_template = f.read()
        
        print("📄 LaTeX template loaded successfully!\n")
    
    
    def generate_tailored_resume(self, resume_data: dict, strategy: dict, 
                                  job_analysis: dict) -> str:
        """
        Generate tailored resume in LaTeX format following the strategy
        
        Process:
        --------
        1. Reads original resume data
        2. Follows strategic plan from Tool #3
        3. Generates LaTeX content
        4. Inserts into template
        5. Returns complete .tex file
        
        The AI generates ONLY the content part, we handle the template!
        
        Args:
            resume_data: Structured resume from Tool #2
            strategy: Strategic plan from Tool #3
            job_analysis: Job requirements from Tool #1
            
        Returns:
            str: Complete LaTeX resume code ready for Overleaf
        """
        
        print("✍️  Generating Tailored Resume in LaTeX Format...")
        print("-" * 60)
        
        # Create prompt for content generation
        prompt = f"""You are an expert resume writer. Generate tailored resume CONTENT in LaTeX format.

ORIGINAL RESUME DATA:
{json.dumps(resume_data, indent=2)}

JOB REQUIREMENTS:
{json.dumps(job_analysis, indent=2)}

STRATEGIC PLAN (MUST FOLLOW):
{json.dumps(strategy, indent=2)}

Generate ONLY the resume content sections in LaTeX format. Use these LaTeX commands:

HEADER FORMAT:
\\begin{{center}}
    {{\\Huge \\scshape [NAME]}} \\\\ \\vspace{{1pt}}
    \\small \\raisebox{{-0.1\\height}}\\faPhone\\ [PHONE] ~ 
    \\href{{mailto:[EMAIL]}}{{\\raisebox{{-0.2\\height}}\\faEnvelope\\ [EMAIL]}} ~ 
    \\href{{[LINKEDIN]}}{{\\raisebox{{-0.2\\height}}\\faLinkedin\\ LinkedIn}} ~
    \\href{{[GITHUB]}}{{\\raisebox{{-0.2\\height}}\\faGithub\\ GitHub}}
    \\vspace{{-8pt}}
\\end{{center}}

SUMMARY SECTION:
\\section{{Summary}}
[Write strategic summary emphasizing what strategy recommends]

EDUCATION SECTION:
\\section{{Education}}
  \\resumeSubHeadingListStart
    \\resumeSubheading
      {{[Degree]}}{{[Location]}}
      {{[Program Details]}}{{[Dates]}}
  \\resumeSubHeadingListEnd
\\vspace{{-12pt}}

EXPERIENCE SECTION:
\\section{{Professional Experience}}
  \\resumeSubHeadingListStart
    \\resumeSubheading
      {{[Job Title]}}{{[Dates]}}
      {{[Company]}}{{[Location]}}
      \\resumeItemListStart
        \\resumeItem{{[Bullet point emphasizing relevant skills]}}
        \\resumeItem{{[Bullet point with keywords from strategy]}}
      \\resumeItemListEnd
  \\resumeSubHeadingListEnd
\\vspace{{-16pt}}

PROJECTS SECTION:
\\section{{Key Projects}}
    \\vspace{{-5pt}}
    \\resumeSubHeadingListStart
      \\resumeProjectHeading
          {{\\textbf{{[Project Name]}} $|$ \\emph{{[Technologies]}}}},{{[Year]}}
          \\resumeItemListStart
            \\resumeItem{{[Achievement]}}
          \\resumeItemListEnd
          \\vspace{{-13pt}}
    \\resumeSubHeadingListEnd

SKILLS SECTION:
\\section{{Technical Skills}}
 \\begin{{itemize}}[leftmargin=0.15in, label={{}}]
    \\small{{\\item{{
     \\textbf{{[Category]:}} [Skills list] \\\\
    }}}}
 \\end{{itemize}}
\\vspace{{-16pt}}

CRITICAL INSTRUCTIONS:
1. FOLLOW THE STRATEGY EXACTLY - emphasize what it says to emphasize
2. INCORPORATE all keywords from strategy naturally
3. If GitHub/Portfolio present in contact_info, include them in header
4. If extracurriculars exist and strategy recommends, add them as section
5. ORDER sections per strategy recommendations
6. Make summary compelling and targeted to the job
7. Quantify achievements where possible
8. Use strong action verbs
9. Ensure ATS-friendly (keywords, formatting)
10. Keep LaTeX syntax PERFECT - no syntax errors

Generate the COMPLETE resume content starting with the header and ending with the last section.
Do NOT include \\documentclass or \\begin{{document}} - only the content sections.
"""

        try:
            # Generate content using Gemini
            response = self.model.generate_content(prompt)
            latex_content = response.text
            
            # Clean up response (remove markdown if present)
            latex_content = latex_content.replace('```latex', '').replace('```', '').strip()
            
            # Insert content into template
            final_resume = self.latex_template.replace('{{CONTENT}}', latex_content)
            
            print("✅ Resume generated successfully!")
            print(f"   Length: {len(final_resume)} characters")
            print(f"   Sections: Header, Summary, Education, Experience, Projects, Skills")
            print()
            
            return final_resume
            
        except Exception as e:
            print(f"❌ Error generating resume: {e}")
            raise
    
    
    def run_complete_pipeline(self, job_description: str, resume_text: str, 
                               output_filename: str = "tailored_resume.tex") -> str:
        """
        Run the COMPLETE agent pipeline - all 4 tools!
        
        This is the full workflow:
        1. Analyze job (Tool #1)
        2. Analyze resume (Tool #2)
        3. Create strategy (Tool #3)
        4. Generate tailored resume (Tool #4)
        5. Save to .tex file
        
        Args:
            job_description: The job posting text
            resume_text: Your current resume text
            output_filename: Name for output .tex file
            
        Returns:
            str: Path to generated .tex file
        """
        
        print("\n" + "🚀 "*30)
        print("COMPLETE RESUME TAILORING PIPELINE")
        print("🚀 "*30 + "\n")
        
        # Run Tools 1-3 (inherited method)
        print("="*70)
        print("RUNNING TOOLS 1-3: Analysis & Strategy")
        print("="*70)
        analysis = self.run_complete_analysis(job_description, resume_text)
        
        # Extract results
        job_analysis = analysis['job_analysis']
        resume_data = analysis['resume_data']
        strategy = analysis['strategy']
        
        # Tool #4: Generate resume
        print("\n" + "="*70)
        print("TOOL 4: Generating Tailored Resume")
        print("="*70)
        tailored_resume = self.generate_tailored_resume(
            resume_data, 
            strategy, 
            job_analysis
        )
        
        # Save to file
        output_path = os.path.join(os.path.dirname(__file__), output_filename)
        with open(output_path, 'w') as f:
            f.write(tailored_resume)
        
        print("\n" + "="*70)
        print("✅ COMPLETE PIPELINE FINISHED!")
        print("="*70)
        print(f"\n📄 Tailored resume saved to: {output_filename}")
        print(f"📊 Match score: {strategy.get('overall_match_score', 'N/A')}/100")
        print(f"\n💡 Next steps:")
        print(f"   1. Open {output_filename} in Overleaf")
        print(f"   2. Review and make any manual edits")
        print(f"   3. Download PDF")
        print(f"   4. Apply to the job!")
        
        # Also save analysis for reference
        analysis_file = output_filename.replace('.tex', '_analysis.json')
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n📊 Full analysis saved to: {analysis_file}")
        
        return output_path


