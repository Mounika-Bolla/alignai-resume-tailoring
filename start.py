"""
Start Script for AlignAI
------------------------
Starts both backend server and frontend server with one command
"""

import subprocess
import sys
import os
import time

def check_port(port):
    """Check if port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0  # True if port is free


def kill_port(port):
    """Kill process using the port (Windows)"""
    try:
        if sys.platform == 'win32':
            # Find process using the port
            result = subprocess.run(
                f'netstat -ano | findstr :{port}',
                shell=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        subprocess.run(f'taskkill /PID {pid} /F', shell=True, capture_output=True)
                        print(f"  Killed process on port {port} (PID: {pid})")
        else:
            # Unix/Linux
            subprocess.run(f'lsof -ti:{port} | xargs kill -9', shell=True, capture_output=True)
            print(f"  Killed process on port {port}")
    except Exception as e:
        print(f"  Warning: Could not kill process on port {port}: {e}")


def start_servers():
    """Start backend and frontend servers"""
    print("\n" + "="*60)
    print("🚀 Starting AlignAI Application")
    print("="*60 + "\n")
    
    # Check and clear ports
    print("📡 Checking ports...")
    ports = [5000, 8000]
    for port in ports:
        if not check_port(port):
            print(f"  Port {port} is in use, clearing...")
            kill_port(port)
            time.sleep(1)
    
    print("✅ Ports are ready\n")
    
    # Start backend server - DON'T capture output, let it print
    print("🔧 Starting Backend Server (Port 5000)...")
    print("=" * 60)
    backend_cmd = [sys.executable, os.path.join('backend', 'server.py')]
    backend_process = subprocess.Popen(
        backend_cmd,
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    
    time.sleep(3)  # Give backend time to start
    
    # Check if backend is still running
    if backend_process.poll() is not None:
        print("\n❌ Backend server failed to start!")
        print("💡 Try running manually to see the error:")
        print("   python backend/server.py")
        sys.exit(1)
    
    # Start frontend server
    print("\n🌐 Starting Frontend Server (Port 8000)...")
    print("=" * 60)
    frontend_cmd = [
        sys.executable,
        '-m',
        'http.server',
        '8000',
        '--directory',
        'frontend'
    ]
    frontend_process = subprocess.Popen(
        frontend_cmd,
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    
    time.sleep(2)
    
    # Check if frontend is still running
    if frontend_process.poll() is not None:
        print("\n❌ Frontend server failed to start!")
        backend_process.terminate()
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ AlignAI is Running!")
    print("="*60)
    print("\n📱 Open in your browser:")
    print("   Homepage:  http://localhost:8000/index.html")
    print("   Login:     http://localhost:8000/login.html")
    print("   Dashboard: http://localhost:8000/dashboard.html")
    print("\n🔧 Backend API: http://localhost:5000/api")
    print("\n⚠️  Servers running in separate windows.")
    print("    Close those windows or press Ctrl+C there to stop.")
    print("="*60 + "\n")
    
    try:
        # Keep script alive and monitor processes
        print("Monitoring servers... Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
            # Check if processes are still alive
            if backend_process.poll() is not None:
                print("\n❌ Backend server stopped unexpectedly!")
                frontend_process.terminate()
                sys.exit(1)
            if frontend_process.poll() is not None:
                print("\n❌ Frontend server stopped unexpectedly!")
                backend_process.terminate()
                sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped\n")


if __name__ == '__main__':
    try:
        start_servers()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Try running manually:")
        print("   1. python backend/server.py")
        print("   2. python -m http.server 8000 --directory frontend\n")
        sys.exit(1)

