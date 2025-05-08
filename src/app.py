from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import json
import pandas as pd
from crewai import Crew
from medical_report_system.crew import medical_report_system
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

@app.route('/api/generate', methods=['POST'])
def generate_documents():
    data = request.get_json()
    topic = data.get('topic')
    year = data.get('year', '2025')
    tasks = data.get('tasks', [])

    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    try:
        # Set environment variables
        os.environ['TOPIC'] = topic
        os.environ['CURRENT_YEAR'] = year
        os.environ['SELECTED_TASKS'] = ','.join(tasks) if tasks else ''

        # Run CrewAI workflow
        crew = medical_report_system().crew()
        crew.kickoff()

        # Collect generated files from project root
        files = [
            {
                'name': 'research_brief.md',
                'url': '/outputs/research_brief.md',
                'type': 'markdown',
                'content': open('research_brief.md', 'r').read() if os.path.exists('research_brief.md') else ''
            },
            {
                'name': 'data_analysis.md',
                'url': '/outputs/data_analysis.md',
                'type': 'markdown',
                'content': open('data_analysis.md', 'r').read() if os.path.exists('data_analysis.md') else ''
            },
            {
                'name': 'report.md',
                'url': '/outputs/report.md',
                'type': 'markdown',
                'content': open('report.md', 'r').read() if os.path.exists('report.md') else ''
            },
            {
                'name': 'ethics_assessment.md',
                'url': '/outputs/ethics_assessment.md',
                'type': 'markdown',
                'content': open('ethics_assessment.md', 'r').read() if os.path.exists('ethics_assessment.md') else ''
            },
            {
                'name': 'master_report.md',
                'url': '/outputs/master_report.md',
                'type': 'markdown',
                'content': open('master_report.md', 'r').read() if os.path.exists('master_report.md') else ''
            },
            {
                'name': 'presentation.md',
                'url': '/outputs/presentation.md',
                'type': 'markdown',
                'content': open('presentation.md', 'r').read() if os.path.exists('presentation.md') else ''
            },
            {
                'name': 'dashboard_spec.json',
                'url': '/outputs/dashboard_spec.json',
                'type': 'json',
                'content': json.load(open('dashboard_spec.json')) if os.path.exists('dashboard_spec.json') else {}
            },
            {
                'name': 'tracking_template.csv',
                'url': '/outputs/tracking_template.csv',
                'type': 'excel',
                'content': pd.read_excel('tracking_template.csv').to_dict('records') if os.path.exists('tracking_template.xlsx') else []
            }
        ]
        files = [f for f in files if os.path.exists(f['name'])]

        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up environment variables
        os.environ.pop('SELECTED_TASKS', None)
        os.environ.pop('TOPIC', None)
        os.environ.pop('CURRENT_YEAR', None)

@app.route('/outputs/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

@app.route('/')
def serve_ui():
    return send_file('medical_report_system/frontend/index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)