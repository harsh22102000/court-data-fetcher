#!/usr/bin/env python3
"""
Local development runner for Court Data Fetcher
Run this script instead of app.py for better local development experience
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Setup environment variables and paths for local development"""
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # Set default environment variables if not set
    env_defaults = {
        'FLASK_APP': 'main.py',
        'FLASK_ENV': 'development',
        'SESSION_SECRET': 'dev-secret-key-change-in-production',
        'DATABASE_URL': 'sqlite:///court_scraper.db'
    }
    
    for key, value in env_defaults.items():
        if key not in os.environ:
            os.environ[key] = value
    
    # Load .env file if it exists
    env_file = current_dir / '.env'
    if env_file.exists():
        print(f"Loading environment from {env_file}")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'selenium',
        'beautifulsoup4',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r dependencies.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def initialize_database():
    """Initialize the database if it doesn't exist"""
    from app import app, db
    
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database initialized successfully")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return False
    return True

def main():
    """Main function to run the application locally"""
    print("🚀 Starting Court Data Fetcher - Local Development")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Import and run the app
    try:
        from app import app
        print("\n🌐 Starting Flask development server...")
        print("📍 Application will be available at: http://127.0.0.1:5000")
        print("🛑 Press Ctrl+C to stop the server\n")
        
        # Run with debug mode for local development
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application failed to start: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()