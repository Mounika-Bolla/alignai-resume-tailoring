"""
RAG-Powered Resume Agent
------------------------
Combines traditional resume generation with RAG capabilities
Uses Google Gemini for intelligent, context-aware resume tailoring

This agent:
- Ingests resume + JD into vector database
- Retrieves relevant context for queries
- Generates tailored content with RAG
- Learns from user feedback
- Provides intelligent suggestions
"""

from typing import Dict, List, Any, Optional
from rag_engine import get_rag_engine
from resume_generator import ResumeGeneratorAgent


class RAGResumeAgent:
    """
    RAG-Enhanced Resume Agent
    
    Combines:
    - Traditional resume generation (LaTeX)
    - RAG-powered intelligent tailoring
    - Continuous learning from feedback
    - Context-aware suggestions
    """
    
    def __init__(self):
        """Initialize RAG agent"""
        self.rag_engine = get_rag_engine()
        
        # Try to load traditional agent (optional - for LaTeX generation)
        try:
            self.traditional_agent = ResumeGeneratorAgent()
            print("✅ Traditional Agent loaded")
        except Exception as e:
            print(f"⚠️ Traditional Agent not available: {e}")
            self.traditional_agent = None
        
        print("✅ RAG Resume Agent initialized")
    
    
    def analyze_and_ingest(self, resume_text: str, job_description: str,
                          user_id: str) -> Dict[str, Any]:
        """
        Analyze documents and ingest into RAG system
        
        Args:
            resume_text: Resume content
            job_description: Job description
            user_id: User identifier
            
        Returns:
            Combined analysis + ingestion result
        """
        # Traditional analysis (if available)
        resume_analysis = None
        job_analysis = None
        if self.traditional_agent:
            try:
                resume_analysis = self.traditional_agent.analyze_resume(resume_text)
                job_analysis = self.traditional_agent.analyze_job_description(job_description) if job_description else None
            except Exception as e:
                print(f"⚠️ Traditional analysis failed: {e}")
        
        # Ingest into RAG system
        rag_result = self.rag_engine.ingest_documents(
            resume_text=resume_text,
            job_description=job_description,
            user_id=user_id
        )
        
        # Get AI suggestions
        suggestions = self.rag_engine.get_suggestions(resume_text, job_description)
        
        return {
            "resume_analysis": resume_analysis,
            "job_analysis": job_analysis,
            "rag_ingestion": rag_result,
            "ai_suggestions": suggestions,
            "status": "ready_for_tailoring"
        }
    
    
    def tailor_with_instruction(self, instruction: str, user_id: str) -> Dict[str, Any]:
        """
        Tailor resume based on user instruction using RAG
        
        Examples:
            - "Emphasize my Python and machine learning experience"
            - "Add quantifiable metrics to all achievements"
            - "Rewrite experience section to match data scientist role"
        
        Args:
            instruction: Natural language instruction
            user_id: User identifier
            
        Returns:
            Tailored content with context
        """
        result = self.rag_engine.generate_tailored_content(
            instruction=instruction,
            user_id=user_id
        )
        
        return result
    
    
    def generate_complete_resume(self, resume_data: dict, 
                                job_description: str,
                                user_id: str,
                                custom_instructions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate complete tailored resume using RAG + traditional methods
        
        Args:
            resume_data: Structured resume data
            job_description: Target job description
            user_id: User identifier
            custom_instructions: Optional list of tailoring instructions
            
        Returns:
            Complete tailored resume in multiple formats
        """
        # Run traditional pipeline first (if available)
        if not self.traditional_agent:
            return {
                "error": "Traditional agent not available. LaTeX generation requires resume_template.tex",
                "status": "use_rag_only"
            }
        
        job_analysis = self.traditional_agent.analyze_job_description(job_description)
        strategy = self.traditional_agent.create_tailoring_strategy(resume_data, job_analysis)
        
        # Apply custom RAG-based modifications if provided
        if custom_instructions:
            rag_modifications = []
            for instruction in custom_instructions:
                mod = self.rag_engine.generate_tailored_content(
                    instruction=instruction,
                    user_id=user_id
                )
                rag_modifications.append(mod)
        else:
            rag_modifications = []
        
        # Generate LaTeX resume
        latex_resume = self.traditional_agent.generate_tailored_resume(
            resume_data=resume_data,
            strategy=strategy,
            job_analysis=job_analysis
        )
        
        return {
            "latex_resume": latex_resume,
            "strategy": strategy,
            "job_analysis": job_analysis,
            "rag_modifications": rag_modifications,
            "status": "generated"
        }
    
    
    def interactive_refinement(self, user_id: str, feedback: str,
                             rating: int, previous_instruction: str,
                             previous_content: str) -> Dict[str, Any]:
        """
        Learn from user feedback and refine content
        
        Args:
            user_id: User identifier
            feedback: User's feedback text
            rating: Rating 1-5
            previous_instruction: The instruction that was given
            previous_content: Content that was generated
            
        Returns:
            Learning status + refined content
        """
        # Store feedback for learning
        learn_result = self.rag_engine.learn_from_feedback(
            user_id=user_id,
            instruction=previous_instruction,
            generated_content=previous_content,
            feedback=feedback,
            rating=rating
        )
        
        # Generate refined version
        refined_instruction = f"{previous_instruction}\n\nUser Feedback: {feedback}\n\nPlease improve based on this feedback."
        refined_content = self.rag_engine.generate_tailored_content(
            instruction=refined_instruction,
            user_id=user_id
        )
        
        return {
            "learning_status": learn_result,
            "refined_content": refined_content,
            "improvement_applied": True
        }
    
    
    def get_improvement_suggestions(self, resume_text: str, 
                                   job_description: str) -> List[str]:
        """
        Get AI-powered improvement suggestions
        
        Args:
            resume_text: Current resume
            job_description: Target job
            
        Returns:
            List of actionable suggestions
        """
        return self.rag_engine.get_suggestions(resume_text, job_description)
    
    
    def chat(self, message: str, user_id: str) -> str:
        """
        Chat interface for resume tailoring
        
        Args:
            message: User message/query
            user_id: User identifier
            
        Returns:
            AI response
        """
        result = self.rag_engine.generate_tailored_content(
            instruction=message,
            user_id=user_id
        )
        
        if result["success"]:
            return result["tailored_content"]
        else:
            return f"Error: {result.get('error', 'Unknown error')}"


# Create singleton instance
_rag_agent = None

def get_rag_agent() -> RAGResumeAgent:
    """Get or create RAG agent singleton"""
    global _rag_agent
    if _rag_agent is None:
        try:
            _rag_agent = RAGResumeAgent()
            print("✅ RAG Agent initialized successfully")
        except Exception as e:
            print(f"⚠️ RAG Agent initialization failed: {e}")
            print(f"⚠️ Error details: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            print("💡 Make sure GEMINI_API_KEY is set in .env file")
            return None
    return _rag_agent

