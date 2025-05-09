import os
import yaml
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import time
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

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
            raise ValueError("OPENROUTER_API_KEY or GROK_API_KEY must be set in .env")

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
                verbose=True,  # Ensures detailed logging of agent actions
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
            verbose=2  # Increased verbosity for detailed execution logs
        )
        logger.info("Successfully initialized Crew with agents and tasks")

        # Wrap execution to include progress updates
        def wrapped_execute(crew_instance, *args, **kwargs):
            logger.info("Starting crew execution")
            start_time = time.time()

            # Use crew.kickoff() to execute all tasks
            if self.progress_callback:
                self.progress_callback("System", "Starting all tasks", 0)
            result = crew_instance.kickoff()
            if self.progress_callback:
                self.progress_callback("System", "All tasks completed", 100)

            logger.info(f"Crew execution completed with result: {result}")
            logger.info(f"Crew execution completed in {time.time() - start_time:.2f} seconds")

            # Generate master_report.pdf if master_report_task is selected
            if 'master_report_task' in selected_tasks:
                self.generate_master_pdf(tasks)
            return True

        return crew, wrapped_execute

    def execute_crew(self, crew_instance, execute_func, *args, **kwargs):
        return execute_func(crew_instance, *args, **kwargs)

    def generate_master_pdf(self, tasks):
        output_dir = os.path.join(self.base_dir, 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'master_report.pdf')

        # Set up styles for the PDF
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading1']
        subheading_style = styles['Heading2']
        normal_style = styles['Normal']
        normal_style.leading = 14  # Line spacing

        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        elements = []

        # Title
        elements.append(Paragraph(f"Master Report on {os.environ.get('TOPIC', 'Default Topic')}", title_style))
        elements.append(Paragraph("Integration Specialist", normal_style))
        elements.append(Paragraph("May 9, 2025", normal_style))
        elements.append(Spacer(1, 12))

        # Abstract
        elements.append(Paragraph("Abstract", heading_style))
        abstract_text = (
            f"This report synthesizes comprehensive research, data analysis, narrative reporting, and ethical "
            f"assessments on {os.environ.get('TOPIC', 'Default Topic')} as of {os.environ.get('CURRENT_YEAR', '2025')}. "
            f"It integrates key insights into a cohesive narrative, highlighting technological advancements, "
            f"data-driven trends, stakeholder implications, and ethical considerations. Strategic recommendations "
            f"are provided to guide future developments, supported by tables and visualizations."
        )
        elements.append(Paragraph(abstract_text, normal_style))
        elements.append(Spacer(1, 12))

        # Introduction
        elements.append(Paragraph("Introduction", heading_style))
        intro_text = (
            f"Integrating findings from multiple perspectives, this report addresses "
            f"{os.environ.get('TOPIC', 'Default Topic')}'s current state and future potential."
        )
        elements.append(Paragraph(intro_text, normal_style))
        elements.append(Spacer(1, 12))

        # Batch read content from relevant task outputs
        content = []
        file_paths = []
        for task in tasks:
            if task.output_file in ['research_brief.md', 'data_analysis.md', 'report.md', 'ethics_assessment.md', 'master_report.md']:
                file_path = os.path.join(self.base_dir, task.output_file)
                if os.path.exists(file_path):
                    file_paths.append(file_path)
                else:
                    logger.warning(f"Output file not found: {file_path}")

        # Batch read files
        with ThreadPoolExecutor() as executor:
            content = list(executor.map(lambda fp: open(fp, 'r', encoding='utf-8').read(), file_paths))

        # Add sections
        section_titles = ["Research Findings", "Data Analysis", "Narrative Report", "Ethical Assessment", "Synthesis and Recommendations"]
        for section, content in zip(section_titles, content):
            elements.append(Paragraph(section, heading_style))
            lines = content.split('\n')
            in_table = False
            table_data = []
            for line in lines:
                line = line.strip()
                if line.startswith('# '):
                    if in_table:
                        self._add_table(elements, table_data)
                        in_table = False
                        table_data = []
                    elements.append(Paragraph(line[2:], subheading_style))
                elif line.startswith('|'):
                    if not in_table:
                        in_table = True
                    table_data.append(line)
                elif line and not in_table:
                    if "figure" in line.lower() or "visualization" in line.lower():
                        elements.append(Paragraph(f"[Placeholder for figure: {line}]", normal_style))
                        elements.append(Paragraph(f"Caption: Conceptual visualization of {line.split()[0]}", normal_style))
                    else:
                        elements.append(Paragraph(line, normal_style))
            if in_table:
                self._add_table(elements, table_data)
            elements.append(Spacer(1, 12))

        # Appendix
        elements.append(Paragraph("Supplementary Information", heading_style))
        elements.append(Paragraph("Additional details are available upon request.", normal_style))
        elements.append(Spacer(1, 12))

        # Build PDF
        try:
            doc.build(elements)
            logger.info(f"Generated master_report.pdf in {output_dir}")
        except Exception as e:
            logger.error(f"Failed to generate PDF with reportlab: {str(e)}")
            raise

    def _add_table(self, elements, table_lines):
        if not table_lines or not any('|' in line for line in table_lines):
            return
        # Parse table data
        headers = table_lines[0].split('|')[1:-1]
        headers = [h.strip() for h in headers]
        data = [headers]
        for line in table_lines[2:]:
            if '|' in line:
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                data.append(cells)
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)