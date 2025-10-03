import os
import sys
import subprocess
import platform
from pathlib import Path
import json

def print_msg(message):
    print(message)

def check_requirements():
    version = sys.version_info
    if version.major != 3 or version.minor < 8:
        print_msg(f"Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False
    try:
        import urllib.request
        urllib.request.urlopen('https://console.x.ai', timeout=5)
    except:
        print_msg("Internet connection may be limited.")
    return True

def install_dependencies():
    packages = ['requests>=2.31.0', 'python-dotenv>=1.0.0', 'schedule>=1.2.0', 'colorama>=0.4.6']
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--upgrade', '--quiet'])
        except subprocess.CalledProcessError as e:
            print_msg(f"Failed to install {package}: {e}")
            return False
    return True

def create_project_structure():
    for directory in ['output', 'logs', 'config', 'templates', 'backups']:
        Path(directory).mkdir(exist_ok=True)
    return True

def create_configuration_files():
    env_content = """GROK_API_KEY=your_grok_api_key_here
MARINE_DATA_API_URL=https://api.example.com/marine-data
MARINE_DATA_API_KEY=your_marine_api_key_here
LETTERS_PER_DAY=3
AUTO_SCHEDULE=true
OUTPUT_FORMAT=both
"""
    with open('.env', 'w') as f:
        f.write(env_content)

    organizations_config = {
        "organizations": {
            "policy_makers": {"name": "Ocean Policy Institute", "target_audience": "Government Officials"},
            "industry_leaders": {"name": "Sustainable Marine Industries Coalition", "target_audience": "Corporate Leaders"},
            "communities": {"name": "Coastal Communities Alliance", "target_audience": "Local Communities"}
        }
    }
    with open('config/organizations.json', 'w') as f:
        json.dump(organizations_config, f, indent=2)
    return True

def create_convenience_scripts():
    system = platform.system()
    if system == "Windows":
        batch_content = """@echo off
python marine_ai.py
pause"""
        with open('quick_run.bat', 'w') as f:
            f.write(batch_content)
    else:
        shell_content = """#!/bin/bash
python3 marine_ai.py
read -p "Press Enter to continue..." """
        with open('quick_run.sh', 'w') as f:
            f.write(shell_content)
        os.chmod('quick_run.sh', 0o755)
    return True

def final_setup_check():
    required_files = ['marine_ai.py', '.env', 'config/organizations.json']
    missing = [f for f in required_files if not Path(f).exists()]
    if missing:
        print_msg(f"Missing files: {', '.join(missing)}")
        return False
    try:
        import requests, dotenv, schedule, colorama
    except ImportError as e:
        print_msg(f"Missing dependency: {e}")
        return False
    return True

def main():
    if not check_requirements():
        return False
    if not install_dependencies():
        return False
    if not create_project_structure():
        return False
    if not create_configuration_files():
        return False
    if not create_convenience_scripts():
        return False
    if not final_setup_check():
        return False
    print_msg("Installation completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
