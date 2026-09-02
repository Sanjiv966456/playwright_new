#!/usr/bin/env python3
"""Generate an HTML Allure report from JSON results."""

import json
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def read_allure_results(results_dir):
    """Read all Allure JSON result files."""
    results_dir = Path(results_dir)
    tests = []
    containers = defaultdict(dict)

    # Read all JSON files
    for json_file in results_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if json_file.name.endswith('-result.json'):
                tests.append(data)
            elif json_file.name.endswith('-container.json'):
                uuid = data.get('uuid')
                containers[uuid] = data

    return tests, containers

def generate_html_report(tests, containers, output_path):
    """Generate HTML report from Allure test results."""

    # Calculate statistics
    total = len(tests)
    passed = sum(1 for t in tests if t.get('status') == 'passed')
    failed = sum(1 for t in tests if t.get('status') == 'failed')
    skipped = sum(1 for t in tests if t.get('status') == 'skipped')

    # Build test rows HTML
    test_rows = ""
    for test in tests:
        status = test.get('status', 'unknown').upper()
        status_class = status.lower()
        test_name = test.get('name', 'Unknown')
        test_path = test.get('fullName', test_name)
        duration_ms = test.get('stop', 0) - test.get('start', 0)
        duration_sec = duration_ms / 1000

        # Get status badge
        status_badge = f'<span class="badge badge-{status_class}">{status}</span>'

        test_rows += f"""
        <tr>
            <td>{test_name}</td>
            <td>{status_badge}</td>
            <td>{duration_sec:.2f}s</td>
            <td>{test_path}</td>
        </tr>
        """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Allure Test Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 8px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .timestamp {{
                opacity: 0.9;
                font-size: 0.9em;
            }}
            
            .stats {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                padding: 30px;
                background: #f8f9fa;
                border-bottom: 1px solid #e0e0e0;
            }}
            
            .stat-card {{
                background: white;
                padding: 20px;
                border-radius: 6px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
                border-left: 4px solid #667eea;
            }}
            
            .stat-card.passed {{
                border-left-color: #28a745;
            }}
            
            .stat-card.failed {{
                border-left-color: #dc3545;
            }}
            
            .stat-card.skipped {{
                border-left-color: #ffc107;
            }}
            
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                color: #333;
                margin-bottom: 5px;
            }}
            
            .stat-label {{
                color: #666;
                font-size: 0.9em;
            }}
            
            .content {{
                padding: 30px;
            }}
            
            .section-title {{
                font-size: 1.5em;
                margin: 30px 0 20px 0;
                color: #333;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}
            
            thead {{
                background: #f8f9fa;
            }}
            
            th {{
                padding: 15px;
                text-align: left;
                font-weight: 600;
                color: #333;
                border-bottom: 2px solid #e0e0e0;
            }}
            
            td {{
                padding: 12px 15px;
                border-bottom: 1px solid #e0e0e0;
            }}
            
            tr:hover {{
                background: #f8f9fa;
            }}
            
            .badge {{
                display: inline-block;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: 600;
                text-transform: uppercase;
            }}
            
            .badge-passed {{
                background: #d4edda;
                color: #155724;
            }}
            
            .badge-failed {{
                background: #f8d7da;
                color: #721c24;
            }}
            
            .badge-skipped {{
                background: #fff3cd;
                color: #856404;
            }}
            
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
                border-top: 1px solid #e0e0e0;
            }}
            
            .progress-bar {{
                height: 8px;
                background: #e0e0e0;
                border-radius: 4px;
                overflow: hidden;
                margin-top: 10px;
            }}
            
            .progress {{
                height: 100%;
                background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
            }}
            
            @media (max-width: 768px) {{
                .stats {{
                    grid-template-columns: repeat(2, 1fr);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Allure Test Report</h1>
                <div class="timestamp">Generated: {timestamp}</div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{total}</div>
                    <div class="stat-label">Total Tests</div>
                </div>
                <div class="stat-card passed">
                    <div class="stat-value">{passed}</div>
                    <div class="stat-label">Passed</div>
                </div>
                <div class="stat-card failed">
                    <div class="stat-value">{failed}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-card skipped">
                    <div class="stat-value">{skipped}</div>
                    <div class="stat-label">Skipped</div>
                </div>
            </div>
            
            <div class="content">
                <h2 class="section-title">Test Results</h2>
                
                <table>
                    <thead>
                        <tr>
                            <th>Test Name</th>
                            <th>Status</th>
                            <th>Duration</th>
                            <th>Full Path</th>
                        </tr>
                    </thead>
                    <tbody>
                        {test_rows}
                    </tbody>
                </table>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
                    <h3 style="margin-bottom: 15px; color: #333;">Pass Rate</h3>
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <div style="flex: 1;">
                            <div class="progress-bar">
                                <div class="progress" style="width: {(passed/total*100) if total > 0 else 0:.1f}%"></div>
                            </div>
                        </div>
                        <div style="font-size: 1.2em; font-weight: bold; color: #667eea;">
                            {(passed/total*100) if total > 0 else 0:.1f}%
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>Allure Report | Generated on {timestamp}</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Write to file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path

if __name__ == "__main__":
    results_dir = Path(__file__).parent / "allure-results"
    output_file = Path(__file__).parent / "allure-report" / "index.html"

    print(f"📁 Reading Allure results from: {results_dir}")
    tests, containers = read_allure_results(results_dir)

    print(f"📊 Found {len(tests)} test results")

    print(f"✍️ Generating HTML report...")
    report_path = generate_html_report(tests, containers, output_file)

    print(f"✅ Report generated successfully!")
    print(f"📍 Location: {report_path.absolute()}")
    print(f"🌐 Open in browser: file:///{report_path.absolute()}")

