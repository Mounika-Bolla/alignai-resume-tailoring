"""
AlignAI Backend Server
---------------------
Complete backend server handling:
- User authentication (login/signup/OAuth)
- Resume uploads and parsing
- AI chat and resume generation
- Resume library management
"""

from flask import Flask, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from urllib.parse import urlencode
import secrets
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import configuration and modules
load_dotenv()

# ============================================================================
# FLASK APP CONFIGURATION
# ============================================================================

app = Flask(__name__)

# Security Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'alignai-secret-key-change-in-production-12345')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_NAME'] = 'alignai_session'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

# Database Configuration - PostgreSQL
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'alignai_db')

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize database
db = SQLAlchemy(app)

# CORS Configuration
CORS(app, 
     supports_credentials=True,
     origins=['http://localhost:8000', 'http://127.0.0.1:8000'],
     allow_headers=['Content-Type', 'Cookie'],
     expose_headers=['Set-Cookie'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# File upload settings
ALLOWED_EXTENSIONS = {'pdf', 'docx'}


# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    resumes = db.relationship('SavedResume', backref='owner', lazy=True, cascade='all, delete-orphan')
    chat_sessions = db.relationship('ChatSession', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SavedResume(db.Model):
    """Saved resumes in user's library"""
    __tablename__ = 'saved_resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    file_type = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'file_type': self.file_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ChatSession(db.Model):
    """Chat sessions for AI interactions"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')


class ChatMessage(db.Model):
    """Individual chat messages"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def init_database():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")


def get_current_user():
    """Get currently logged-in user from session"""
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================================================
# FILE PARSER
# ============================================================================

class FileParser:
    """Parse PDF and DOCX files to extract text"""
    
    @staticmethod
    def parse_pdf(file_path):
        """Extract text from PDF file"""
        try:
            import pypdf
            text = []
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            raise
    
    @staticmethod
    def parse_docx(file_path):
        """Extract text from DOCX file"""
        try:
            from docx import Document
            doc = Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            raise
    
    @staticmethod
    def parse_file(file_path):
        """Parse file based on extension"""
        ext = file_path.rsplit('.', 1)[1].lower()
        if ext == 'pdf':
            return FileParser.parse_pdf(file_path)
        elif ext == 'docx':
            return FileParser.parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")


# ============================================================================
# AI AGENT INTEGRATION
# ============================================================================

# Try to import AI agent
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))
    from resume_generator import ResumeGeneratorAgent
    AI_ENABLED = True
    print("✅ AI Agent loaded successfully")
