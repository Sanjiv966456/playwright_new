#!/usr/bin/env python3
import subprocess
import sys
import os

# Try to use allure from node_modules or system
try:
    # For Windows, try npm's allure
    result = subprocess.run(
        ['npx', 'allure', 'generate', 'allure-results', '-o', 'allure-report', '--clean'],
        cwd=os.getcwd(),
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✓ Allure report generated successfully!")
        print(f"✓ Report location: {os.path.abspath('allure-report/index.html')}")
        
        # List the files in allure-report
        if os.path.exists('allure-report'):
            print("\nGenerated files:")
            for root, dirs, files in os.walk('allure-report'):
                for file in files:
                    filepath = os.path.join(root, file)
                    print(f"  - {filepath}")
    else:
        print(f"Error: {result.stderr}")
except Exception as e:
    print(f"npx not available, trying direct method: {e}")
    print("\nAllure results directory created at: allure-results/")
    print("\nTo view the report, you can:")
    print("1. Install allure globally: npm install -g allure-commandline")
    print("2. Then run: allure serve allure-results")
