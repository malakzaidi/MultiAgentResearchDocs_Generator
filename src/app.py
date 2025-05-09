from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import os
import json
import logging
from crewai import Process
from medical_report_system.crew import MultiAgentDocsCrew
from dotenv import load_dotenv
import queue
import time

app = Flask(__name__)
CORS(app)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Queue for progress updates
progress_queue = queue.Queue()

# Task ID mapping for potential frontend mismatches
TASK_MAPPING = {
    'task-research': 'research_task',
    'task-data': 'data_analysis_task',
    'task-report': 'reporting_task',
    'task-ethics': 'ethics_assessment_task',
    'task-master': 'master_report_task',
    'task-presentation': 'presentation_task',
    'task-dashboard': 'dashboard_spec_task'
}

@app.route('/')
def health_check():
    logger.info("Health check endpoint accessed")
    return jsonify({'message': 'Flask server is running. Use /api/generate to create reports.'}), 200

@app.route('/api/generate', methods=['POST'])
def generate_documents():
    data = request.get_json()
    topic = data.get('topic')
    year = data.get('year', '2025')
    tasks = data.get('tasks', [])

    if not topic:
        logger.error("Topic is required")
        return jsonify({'error': 'Topic is required'}), 400

    # Map task IDs
    tasks = [TASK_MAPPING.get(t, t) for t in tasks]

    try:
        logger.info(f"Starting document generation for topic: {topic}, year: {year}, tasks: {tasks}")
        # Verify environment variables
        if not os.environ.get('OPENROUTER_API_KEY'):
            logger.error("Missing API key")
            raise ValueError("OPENROUTER_API_KEY must be set in .env")

        # Set environment variables
        os.environ['TOPIC'] = topic
        os.environ['CURRENT_YEAR'] = year
        os.environ['SELECTED_TASKS'] = ','.join(tasks) if tasks else ''

        # Initialize Crew with progress callback
        def progress_callback(agent, task, status):
            message = f"{agent}: {task} - {status}%"
            progress_queue.put(message)
            logger.debug(message)

        # Create the MultiAgentDocsCrew instance with our progress callback
        crew_manager = MultiAgentDocsCrew(progress_callback=progress_callback)

        # Execute the crew using the created crew instance
        crew_manager.execute_crew(crew_manager.create_crew())

        # Collect the generated master report
        files = [
            {
                'name': 'master_report.md',
                'url': '/outputs/master_report.md',
                'type': 'markdown',
                'content': open(os.path.join(BASE_DIR, 'master_report.md'), 'r').read() if os.path.exists(
                    os.path.join(BASE_DIR, 'master_report.md')) else ''
            }
        ]
        files = [f for f in files if os.path.exists(os.path.join(BASE_DIR, f['name']))]

        logger.info(f"Generated files: {[f['name'] for f in files]}")
        return jsonify({'files': files})
    except Exception as e:
        logger.exception(f"Error generating documents: {str(e)}")
        return jsonify({'error': f'Failed to generate documents: {str(e)}'}), 500
    finally:
        # Clean up environment variables
        os.environ.pop('SELECTED_TASKS', None)
        os.environ.pop('TOPIC', None)
        os.environ.pop('CURRENT_YEAR', None)

@app.route('/api/progress')
def progress():
    def stream():
        while True:
            try:
                message = progress_queue.get_nowait()
                logger.debug(f"Progress message sent: {message}")
                yield f"data: {json.dumps({'message': message})}\n\n"
            except queue.Empty:
                time.sleep(0.1)
                yield f"data: {json.dumps({'message': 'waiting'})}\n\n"

    return Response(stream(), mimetype='text/event-stream')

@app.route('/api/placeholder/<int:width>/<int:height>')
def placeholder(width, height):
    logger.info(f"Placeholder endpoint called: {width}x{height}")
    return jsonify({'message': f'Placeholder {width}x{height} not implemented'}), 200

@app.route('/outputs/<path:filename>')
def serve_file(filename):
    try:
        logger.info(f"Serving file: {filename}")
        return send_from_directory(BASE_DIR, filename)
    except FileNotFoundError as e:
        logger.error(f"File not found: {filename}, error: {str(e)}")
        return jsonify({'error': f'File {filename} not found'}), 404

# Log unknown routes
@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"404 error: {request.url} not found")
    return jsonify({'error': 'Not Found', 'message': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)