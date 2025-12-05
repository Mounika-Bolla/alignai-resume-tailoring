"""
RAG Engine for AlignAI
-----------------------
Retrieval-Augmented Generation system using:
- Google Gemini (Free LLM)
- ChromaDB (Vector Database)
- Sentence Transformers (Embeddings)
- LangChain (Orchestration)

This engine learns from resumes and job descriptions to provide
intelligent, context-aware resume tailoring suggestions.
"""

import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import pickle
from dotenv import load_dotenv

load_dotenv()


class RAGEngine:
    """
    RAG (Retrieval-Augmented Generation) Engine for Resume Tailoring
    
    Features:
    - Document ingestion and chunking
    - Semantic search with vector embeddings
    - Context-aware generation using Gemini
    - Continuous learning from user feedback
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize RAG engine with Google Gemini"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key or self.api_key == 'your-gemini-api-key-here':
            raise ValueError(
                "❌ ERROR: No valid API key found!\n"
                "Please add your Gemini API key to the .env file\n"
                "Get free key from: https://makersuite.google.com/app/apikey"
            )
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize embeddings model (free)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.api_key
        )
        
        # Initialize LLM (Gemini 2.5 Flash - Same as base_agent)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Vector store (FAISS)
        self.vector_store = None
        self.vector_store_path = "./vector_stores"
        
        # Create vector store directory
        os.makedirs(self.vector_store_path, exist_ok=True)
        
        print("✅ RAG Engine initialized with Google Gemini + FAISS")
    
    
    def ingest_documents(self, resume_text: str, job_description: str, 
                        user_id: str) -> Dict[str, Any]:
        """
        Ingest resume and job description into vector database
        
        Args:
            resume_text: Full resume text
            job_description: Job description text (optional)
            user_id: User identifier for personalization
            
        Returns:
            Dict with ingestion status and metadata
        """
        try:
            # Create documents list - always include resume
            documents = [
                Document(
                    page_content=resume_text,
                    metadata={
                        "source": "resume",
                        "user_id": user_id,
                        "type": "resume"
                    }
                )
            ]
            
            # Only add JD if it's meaningful (more than 50 chars)
            if job_description and len(job_description.strip()) > 50:
                documents.append(
                    Document(
                        page_content=job_description,
                        metadata={
                            "source": "job_description",
                            "user_id": user_id,
                            "type": "jd"
                        }
                    )
                )
                has_jd = True
            else:
                has_jd = False
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Create vector store with FAISS
            self.vector_store = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings
            )
            
            # Save to disk
            store_path = os.path.join(self.vector_store_path, f"user_{user_id}")
            self.vector_store.save_local(store_path)
            
            return {
                "success": True,
                "chunks_created": len(chunks),
                "has_job_description": has_jd,
                "vector_store_path": store_path,
                "message": f"Resume ingested successfully! {'Job description also added.' if has_jd else 'Add a job description for better tailoring.'}"
            }
            
        except Exception as e:
            print(f"❌ Ingestion error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to ingest documents. Check GEMINI_API_KEY."
            }
    
    
    def retrieve_context(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve relevant context from vector store
        
        Args:
            query: User query or instruction
            k: Number of relevant chunks to retrieve
            
        Returns:
            List of relevant document chunks
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call ingest_documents first.")
        
        # Semantic search
        relevant_docs = self.vector_store.similarity_search(query, k=k)
        return relevant_docs
    
    
    def generate_tailored_content(self, instruction: str, 
                                 user_id: str,
                                 context_override: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate tailored resume content using RAG
        
        Args:
            instruction: User instruction (e.g., "emphasize Python skills")
            user_id: User identifier
            context_override: Optional manual context override
            
        Returns:
            Dict with generated content and metadata
        """
        try:
            # Load user's vector store from disk if not in memory
            if not self.vector_store:
                store_path = os.path.join(self.vector_store_path, f"user_{user_id}")
                if os.path.exists(store_path):
                    self.vector_store = FAISS.load_local(
                        store_path,
                        self.embeddings,
                        allow_dangerous_deserialization=True
                    )
                else:
                    return {
                        "success": False,
                        "error": "Vector store not found. Please analyze documents first.",
                        "message": "Call /api/rag/analyze first to ingest documents"
                    }
            
            # Retrieve relevant context
            if context_override:
                context = context_override
            else:
                relevant_docs = self.retrieve_context(instruction, k=5)
                context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Create prompt template
            prompt_template = """You are an expert resume writer and career coach. 
You help tailor resumes to match job descriptions perfectly.

CONTEXT (Resume + Job Description):
{context}

USER INSTRUCTION:
{instruction}

TASK:
Based on the context above and the user's instruction, generate tailored resume content.
Focus on:
1. Matching keywords from job description
2. Quantifying achievements
3. Using action verbs
4. Highlighting relevant skills
5. Maintaining professional tone

Generate clear, impactful bullet points or sections that align with the job requirements.

TAILORED CONTENT:"""

            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "instruction"]
            )
            
            # Create RAG chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": prompt}
            )
            
            # Generate response
            result = qa_chain({"query": instruction})
            
            return {
                "success": True,
                "tailored_content": result["result"],
                "source_documents": [doc.page_content[:200] for doc in result["source_documents"]],
                "instruction": instruction
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate tailored content"
            }
    
    
    def interactive_tailor(self, user_id: str) -> Dict[str, Any]:
        """
        Interactive mode for resume tailoring
        Allows continuous learning from user feedback
        
        Args:
            user_id: User identifier
            
        Returns:
            Session data and generated content
        """
        session_data = {
            "user_id": user_id,
            "interactions": [],
            "improvements": []
        }
        
        return session_data
    
    
    def learn_from_feedback(self, user_id: str, instruction: str, 
                           generated_content: str, feedback: str,
                           rating: int) -> Dict[str, Any]:
        """
        Learn from user feedback to improve future generations
        
        Args:
            user_id: User identifier
            instruction: Original instruction
            generated_content: Content that was generated
            feedback: User's feedback text
            rating: Rating 1-5
            
        Returns:
            Learning status
        """
        try:
            # Create feedback document
            feedback_doc = Document(
                page_content=f"""
INSTRUCTION: {instruction}
GENERATED: {generated_content}
USER FEEDBACK: {feedback}
RATING: {rating}/5
                """,
                metadata={
                    "type": "feedback",
                    "user_id": user_id,
                    "rating": rating
                }
            )
            
            # Add to vector store for future reference
            if self.vector_store:
                chunks = self.text_splitter.split_documents([feedback_doc])
                self.vector_store.add_documents(chunks)
                
                return {
                    "success": True,
                    "message": "Feedback stored for continuous learning"
                }
            
            return {
                "success": False,
                "message": "Vector store not initialized"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    
    def get_suggestions(self, resume_text: str, job_description: str) -> List[str]:
        """
        Get AI-powered suggestions for resume improvement
        
        Args:
            resume_text: Current resume
            job_description: Target job description
            
        Returns:
            List of improvement suggestions
        """
        try:
            # Handle empty or generic JD
            has_specific_jd = job_description and len(job_description.strip()) > 50
            
            if has_specific_jd:
                prompt = f"""You are an expert resume coach. Analyze this resume against the job description and provide specific, actionable improvements.

RESUME:
{resume_text[:3000]}

TARGET JOB DESCRIPTION:
{job_description[:2000]}

Provide exactly 5 specific, actionable suggestions. Each suggestion should:
- Start with a clear action verb (Add, Quantify, Highlight, Reframe, Include)
- Be specific to this resume's content
- Directly improve alignment with the job requirements

Format each suggestion as a single numbered line like:
1. [Action] - [Specific recommendation]

SUGGESTIONS:"""
            else:
                prompt = f"""You are an expert resume coach. Analyze this resume and provide specific improvements to make it stronger and more impactful.

RESUME:
{resume_text[:3000]}

Provide exactly 5 specific, actionable suggestions to improve this resume. Focus on:
- Adding quantifiable metrics and achievements
- Strengthening action verbs
- Improving professional impact
- Highlighting transferable skills
- Enhancing overall clarity and readability

Format each suggestion as a single numbered line like:
1. [Action] - [Specific recommendation based on actual content in the resume]

SUGGESTIONS:"""

            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            
            # Parse suggestions - look for numbered lines
            raw_lines = response.text.strip().split('\n')
            suggestions = []
            for line in raw_lines:
                line = line.strip()
                # Check if it starts with a number followed by . or )
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    # Clean up the line
                    cleaned = line.lstrip('0123456789.-•) ').strip()
                    if cleaned and len(cleaned) > 10:
                        suggestions.append(cleaned)
            
            # If parsing failed, return raw lines
            if not suggestions:
                suggestions = [s.strip() for s in raw_lines if s.strip() and len(s.strip()) > 10]
            
            return suggestions[:5]  # Return top 5
            
        except Exception as e:
            print(f"❌ Suggestion generation error: {e}")
            return [f"Unable to generate suggestions: {str(e)}. Please check your GEMINI_API_KEY."]


# Singleton instance
_rag_engine = None

def get_rag_engine() -> RAGEngine:
    """Get or create RAG engine singleton"""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine

