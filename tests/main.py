"""
main.py
-------
Main application file - Clean and API-ready

This file provides:
1. Core functions for the resume tailoring pipeline
2. Functions ready to be called by a web API
3. Optional test mode using external sample data

NO hardcoded data here - ready for frontend/backend integration!
"""

from resume_generator import ResumeGeneratorAgent
import json


# ========================================================================
# CORE API-READY FUNCTIONS
# These functions are clean and ready to be called by your web backend
# ========================================================================

def generate_tailored_resume(job_description: str, resume_text: str, 
                             output_filename: str = "tailored_resume.tex") -> dict:
    """
    Main function for generating a tailored resume
    
    This is YOUR MAIN API ENDPOINT function - call this from your backend!
    
    Args:
        job_description (str): The job posting text
        resume_text (str): The candidate's resume text
        output_filename (str): Name for the output .tex file
        
    Returns:
        dict: {
            'success': bool,
            'output_file': str,
            'analysis_file': str,
            'match_score': int,
            'message': str
        }
    """
    try:
        agent = ResumeGeneratorAgent()
        
        output_path = agent.run_complete_pipeline(
            job_description=job_description,
            resume_text=resume_text,
            output_filename=output_filename
        )
        
        # Read the analysis file to get match score
        analysis_file = output_filename.replace('.tex', '_analysis.json')
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)
        
        match_score = analysis.get('strategy', {}).get('overall_match_score', 0)
        
        return {
            'success': True,
            'output_file': output_filename,
            'analysis_file': analysis_file,
            'match_score': match_score,
            'message': f'Resume generated successfully with {match_score}/100 match score'
        }
        
    except Exception as e:
        return {
            'success': False,
            'output_file': None,
            'analysis_file': None,
            'match_score': 0,
            'message': f'Error: {str(e)}'
        }


def analyze_job_and_resume(job_description: str, resume_text: str) -> dict:
    """
    Analyze job and resume WITHOUT generating the full resume
    Useful for quick match score checks
    
    Args:
        job_description (str): The job posting text
        resume_text (str): The candidate's resume text
        
    Returns:
        dict: Complete analysis including job, resume, and strategy
    """
    try:
        agent = ResumeGeneratorAgent()
        
        # Run analysis only (Tools 1-3, not Tool 4)
        analysis = agent.run_complete_analysis(job_description, resume_text)
        
        return {
            'success': True,
            'job_analysis': analysis['job_analysis'],
            'resume_data': analysis['resume_data'],
            'strategy': analysis['strategy'],
            'match_score': analysis['strategy'].get('overall_match_score', 0),
            'message': 'Analysis completed successfully'
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }


def test_individual_tools(job_description: str, resume_text: str):
    """
    Test each tool step-by-step for learning/debugging purposes
    
    Args:
        job_description (str): The job posting text
        resume_text (str): The candidate's resume text
    """
    print("="*70)
    print("INDIVIDUAL TOOL TESTING - LEARNING MODE")
    print("="*70)
    
    agent = ResumeGeneratorAgent()
    
    # Test Tool #1
    print("\n🔍 TOOL #1: Job Analysis")
    print("-"*70)
    job_analysis = agent.analyze_job_description(job_description)
    print(f"✅ Found {len(job_analysis.get('required_skills', []))} required skills")
    
    # Test Tool #2
    print("\n📄 TOOL #2: Resume Analysis")
    print("-"*70)
    resume_data = agent.analyze_resume(resume_text)
    print(f"✅ Extracted {len(resume_data.get('skills', []))} skills from resume")
    
    # Test Tool #3
    print("\n🧠 TOOL #3: Strategy Creation")
    print("-"*70)
    strategy = agent.create_matching_strategy(job_analysis, resume_data)
    print(f"✅ Match Score: {strategy.get('overall_match_score', 'N/A')}/100")
    
    # Test Tool #4
    print("\n✍️  TOOL #4: Resume Generation")
    print("-"*70)
    tailored_resume = agent.generate_tailored_resume(resume_data, strategy, job_analysis)
    print(f"✅ Generated {len(tailored_resume)} characters of LaTeX resume")
    
    print("\n" + "="*70)
    print("✅ ALL INDIVIDUAL TOOLS WORKING!")
    print("="*70)


