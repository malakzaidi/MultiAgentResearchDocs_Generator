import os
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from typing import List
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class MultiAgentDocsCrew:
    """MultiAgentDocs Crew for Comprehensive Document Generation"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Agent(
            role=f"{topic} Senior Research Intelligence Specialist",
            goal=f"Uncover cutting-edge developments, evaluate evidence quality, and synthesize cross-disciplinary insights in {topic}",
            backstory=(
                f"You're a world-class researcher with 15+ years of experience in {topic} and related fields. "
                "Your methodical approach combines academic rigor with practical insight. Known for identifying emerging trends "
                "before they become mainstream, your research has influenced both academic discourse and industry innovation. "
                "You have a talent for distinguishing between hype and genuine breakthroughs."
            ),
            capabilities=[
                "Deep literature analysis across multiple databases and repositories",
                "Evaluation of methodological soundness and evidence quality",
                "Identification of cross-disciplinary connections and implications",
                "Recognition of historical patterns and future trajectories",
                "Critical assessment of claims against established knowledge"
            ],
            verbose=True
        )

    @agent
    def data_analyst(self) -> Agent:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Agent(
            role=f"{topic} Quantitative Intelligence Analyst",
            goal=f"Transform research insights into structured data, statistical analyses, and compelling visualizations",
            backstory=(
                f"With expertise in both data science and {topic}, you bridge the gap between raw information and actionable intelligence. "
                f"Your background combines advanced statistical methods with domain expertise, allowing you to create meaningful metrics "
                "and visualizations that reveal hidden patterns. Your analyses have guided strategic decisions in both research institutions "
                "and industry leaders."
            ),
            capabilities=[
                "Creation of structured datasets from qualitative research",
                "Development of custom metrics and indices for tracking progress",
                "Design of informative visualizations and dashboards",
                "Performance of statistical analyses to validate trends",
                "Identification of correlations, causations, and outliers"
            ],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Agent(
            role=f"{topic} Strategic Communication Specialist",
            goal=f"Transform complex research and data into clear, compelling, and actionable reports for diverse audiences",
            backstory=(
                f"You're renowned for your ability to translate technical complexity into strategic clarity. With experience communicating "
                f"to both technical experts and executive decision-makers, you know exactly how to structure information for maximum impact. "
                f"Your reports have informed policy changes, research directions, and investment decisions across multiple sectors related to {topic}."
            ),
            capabilities=[
                "Crafting narrative structures that connect diverse findings",
                "Adapting technical content for different knowledge levels",
                "Balancing depth with accessibility in specialized topics",
                "Creating professional document formats optimized for different uses",
                "Highlighting actionable insights and strategic implications"
            ],
            verbose=True
        )

    @agent
    def ethics_guardian(self) -> Agent:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Agent(
            role=f"{topic} Ethics and Impact Evaluator",
            goal=f"Assess the ethical implications, societal impacts, and potential misuse scenarios of developments in {topic}",
            backstory=(
                f"With a background spanning technology ethics, public policy, and {topic}, you provide a crucial perspective on how innovations "
                f"might affect diverse stakeholders. Your evaluations have prevented harmful applications while promoting responsible innovation. "
                f"You're known for your balanced approach that considers both benefits and risks across multiple timeframes and social contexts."
            ),
            capabilities=[
                "Identification of ethical concerns in research and applications",
                "Assessment of differential impacts across diverse populations",
                "Analysis of potential misuse scenarios and safeguards",
                "Evaluation of long-term societal implications",
                "Recommendation of responsible governance approaches"
            ],
            verbose=True
        )

    @agent
    def integration_specialist(self) -> Agent:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Agent(
            role=f"{topic} Knowledge Integration Architect",
            goal=f"Synthesize outputs from all agents into cohesive, multi-format deliverables that maximize value and impact",
            backstory=(
                f"You excel at seeing the big picture while managing complex details. Your background spans project management, systems thinking, "
                f"and {topic}, enabling you to create integrated knowledge products across multiple formats (documents, presentations, data specifications, "
                "and templates). You've orchestrated major interdisciplinary initiatives that bridge research, application, and policy, ensuring deliverables "
                "meet diverse stakeholder needs."
            ),
            capabilities=[
                "Harmonizing diverse information sources into unified deliverables",
                "Creating structured outputs in multiple formats (Markdown, JSON, Excel)",
                "Identifying gaps and inconsistencies across different analyses",
                "Ensuring logical flow and narrative coherence",
                "Optimizing final outputs for specific stakeholder needs"
            ],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        topic = os.environ.get('TOPIC', 'the specified topic')
        year = os.environ.get('CURRENT_YEAR', '2025')
        return Task(
            name='task-research',
            description=f"Conduct comprehensive research on {topic}, leveraging academic databases, industry reports, and web sources as of {year}.",
            expected_output=(
                "Comprehensive research brief in Markdown format including:\n"
                "1. A curated list of 15 substantive insights about {topic}\n"
                "2. For each insight: headline, detailed explanation (200-300 words), evidence quality assessment, and credible sources (APA format)\n"
                "3. A detailed knowledge graph (in DOT format) mapping connections between insights, stakeholders, and trends\n"
                "4. A timeline of major developments from 2020 to {year}, with annotations for pivotal events\n"
                "5. Identification of 5-7 critical knowledge gaps with suggested research directions\n"
                "6. A summary of cross-disciplinary implications (e.g., economic, social, technological)"
            ),
            agent=self.researcher(),
            output_file="research_brief.md"
        )

    @task
    def data_analysis_task(self) -> Task:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Task(
            name='task-data',
            description=f"Develop a quantitative analysis framework for {topic} based on research findings, using statistical methods and visualization tools.",
            expected_output=(
                "Data analysis package in Markdown format including:\n"
                "1. A structured data schema (JSON format) defining key variables, relationships, and metadata\n"
                "2. 7-10 visualization concepts (e.g., heatmaps, network graphs) with mockups and strategic rationale\n"
                "3. Statistical analysis results highlighting significant patterns (e.g., correlations, trends) with p-values and confidence intervals\n"
                "4. A comparative framework for evaluating {topic} approaches or technologies, with weighted criteria\n"
                "5. Custom metrics and indices for tracking {topic} progress over time\n"
                "6. A dashboard specification (JSON format) with interactive elements and KPI definitions\n"
                "7. Recommendations for data collection improvements"
            ),
            agent=self.data_analyst(),
            output_file="data_analysis.md"
        )

    @task
    def reporting_task(self) -> Task:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Task(
            name='task-report',
            description=f"Transform research and data findings into a professional report on {topic} tailored for diverse stakeholders.",
            expected_output=(
                "Professional report in Markdown format including:\n"
                "1. Executive summary (300-500 words) synthesizing key findings and recommendations\n"
                "2. Introduction establishing context and relevance of {topic}\n"
                "3. 12-15 sections covering insights, evidence, visualizations, and strategic implications\n"
                "4. Future outlook section projecting trends for the next 5-10 years\n"
                "5. 5-7 actionable strategic recommendations for stakeholders (e.g., policymakers, industry leaders)\n"
                "6. Reference section with APA-formatted citations\n"
                "7. Appendix with supplementary data, charts, and methodology details"
            ),
            agent=self.reporting_analyst(),
            output_file="report.md"
        )

    @task
    def ethics_assessment_task(self) -> Task:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Task(
            name='task-ethics',
            description=f"Evaluate the ethical dimensions, societal impacts, and potential misuse scenarios of developments in {topic}.",
            expected_output=(
                "Ethical impact assessment in Markdown format including:\n"
                "1. A detailed impact matrix (table format) outlining benefits and risks across stakeholder groups\n"
                "2. 7-10 key ethical considerations with in-depth analysis (150-200 words each)\n"
                "3. Analysis of 3-5 potential misuse scenarios with proposed safeguards\n"
                "4. Recommendations for responsible governance frameworks, including regulatory and voluntary measures\n"
                "5. A framework for ongoing ethical evaluation with measurable indicators\n"
                "6. Assessment of long-term societal implications (10-20 years)"
            ),
            agent=self.ethics_guardian(),
            output_file="ethics_assessment.md"
        )

    @task
    def master_report_task(self) -> Task:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Task(
            name='task-master',
            description=(
                f"Synthesize outputs from all previous tasks into a cohesive master document about {topic}, harmonizing research, data, reporting, and ethics insights."
            ),
            expected_output=(
                "Master document in Markdown format including:\n"
                "1. Executive summary (500-750 words) synthesizing key findings across all tasks\n"
                "2. Integrated sections covering technical advancements, societal impacts, ethical considerations, and knowledge gaps\n"
                "3. 7-10 strategic recommendations tailored to diverse stakeholders (e.g., academia, industry, government)\n"
                "4. A consolidated reference section with APA-formatted citations\n"
                "5. Visual summaries (e.g., infographics, charts) embedded as image references\n"
                "6. A stakeholder impact map highlighting key beneficiaries and risks"
            ),
            agent=self.integration_specialist(),
            output_file="master_report.md"
        )

    @task
    def presentation_task(self) -> Task:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Task(
            name='task-presentation',
            description=(
                f"Create presentation-ready slides based on all previous task outputs about {topic}, designed for high-impact delivery."
            ),
            expected_output=(
                "Presentation document in Markdown format including:\n"
                "1. Title slide with {topic} context and key objectives\n"
                "2. 7-10 slides covering critical insights, trends, ethical considerations, and recommendations\n"
                "3. Visual elements (e.g., charts, graphs, infographics) described with placeholder image references\n"
                "4. Closing slide with a compelling call to action for stakeholders\n"
                "5. Notes section for each slide with talking points (50-100 words per slide)"
            ),
            agent=self.integration_specialist(),
            output_file="presentation.md"
        )

    @task
    def dashboard_spec_task(self) -> Task:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Task(
            name='task-dashboard',
            description=(
                f"Design an interactive dashboard specification for {topic} based on all previous task outputs, enabling dynamic data exploration."
            ),
            expected_output=(
                "JSON specification for an interactive dashboard including:\n"
                "1. Overview panel with 5-7 key performance indicators (KPIs) relevant to {topic}\n"
                "2. Visualization definitions (e.g., line graphs, heatmaps, network diagrams) with data mappings\n"
                "3. Filter options (e.g., year, region, subtopic) with interactive controls\n"
                "4. Data schema references linking to the data analysis task output\n"
                "5. User interaction flows (e.g., drill-down, hover effects)\n"
                "6. Accessibility considerations (e.g., colorblind-friendly palettes)"
            ),
            agent=self.integration_specialist(),
            output_file="dashboard_spec.json"
        )

    @task
    def tracking_template_task(self) -> Task:
        topic = os.environ.get('TOPIC', 'the specified topic')
        return Task(
            name='task-template',
            description=(
                f"Create a document template for ongoing tracking of {topic} developments based on all previous task outputs."
            ),
            expected_output=(
                "Excel template (CSV format for compatibility) including:\n"
                "1. Columns for phase, objective, KPIs, owner, status, and timeline\n"
                "2. 10-15 pre-populated rows based on current findings and recommendations\n"
                "3. Notes section with instructions for updating and maintaining the template\n"
                "4. A metadata sheet defining KPI calculations and data sources\n"
                "5. Conditional formatting rules for status tracking"
            ),
            agent=self.integration_specialist(),
            output_file="tracking_template.csv"
        )

    @crew
    def crew(self) -> Crew:
        all_tasks = [
            self.research_task(),
            self.data_analysis_task(),
            self.reporting_task(),
            self.ethics_assessment_task(),
            self.master_report_task(),
            self.presentation_task(),
            self.dashboard_spec_task(),
            self.tracking_template_task()
        ]
        # Filter tasks based on SELECTED_TASKS environment variable
        selected_task_ids = os.environ.get('SELECTED_TASKS', '').split(',')
        if selected_task_ids and selected_task_ids[0]:
            tasks = [task for task in all_tasks if task.name in selected_task_ids]
            # Ensure dependencies for master, presentation, dashboard, and template tasks
            if any(t in selected_task_ids for t in ['task-master', 'task-presentation', 'task-dashboard', 'task-template']):
                tasks.extend([t for t in all_tasks if t.name in ['task-research', 'task-data', 'task-report', 'task-ethics'] and t not in tasks])
        else:
            tasks = all_tasks

        return Crew(
            agents=[
                self.researcher(),
                self.data_analyst(),
                self.reporting_analyst(),
                self.ethics_guardian(),
                self.integration_specialist()
            ],
            tasks=tasks,
            process=Process.sequential  # Sequential to respect task dependencies
        )