except ImportError as e:
    print(f"⚠️  Warning: AI Agent not available: {e}")
    AI_ENABLED = False


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'AlignAI Backend is running'}), 200


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """User registration"""
    try:
        data = request.get_json()
        full_name = data.get('fullName', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not all([full_name, email, password]):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(full_name=full_name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Log them in
        session.permanent = True
        session['user_id'] = user.id
        session['user_email'] = user.email
        
        print(f"✅ New user registered: {user.email}")
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Signup error: {e}")
        return jsonify({'success': False, 'error': 'Registration failed'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create session
        session.permanent = True
        session['user_id'] = user.id
        session['user_email'] = user.email
        
        print(f"✅ User logged in: {user.email}")
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return jsonify({'success': False, 'error': 'Login failed'}), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200


@app.route('/api/auth/check-session', methods=['GET'])
def check_session():
    """Check if user is authenticated"""
    user = get_current_user()
    
    if user:
        return jsonify({
            'authenticated': True,
            'user': user.to_dict()
        }), 200
    else:
        return jsonify({'authenticated': False}), 200


# ============================================================================
# RESUME ROUTES
# ============================================================================

@app.route('/api/resume/upload', methods=['POST'])
def upload_resume():
    """Upload and parse resume file"""
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type. Only PDF and DOCX allowed'}), 400
    
    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join('/tmp', filename)
        file.save(temp_path)
        
        # Parse file
        content = FileParser.parse_file(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        print(f"✅ Resume parsed: {filename} ({len(content)} chars)")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'content': content,
            'length': len(content)
        }), 200
        
    except Exception as e:
        print(f"❌ Resume upload error: {e}")
        return jsonify({'success': False, 'error': f'Failed to parse resume: {str(e)}'}), 500


@app.route('/api/resume/save', methods=['POST'])
def save_resume_to_library():
    """Save resume to user's library"""
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        content = data.get('content', '')
        file_type = data.get('file_type', 'text')
        
        if not name or not content:
            return jsonify({'success': False, 'error': 'Name and content required'}), 400
        
        # Create saved resume
        resume = SavedResume(
            user_id=user.id,
            name=name,
            content=content,
            file_type=file_type
        )
        db.session.add(resume)
        db.session.commit()
        
        print(f"✅ Resume saved: {name} (User: {user.email})")
        
        return jsonify({
            'success': True,
            'resume': resume.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Save resume error: {e}")
        return jsonify({'success': False, 'error': 'Failed to save resume'}), 500


@app.route('/api/resume/list', methods=['GET'])
def list_resumes():
    """Get all resumes for current user"""
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        resumes = SavedResume.query.filter_by(user_id=user.id).order_by(SavedResume.updated_at.desc()).all()
        return jsonify({
            'success': True,
            'resumes': [r.to_dict() for r in resumes]
        }), 200
    except Exception as e:
        print(f"❌ List resumes error: {e}")
        return jsonify({'success': False, 'error': 'Failed to fetch resumes'}), 500


@app.route('/api/resume/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get specific resume"""
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    resume = SavedResume.query.filter_by(id=resume_id, user_id=user.id).first()
    if not resume:
        return jsonify({'success': False, 'error': 'Resume not found'}), 404
    
    return jsonify({'success': True, 'resume': resume.to_dict()}), 200


@app.route('/api/resume/<int:resume_id>', methods=['DELETE'])
def delete_resume_route(resume_id):
    """Delete resume"""
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        resume = SavedResume.query.filter_by(id=resume_id, user_id=user.id).first()
        if not resume:
            return jsonify({'success': False, 'error': 'Resume not found'}), 404
        
        db.session.delete(resume)
        db.session.commit()
        
        print(f"✅ Resume deleted: {resume.name}")
        return jsonify({'success': True, 'message': 'Resume deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Delete resume error: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete resume'}), 500


@app.route('/api/resume/<int:resume_id>/rename', methods=['PUT'])
def rename_resume(resume_id):
    """Rename resume"""
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        new_name = data.get('name', '').strip()
        
        if not new_name:
            return jsonify({'success': False, 'error': 'Name required'}), 400
        
        resume = SavedResume.query.filter_by(id=resume_id, user_id=user.id).first()
        if not resume:
            return jsonify({'success': False, 'error': 'Resume not found'}), 404
        
        old_name = resume.name
        resume.name = new_name
        resume.updated_at = datetime.utcnow()
        db.session.commit()
        
        print(f"✅ Resume renamed: '{old_name}' → '{new_name}'")
        return jsonify({'success': True, 'resume': resume.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Rename resume error: {e}")
        return jsonify({'success': False, 'error': 'Failed to rename resume'}), 500


# ============================================================================
# AI CHAT ROUTES
# ============================================================================

@app.route('/api/chat/message', methods=['POST'])
def chat_message():
    """Handle AI chat messages"""
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    if not AI_ENABLED:
        return jsonify({
            'success': False,
            'error': 'AI features not available'
        }), 503
    
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        resume_text = data.get('resume', '')
        job_description = data.get('job_description', '')
        
        if not user_message:
            return jsonify({'success': False, 'error': 'Message required'}), 400
        
        # TODO: Integrate with ResumeGeneratorAgent
        # For now, return a placeholder response
        ai_response = f"I received your message: '{user_message[:50]}...'"
        
        if resume_text:
            ai_response += f"\nI can see you've provided a resume ({len(resume_text)} characters)."
        if job_description:
            ai_response += f"\nI can see the job description ({len(job_description)} characters)."
        
        return jsonify({
            'success': True,
            'response': ai_response
        }), 200
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({'success': False, 'error': 'Chat failed'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AlignAI Backend Server")
    print("="*60)
    
    # Initialize database
    init_database()
    
    print(f"✅ Server starting on http://127.0.0.1:5000")
    print(f"✅ Database: {POSTGRES_DB}")
    print(f"✅ AI Enabled: {AI_ENABLED}")
    print("="*60 + "\n")
    
    # Run server
    app.run(host='127.0.0.1', port=5000, debug=True)

