#!/usr/bin/env python3
"""
OIDC Provider Test Suite - Different Testing Options
"""

import subprocess
import sys
import os

print("🧪 OIDC Provider Test Suite")
print("="*50)
print()
print("Available test options:")
print()
print("1. 🤖 Automated End-to-End Test")
print("   - Fully automated programmatic test")
print("   - Tests all endpoints without browser")
print("   - Simulates user login and consent")
print("   - File: test_flow_complete.py")
print()
print("2. 🌐 Interactive Browser Test")
print("   - Opens browser for manual testing")
print("   - Real user login experience")
print("   - Visual consent flow")
print("   - File: test_client_enhanced.py")
print()
print("3. 📋 Unit Test Suite")
print("   - pytest-based unit tests")
print("   - Tests individual components")
print("   - Coverage reporting available")
print("   - Directory: tests/")
print()
print("4. 🔗 API Endpoint Tests")
print("   - Direct API testing")
print("   - cURL-based examples")
print("   - File: test_all_endpoints.py")
print()

def run_test(test_choice):
    """Run the selected test"""
    python_exe = r"e:\New Folder(1)\Downloads\oidc-2\OIDC-with-flask\.venv\Scripts\python.exe"
    
    if test_choice == "1":
        print("🤖 Running Automated End-to-End Test...")
        subprocess.run([python_exe, "test_flow_complete.py"])
    elif test_choice == "2":
        print("🌐 Starting Interactive Browser Test...")
        print("   -> The browser will open automatically")
        print("   -> Use credentials: alice / alicepassword")
        print("   -> Press Ctrl+C to stop when done")
        subprocess.run([python_exe, "test_client_enhanced.py"])
    elif test_choice == "3":
        print("📋 Running Unit Test Suite...")
        subprocess.run([python_exe, "-m", "pytest", "tests/", "-v"])
    elif test_choice == "4":
        print("🔗 Running API Endpoint Tests...")
        subprocess.run([python_exe, "test_all_endpoints.py"])
    else:
        print("❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    while True:
        print("\nSelect a test to run (1-4), or 'q' to quit:")
        choice = input("Your choice: ").strip().lower()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        elif choice in ['1', '2', '3', '4']:
            print()
            run_test(choice)
            print("\n" + "="*50)
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, 4, or 'q'.")
