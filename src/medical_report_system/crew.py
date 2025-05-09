import os
import yaml
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

class MultiAgentDocsCrew:
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        logger.info(f"Computed base_dir: {self.base_dir}")

        self.config_dir = os.path.join(self.base_dir, 'src', 'medical_report_system', 'config')
        logger.info(f"Computed config_dir: {self.config_dir}")

        agents_yaml_path = os.path.join(self.config_dir, 'agents.yaml')
        tasks_yaml_path = os.path.join(self.config_dir, 'tasks.yaml')
        logger.info(f"Attempting to load agents.yaml from: {agents_yaml_path}")
        logger.info(f"Attempting to load tasks.yaml from: {tasks_yaml_path}")

        self.agents_config = self.load_yaml(agents_yaml_path)
        self.tasks_config = self.load_yaml(tasks_yaml_path)
        self.llm = self.initialize_llm()

    def load_yaml(self, file_path):
        try:
            if not os.path.exists(file_path):
                logger.error(f"File does not exist: {file_path}")
                raise FileNotFoundError(f"File not found: {file_path}")
            with open(file_path, 'r') as file:
                logger.info(f"Successfully opened YAML file: {file_path}")
                content = file.read()
                if not content.strip():
                    logger.error(f"YAML file is empty: {file_path}")
                    raise ValueError(f"YAML file is empty: {file_path}")
                data = yaml.safe_load(content)
                if data is None:
                    logger.error(f"YAML file contains no data after parsing: {file_path}")
                    raise ValueError(f"YAML file contains no data: {file_path}")
                return data
        except FileNotFoundError as e:
            logger.error(f"FileNotFoundError while loading YAML file {file_path}: {str(e)}")
            raise ValueError(f"Failed to load YAML configs: {str(e)}")
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in file {file_path}: {str(e)}")
            raise ValueError(f"Failed to load YAML configs: {str(e)}")
        except PermissionError as e:
            logger.error(f"PermissionError while accessing YAML file {file_path}: {str(e)}")
            raise ValueError(f"Failed to load YAML configs: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while loading YAML file {file_path}: {str(e)}")
            raise ValueError(f"Failed to load YAML configs: {str(e)}")

    def initialize_llm(self):
        if os.environ.get('OPENROUTER_API_KEY'):
            logger.info("Initializing LLM with OpenRouter API")
            return ChatOpenAI(
                openai_api_key=os.environ.get('OPENROUTER_API_KEY'),
                openai_api_base='https://openrouter.ai/api/v1',
                model_name='openrouter/qwen/qwen3-32b:free'
            )
        else:
            logger.error("No valid API key found for LLM initialization")
            raise ValueError("OPENROUTER_API_KEY  must be set in .env")

    def crew(self):
        topic = os.environ.get('TOPIC', 'Default Topic')
        current_year = os.environ.get('CURRENT_YEAR', '2025')
        selected_tasks = os.environ.get('SELECTED_TASKS', '').split(',')

        logger.info(f"Selected tasks from environment: {selected_tasks}")

        # Initialize agents
        agents = {}
        for agent_name, config in self.agents_config.items():
            agents[agent_name] = Agent(
                role=config['role'].format(topic=topic),
                goal=config['goal'].format(topic=topic),
                backstory=config['backstory'].format(topic=topic),
                llm=self.llm,
                verbose=True,
                allow_delegation=True,
                capabilities=config.get('capabilities', [])
            )
            logger.info(f"Initialized agent: {agent_name}")

        # Initialize tasks
        tasks = []
        for task_name, config in self.tasks_config.items():
            if task_name in selected_tasks:
                logger.info(f"Initializing task: {task_name} with config: {config}")
                task_description = config['description'].format(topic=topic, current_year=current_year)
                task = Task(
                    description=task_description,
                    expected_output=config['expected_output'].format(topic=topic, current_year=current_year),
                    agent=agents[config['agent']],
                    output_file=config.get('output_file')
                )
                tasks.append(task)
                logger.info(f"Initialized task: {task_name} with output {config.get('output_file')}")
            else:
                logger.info(f"Skipping task: {task_name} as it is not in selected_tasks")

        if not tasks:
            logger.warning("No tasks initialized. Check selected_tasks and tasks_config.")

        # Create and return crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=True
        )
        logger.info("Successfully initialized Crew with agents and tasks")

        # Wrap execution to include progress updates and generate master report
        def wrapped_execute(crew_instance, *args, **kwargs):
            logger.info("Starting crew execution")
            if self.progress_callback:
                self.progress_callback("System", "Starting all tasks", 0)

            # Execute tasks
            results = crew_instance.kickoff()

            if self.progress_callback:
                self.progress_callback("System", "All tasks completed", 100)

            logger.info(f"Crew execution completed with results: {results}")

            # Generate master_report.md by consolidating all task outputs
            self.generate_master_report(tasks)

            return True

        return crew, wrapped_execute

    def execute_crew(self, crew_instance, execute_func, *args, **kwargs):
        return execute_func(crew_instance, *args, **kwargs)

    def generate_master_report(self, tasks):
        output_path = os.path.join(self.base_dir, 'master_report.md')
        topic = os.environ.get('TOPIC', 'Default Topic')
        current_year = os.environ.get('CURRENT_YEAR', '2025')

        # Initialize the Markdown content
        md_content = [
            f"# Master Report on {topic}",
            f"**Generated on May 9, 2025**",
            "",
            "## Abstract",
            f"This report synthesizes comprehensive research, data analysis, narrative reporting, and ethical assessments on {topic} as of {current_year}. It integrates key insights into a cohesive narrative, highlighting technological advancements, data-driven trends, stakeholder implications, and ethical considerations. Strategic recommendations are provided to guide future developments.",
            "",
            "## Introduction",
            f"This report integrates findings from multiple perspectives to address {topic}'s current state and future potential. It covers research insights, data analysis, narrative reporting, and ethical considerations, providing a holistic view for stakeholders.",
            ""
        ]

        # Collect task outputs and append to the master report
        sections = [
            ("Research Findings", "research_brief.md"),
            ("Data Analysis", "data_analysis.md"),
            ("Narrative Report", "report.md"),
            ("Ethical Assessment", "ethics_assessment.md"),
            ("Presentation Summary", "presentation.md")
        ]

        for section_title, output_file in sections:
            file_path = os.path.join(self.base_dir, output_file)
            if os.path.exists(file_path):
                md_content.append(f"## {section_title}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    md_content.append(content)
                md_content.append("")
            else:
                logger.warning(f"Output file not found for {section_title}: {file_path}")

        # Add a recommendations section
        md_content.extend([
            "## Recommendations",
            "Based on the integrated findings, the following recommendations are proposed:",
            "- **Invest in Research Gaps**: Address identified knowledge gaps through targeted research initiatives.",
            "- **Enhance Ethical Frameworks**: Develop robust governance structures to mitigate risks and ensure fairness.",
            "- **Monitor Trends**: Continuously track emerging trends and adapt strategies accordingly.",
            "",
            "## Conclusion",
            f"This master report provides a comprehensive overview of {topic}, combining insights from various dimensions to inform future actions. It serves as a foundation for stakeholders to make informed decisions.",
            "",
            "## References",
            "- Sources and references are embedded within each section as applicable."
        ])

        # Write the master report to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_content))
        logger.info(f"Generated master_report.md at {output_path}")