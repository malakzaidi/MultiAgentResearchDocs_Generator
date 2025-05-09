#!/usr/bin/env python
import sys
import os
from datetime import datetime
from medical_report_system.crew import MultiAgentDocsCrew


def run():
    """
    Run the crew with specified topic and tasks.
    """
    # Get inputs from command-line arguments, environment variables, or defaults
    topic = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('TOPIC', 'Quantum Computing')
    tasks = sys.argv[2].split(',') if len(sys.argv) > 2 else os.environ.get('SELECTED_TASKS', '').split(',')
    current_year = sys.argv[3] if len(sys.argv) > 3 else os.environ.get('CURRENT_YEAR', str(datetime.now().year))

    # Filter out empty task strings
    tasks = [t for t in tasks if t]

    inputs = {
        'topic': topic,
        'current_year': current_year
    }

    try:
        # Set environment variables for task filtering
        os.environ['TOPIC'] = topic
        os.environ['CURRENT_YEAR'] = current_year
        os.environ['SELECTED_TASKS'] = ','.join(tasks) if tasks else ''

        # Run the crew
        crew = MultiAgentDocsCrew().crew()
        crew.kickoff(inputs=inputs)
        print(f"Successfully ran crew for topic: {topic}")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    finally:
        # Clean up environment variables
        os.environ.pop('TOPIC', None)
        os.environ.pop('CURRENT_YEAR', None)
        os.environ.pop('SELECTED_TASKS', None)


def train():
    """
    Train the crew for a given number of iterations.
    """
    topic = sys.argv[3] if len(sys.argv) > 3 else os.environ.get('TOPIC', 'Quantum Computing')
    tasks = sys.argv[4].split(',') if len(sys.argv) > 4 else os.environ.get('SELECTED_TASKS', '').split(',')
    current_year = sys.argv[5] if len(sys.argv) > 5 else os.environ.get('CURRENT_YEAR', str(datetime.now().year))

    tasks = [t for t in tasks if t]
    inputs = {
        'topic': topic,
        'current_year': current_year
    }

    try:
        os.environ['TOPIC'] = topic
        os.environ['CURRENT_YEAR'] = current_year
        os.environ['SELECTED_TASKS'] = ','.join(tasks) if tasks else ''

        crew = MultiAgentDocsCrew().crew()
        crew.train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
        print(f"Successfully trained crew for {sys.argv[1]} iterations on topic: {topic}")
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
    finally:
        os.environ.pop('TOPIC', None)
        os.environ.pop('CURRENT_YEAR', None)
        os.environ.pop('SELECTED_TASKS', None)


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        crew = MultiAgentDocsCrew().crew()
        crew.replay(task_id=sys.argv[1])
        print(f"Successfully replayed crew from task: {sys.argv[1]}")
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and return the results.
    """
    topic = sys.argv[3] if len(sys.argv) > 3 else os.environ.get('TOPIC', 'Quantum Computing')
    tasks = sys.argv[4].split(',') if len(sys.argv) > 4 else os.environ.get('SELECTED_TASKS', '').split(',')
    current_year = sys.argv[5] if len(sys.argv) > 5 else os.environ.get('CURRENT_YEAR', str(datetime.now().year))

    tasks = [t for t in tasks if t]
    inputs = {
        'topic': topic,
        'current_year': current_year
    }

    try:
        os.environ['TOPIC'] = topic
        os.environ['CURRENT_YEAR'] = current_year
        os.environ['SELECTED_TASKS'] = ','.join(tasks) if tasks else ''

        crew = MultiAgentDocsCrew().crew()
        results = crew.test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
        print(f"Test results: {results}")
        return results
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
    finally:
        os.environ.pop('TOPIC', None)
        os.environ.pop('CURRENT_YEAR', None)
        os.environ.pop('SELECTED_TASKS', None)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['train', 'replay', 'test']:
        globals()[sys.argv[1]]()
    else:
        run()