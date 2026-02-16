"""
Run script for Elliott's League Helper with Visual GUI Window
"""

import sys
import os
from pathlib import Path

# Force unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'

# Add src directory to Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Import and run main with visual GUI
from main_visual import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