def test_complete_pipeline(job_description: str, resume_text: str, 
                          output_filename: str = "test_resume.tex"):
    """
    Test the complete pipeline with provided data
    
    Args:
        job_description (str): The job posting text
        resume_text (str): The candidate's resume text
        output_filename (str): Name for output file
    """
    try:
        print("Creating Complete Resume Generator Agent...")
        print("=" * 70)
        agent = ResumeGeneratorAgent()
        
        # Verify it has ALL 4 tools
        print("\n✅ Verifying Agent Capabilities:")
        print("   Tool #1 (Job Analysis):", hasattr(agent, 'analyze_job_description'))
        print("   Tool #2 (Resume Analysis):", hasattr(agent, 'analyze_resume'))
        print("   Tool #3 (Strategy Creation):", hasattr(agent, 'create_matching_strategy'))
        print("   Tool #4 (Resume Generation):", hasattr(agent, 'generate_tailored_resume'))
        print("=" * 70)
        print()
        
        # Run the COMPLETE pipeline (all 4 tools in one call!)
        print("\n🚀 Running Complete Pipeline (All 4 Tools)...\n")
        
        output_file = agent.run_complete_pipeline(
            job_description=job_description,
            resume_text=resume_text,
            output_filename=output_filename
        )
        
        print("\n" + "="*70)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"\n📄 Your tailored resume: {output_filename}")
        print(f"📊 Analysis details: {output_filename.replace('.tex', '_analysis.json')}")
        print(f"\n💡 Next Steps:")
        print(f"   1. Upload {output_filename} to Overleaf")
        print(f"   2. Review the generated resume")
        print(f"   3. Make any final adjustments")
        print(f"   4. Download PDF and apply!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


# ========================================================================
# TEST MODE - Only runs when file is executed directly
# In production, your API will call the functions above directly
# ========================================================================

if __name__ == "__main__":
    # Import sample data only for testing
    from sample_data import SAMPLE_JOB_DESCRIPTION, SAMPLE_RESUME, MINIMAL_JOB, MINIMAL_RESUME
    
    print("\n" + "🎯 "*30)
    print("RESUME TAILORING SYSTEM - TEST MODE")
    print("🎯 "*30 + "\n")
    
    print("Choose a test mode:")
    print("1. Test complete pipeline (full sample data)")
    print("2. Test individual tools (minimal sample data)")
    print("3. Test quick analysis (no resume generation)")
    print("4. Test API function (recommended for backend dev)\n")
    
    choice = input("Enter your choice (1/2/3/4) or press Enter for default [1]: ").strip()
    
    if choice == "2":
        print("\n📖 Testing Individual Tools with Minimal Data...")
        test_individual_tools(MINIMAL_JOB, MINIMAL_RESUME)
        
    elif choice == "3":
        print("\n⚡ Quick Analysis Test...")
        result = analyze_job_and_resume(SAMPLE_JOB_DESCRIPTION, SAMPLE_RESUME)
        if result['success']:
            print(f"\n✅ Match Score: {result['match_score']}/100")
            print(f"📊 Analysis completed successfully")
        else:
            print(f"\n❌ {result['message']}")
            
    elif choice == "4":
        print("\n🔌 Testing Main API Function...")
        result = generate_tailored_resume(
            job_description=SAMPLE_JOB_DESCRIPTION,
            resume_text=SAMPLE_RESUME,
            output_filename="api_test_resume.tex"
        )
        print(f"\n{'✅' if result['success'] else '❌'} {result['message']}")
        if result['success']:
            print(f"📄 Output: {result['output_file']}")
            print(f"📊 Match Score: {result['match_score']}/100")
            
    else:
        # Default: complete pipeline with full sample data
        print("\n🚀 Running Complete Pipeline Test...")
        test_complete_pipeline(SAMPLE_JOB_DESCRIPTION, SAMPLE_RESUME, "test_resume.tex")