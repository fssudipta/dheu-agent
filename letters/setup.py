#!/usr/bin/env python3
"""
Marine Health AI Setup Script
Automatically sets up the environment and dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run shell command with error handling"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported")
        print("   Please install Python 3.8 or higher")
        return False

def create_project_structure():
    """Create necessary directories and files"""
    print("📁 Creating project structure...")
    
    directories = ['output', 'logs', 'templates', 'config']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ Created directory: {directory}/")
    
    # Create config file if it doesn't exist
    if not os.path.exists('config/organizations.json'):
        config = {
            "organizations": {
                "policy_makers": {
                    "name": "Ocean Policy Institute",
                    "target_audience": "Government Officials, Policy Makers, Environmental Agencies",
                    "tone": "formal, evidence-based, diplomatic",
                    "focus_areas": ["policy reform", "international cooperation", "regulatory frameworks", "funding allocation"],
                    "call_to_action": "implement stronger marine protection policies and increase funding",
                    "contact_info": "policy@oceaninstitute.org | +1-555-OCEAN-1"
                },
                "industry_leaders": {
                    "name": "Sustainable Marine Industries Coalition", 
                    "target_audience": "Corporate Leaders, Manufacturing, Shipping, Energy Companies",
                    "tone": "business-focused, solution-oriented, collaborative",
                    "focus_areas": ["sustainable practices", "green technology", "corporate responsibility", "economic benefits"],
                    "call_to_action": "adopt sustainable practices and invest in clean marine technologies",
                    "contact_info": "partnerships@marinecoalition.org | +1-555-OCEAN-2"
                },
                "communities": {
                    "name": "Coastal Communities Alliance",
                    "target_audience": "Local Communities, Volunteers, Community Leaders, Residents", 
                    "tone": "passionate, community-focused, inspiring",
                    "focus_areas": ["grassroots action", "local impact", "community engagement", "educational programs"],
                    "call_to_action": "join local conservation efforts and engage in community marine protection",
                    "contact_info": "community@coastalalliance.org | +1-555-OCEAN-3"
                }
            }
        }
        
        import json
        with open('config/organizations.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("   ✅ Created config/organizations.json")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        env_content = """# Marine Health AI Configuration
# Add your actual API key below

# Your Grok API Key (get from https://console.x.ai/)
GROK_API_KEY=your_grok_api_key_here

# Optional settings
LETTERS_PER_DAY=3
AUTO_SCHEDULE=true
OUTPUT_FORMAT=both
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("   ✅ Created .env file (remember to add your API key!)")
    else:
        print("   ℹ️  .env file already exists")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing Python dependencies...")
    
    # Check if pip is available
    if not shutil.which('pip') and not shutil.which('pip3'):
        print("   ❌ pip not found. Please install pip first.")
        return False
    
    pip_command = 'pip3' if shutil.which('pip3') else 'pip'
    
    # Install requirements
    if os.path.exists('requirements.txt'):
        return run_command(f"{pip_command} install -r requirements.txt", "Installing requirements")
    else:
        # Install manually if requirements.txt doesn't exist
        packages = ['requests', 'python-dotenv', 'schedule', 'colorama']
        for package in packages:
            if not run_command(f"{pip_command} install {package}", f"Installing {package}"):
                return False
        return True

def create_run_script():
    """Create convenient run scripts"""
    
    # Windows batch script
    batch_script = """@echo off
echo 🌊 Starting Marine Health AI Letter Generator...
python marine_ai.py
pause
"""
    with open('run.bat', 'w') as f:
        f.write(batch_script)
    
    # Unix shell script  
    shell_script = """#!/bin/bash
echo "🌊 Starting Marine Health AI Letter Generator..."
python3 marine_ai.py
"""
    with open('run.sh', 'w') as f:
        f.write(shell_script)
    
    # Make shell script executable on Unix systems
    if os.name != 'nt':
        os.chmod('run.sh', 0o755)
    
    print("   ✅ Created run scripts (run.bat for Windows, run.sh for Unix)")

def create_scheduler_script():
    """Create automated scheduling script"""
    scheduler_code = """#!/usr/bin/env python3
import schedule
import time
from datetime import datetime
import os
from marine_ai import main as generate_letters

def scheduled_generation():
    print(f"⏰ Scheduled letter generation started at {datetime.now()}")
    try:
        generate_letters()
        print(f"✅ Scheduled generation completed at {datetime.now()}")
    except Exception as e:
        print(f"❌ Scheduled generation failed: {e}")

def run_scheduler():
    print("📅 Marine Health AI Scheduler Started")
    print("📋 Schedule: Daily at 9:00 AM")
    print("   Press Ctrl+C to stop")
    
    # Schedule daily generation at 9 AM
    schedule.every().day.at("09:00").do(scheduled_generation)
    
    # Also run immediately on startup
    print("🚀 Running initial generation...")
    scheduled_generation()
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    run_scheduler()
"""
    
    with open('scheduler.py', 'w') as f:
        f.write(scheduler_code)
    print("   ✅ Created scheduler.py for automated daily generation")

def main():
    """Main setup function"""
    print("🌊 Marine Health AI Letter Generator Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create project structure
    create_project_structure()
    
    # Create environment file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Create convenience scripts
    create_run_script()
    create_scheduler_script()
    
    print()
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("📋 Next Steps:")
    print("1. Edit the .env file and add your Grok API key")
    print("2. Run: python marine_ai.py (or use run.bat/run.sh)")
    print("3. For automated daily letters: python scheduler.py")
    print()
    print("📁 Project Structure:")
    print("   marine_ai.py      - Main letter generator")
    print("   scheduler.py      - Automated daily generation") 
    print("   config/           - Organization configurations")
    print("   output/           - Generated letters and reports")
    print("   logs/             - Application logs")
    print("   .env              - Your API keys (EDIT THIS!)")
    print()
    print("🔑 Don't forget to add your Grok API key to the .env file!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)