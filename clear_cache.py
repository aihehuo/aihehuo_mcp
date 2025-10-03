#!/usr/bin/env python3
"""
Clear Python cache and test import
"""
import sys
import os
import shutil

# Clear all Python cache
def clear_python_cache():
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))
        for file_name in files:
            if file_name.endswith('.pyc'):
                os.remove(os.path.join(root, file_name))

if __name__ == "__main__":
    print("Clearing Python cache...")
    clear_python_cache()
    
    # Test import
    try:
        import aihehuo_mcp.server
        print("✅ Import successful after cache clear")
    except Exception as e:
        print(f"❌ Import failed: {e}")

