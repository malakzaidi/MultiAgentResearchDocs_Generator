import os
import yaml
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import logging

# Configure logging with INFO level for faster execution
logging.basicConfig(
    level=logging.INFO,
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
        logger.info(f"Loading agents.yaml from: {agents_yaml_path}")
        logger.info(f"Loading tasks.yaml from: {tasks_yaml_path}")

        self.agents_config = self.load_yaml(agents_yaml_path)
        self.tasks_config = self.load_yaml(tasks_yaml_path)
        self.llm = self.initialize_llm()
        self.topic = os.environ.get('TOPIC', 'Default Topic')
        self.current_year = os.environ.get('CURRENT_YEAR', '2025')
        self.selected_tasks = os.environ.get('SELECTED_TASKS', '').split(',')
        logger.info(f"Selected tasks: {self.selected_tasks}")

    def load_yaml(self, file_path):
        try:
            if not os.path.exists(file_path):
                logger.error(f"File does not exist: {file_path}")
                raise FileNotFoundError(f"File not found: {file_path}")
            with open(file_path, 'r') as file:
                content = file.read()
                if not content.strip():
                    logger.error(f"YAML file is empty: {file_path}")
                    raise ValueError(f"YAML file is empty: {file_path}")
                data = yaml.safe_load(content)
                if data is None:
                    logger.error(f"YAML file contains no data: {file_path}")
                    raise ValueError(f"YAML file contains no data: {file_path}")
                return data
        except FileNotFoundError as e:
            logger.error(f"FileNotFoundError: {str(e)}")
            raise ValueError(f"Failed to load YAML configs: {str(e)}")
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {str(e)}")
            raise ValueError(f"Failed to load YAML configs: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
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
            raise ValueError("OPENROUTER_API_KEY must be set in .env")

    def run(self):
        # Define agents directly as per default crewai structure
        researcher = Agent(
            role="Senior Research Intelligence Specialist",
            goal=f"Conduct comprehensive research on {self.topic}",
            backstory="A seasoned researcher with expertise in AI advancements.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        logger.info("Agent initialized: researcher")

        data_analyst = Agent(
            role="Quantitative Intelligence Analyst",
            goal=f"Create a quantitative analysis framework for {self.topic}",
            backstory="An expert in transforming qualitative insights into data-driven patterns.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        logger.info("Agent initialized: data_analyst")

        reporting_analyst = Agent(
            role="Strategic Communication Specialist",
            goal=f"Transform findings into a comprehensive report on {self.topic}",
            backstory="A skilled communicator bridging technical and strategic insights.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        logger.info("Agent initialized: reporting_analyst")

        ethics_guardian = Agent(
            role="Ethics and Impact Evaluator",
            goal=f"Evaluate the ethical dimensions of {self.topic}",
            backstory="A guardian of ethical standards with deep societal impact knowledge.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        logger.info("Agent initialized: ethics_guardian")

        integration_specialist = Agent(
            role="Knowledge Integration Architect",
            goal=f"Synthesize all findings into a master report on {self.topic}",
            backstory="An expert in integrating diverse insights into cohesive outputs.",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
        logger.info("Agent initialized: integration_specialist")

        # Define tasks based on YAML config
        tasks = []
        agent_map = {
            'researcher': researcher,
            'data_analyst': data_analyst,
            'reporting_analyst': reporting_analyst,
            'ethics_guardian': ethics_guardian,
            'integration_specialist': integration_specialist
        }
        for task_name, config in self.tasks_config.items():
            if task_name in self.selected_tasks:
                logger.info(f"Task: {task_name} - Starting for agent: {config['agent']}")
                task_description = config['description'].format(topic=self.topic, current_year=self.current_year)
                task = Task(
                    description=task_description,
                    expected_output=config['expected_output'].format(topic=self.topic, current_year=self.current_year),
                    agent=agent_map[config['agent']],
                    output_file=config.get('output_file')
                )
                tasks.append(task)
                logger.info(f"Task: {task_name} - Initialized with output: {config.get('output_file')}")
            else:
                logger.info(f"Task: {task_name} - Skipped (not in selected tasks)")

        if not tasks:
            logger.warning("No tasks initialized. Check selected_tasks and tasks_config.")
            return False

        # Create and execute the crew
        crew = Crew(
            agents=[researcher, data_analyst, reporting_analyst, ethics_guardian, integration_specialist],
            tasks=tasks,
            verbose=True,
            process="sequential"
        )
        logger.info("Crew initialized with agents and tasks")

        if self.progress_callback:
            self.progress_callback("System", "Starting all tasks", 0)

        results = crew.kickoff()
        logger.info(f"Crew execution completed: {results}")

        if self.progress_callback:
            self.progress_callback("System", "All tasks completed", 100)

        self.generate_master_report(tasks)
        return True

    def generate_master_report(self, tasks):
        output_path = os.path.join(self.base_dir, 'master_report.md')
        topic = self.topic
        current_year = self.current_year

        # Initialize the Markdown content
        md_content = [
            f"# Master Report on {topic}",
            f"**Generated on May 9, 2025**",
            "",
            "## Abstract",
            f"This report synthesizes comprehensive research, data analysis, narrative reporting, and ethical assessments on {topic} as of {current_year}.",
            "",
            "## Introduction",
            f"This report integrates findings on {topic}'s current state and future potential.",
            ""
        ]

        # Collect task outputs efficiently with error handling
        sections = [
            ("Research Findings", "research_brief.md"),
            ("Data Analysis", "data_analysis.md"),
            ("Narrative Report", "report.md"),
            ("Ethical Assessment", "ethics_assessment.md"),
            ("Presentation Summary", "presentation.md")
        ]

        for section_title, output_file in sections:
            file_path = os.path.join(self.base_dir, output_file)
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        md_content.append(f"## {section_title}")
                        md_content.append(content)
                        md_content.append("")
                else:
                    logger.info(f"Section skipped: {section_title} (output file not found: {file_path})")
            except Exception as e:
                logger.error(f"Error reading {file_path}: {str(e)}")
                md_content.append(f"## {section_title} (Error: Content unavailable)")

        # Add a simplified recommendations section
        md_content.extend([
            "## Recommendations",
            "- Address knowledge gaps through targeted research.",
            "- Develop ethical governance structures.",
            "",
            "## Conclusion",
            f"This report provides an overview of {topic}.",
            ""
        ])

        # Write the master report to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(md_content))
            logger.info(f"Generated master_report.md at {output_path}")
        except Exception as e:
            logger.error(f"Failed to write master_report.md: {str(e)}")
            raise