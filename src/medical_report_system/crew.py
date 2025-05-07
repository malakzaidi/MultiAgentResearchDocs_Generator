from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from typing import List
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class medical_report_system:
    """Medical Report System Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            role="Medical AI Senior Research Intelligence Specialist",
            goal="Uncover cutting-edge developments, evaluate evidence quality, and synthesize cross-disciplinary insights in medical AI",
            backstory=(
                "You're a world-class researcher with 15+ years of experience in medical AI and related fields. "
                "Your methodical approach combines academic rigor with practical insight."
            ),
            verbose=True
        )

    @agent
    def data_analyst(self) -> Agent:
        return Agent(
            role="Medical AI Quantitative Intelligence Analyst",
            goal="Transform research insights into structured data, statistical analyses, and compelling visualizations",
            backstory=(
                "With expertise in both data science and medical AI, you bridge the gap between raw information and actionable intelligence."
            ),
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            role="Medical AI Strategic Communication Specialist",
            goal="Transform complex research and data into clear, compelling, and actionable reports for diverse audiences",
            backstory=(
                "You're renowned for translating technical complexity into strategic clarity for stakeholders in medical AI."
            ),
            verbose=True
        )

    @agent
    def ethics_guardian(self) -> Agent:
        return Agent(
            role="Medical AI Ethics and Impact Evaluator",
            goal="Assess the ethical implications, societal impacts, and potential misuse scenarios of developments in medical AI",
            backstory=(
                "With a background spanning tech ethics and public policy, you provide a crucial perspective on how innovations in medical AI affect stakeholders."
            ),
            verbose=True
        )

    @agent
    def integration_specialist(self) -> Agent:
        return Agent(
            role="Medical AI Knowledge Integration Architect",
            goal="Synthesize outputs from all agents into cohesive, multi-format deliverables that maximize value and impact",
            backstory=(
                "You excel at managing complex details and creating integrated knowledge products across multiple formats (documents, presentations, data specifications, and templates)."
            ),
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            description="Conduct comprehensive research on medical AI, focusing on developments as of 2025.",
            expected_output=(
                "Structured research brief with:\n"
                "1. A list of exactly 12 substantive insights about medical AI\n"
                "2. For each insight: headline, explanation, evidence assessment, sources\n"
                "3. A preliminary knowledge graph identifying connections\n"
                "4. A timeline of major developments (2020-2025)\n"
                "5. Identification of 3-5 knowledge gaps"
            ),
            agent=self.researcher(),
            output_file="research_brief.md"
        )

    @task
    def data_analysis_task(self) -> Task:
        return Task(
            description="Create a quantitative analysis framework for medical AI based on the research findings.",
            expected_output=(
                "Data analysis package including:\n"
                "1. Data schema with key variables and relationships\n"
                "2. 5-7 visualization concepts with strategic value\n"
                "3. Statistical highlights of significant patterns\n"
                "4. Comparative framework for evaluating approaches\n"
                "5. Recommendations for metrics to track\n"
                "6. Dashboard specification"
            ),
            agent=self.data_analyst(),
            output_file="data_analysis.md"
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            description="Transform findings into a professional medical AI report with sections and visual support.",
            expected_output=(
                "Formatted report including:\n"
                "1. Executive summary (250-500 words)\n"
                "2. Introduction establishing context\n"
                "3. 10-12 sections with insights, evidence, visuals, and implications\n"
                "4. Future outlook section\n"
                "5. Strategic recommendations\n"
                "6. Reference section\n"
                "7. Appendix with supplementary information"
            ),
            agent=self.reporting_analyst(),
            output_file="report.md"
        )

    @task
    def ethics_assessment_task(self) -> Task:
        return Task(
            description="Evaluate the ethical dimensions and societal impacts of developments in medical AI.",
            expected_output=(
                "Ethical impact assessment including:\n"
                "1. Impact matrix for benefits and risks\n"
                "2. 5-7 key ethical considerations\n"
                "3. Analysis of misuse scenarios and safeguards\n"
                "4. Recommendations for responsible governance\n"
                "5. Framework for ongoing ethical evaluation"
            ),
            agent=self.ethics_guardian(),
            output_file="ethics_assessment.md"
        )

    @task
    def master_report_task(self) -> Task:
        return Task(
            description=(
                "Synthesize outputs from all previous tasks into a cohesive master document about medical AI. "
                "Harmonize findings from research, data analysis, reporting, and ethics assessment."
            ),
            expected_output=(
                "Master document including:\n"
                "1. Executive summary synthesizing key findings\n"
                "2. Integrated sections covering technical advancements, clinical impacts, ethical considerations, and gaps\n"
                "3. Strategic recommendations for stakeholders\n"
                "4. Reference section with key sources"
            ),
            agent=self.integration_specialist(),
            output_file="master_report.md"
        )

    @task
    def presentation_task(self) -> Task:
        return Task(
            description=(
                "Create presentation-ready slides based on outputs from all previous tasks about medical AI. "
                "Capture core insights in a visually compelling format."
            ),
            expected_output=(
                "Presentation document including:\n"
                "1. Title slide with topic and context\n"
                "2. 5-7 slides covering key insights, trends, and recommendations\n"
                "3. Visual elements (e.g., charts, graphs, infographics)\n"
                "4. Closing slide with call to action"
            ),
            agent=self.integration_specialist(),
            output_file="presentation.md"
        )

    @task
    def dashboard_spec_task(self) -> Task:
        return Task(
            description=(
                "Design an interactive dashboard specification based on outputs from all previous tasks about medical AI. "
                "Enable exploration of data and insights."
            ),
            expected_output=(
                "JSON specification for an interactive dashboard including:\n"
                "1. Overview panel with KPIs\n"
                "2. Visualization definitions (e.g., line graphs, heatmaps)\n"
                "3. Filter options (e.g., year, region, use case)\n"
                "4. Data schema references"
            ),
            agent=self.integration_specialist(),
            output_file="dashboard_spec.json"
        )

    @task
    def tracking_template_task(self) -> Task:
        return Task(
            description=(
                "Create a document template for ongoing tracking of medical AI developments based on outputs from all previous tasks. "
                "Support stakeholder monitoring and updates."
            ),
            expected_output=(
                "Excel template including:\n"
                "1. Columns for phase, objective, KPIs, owner, and status\n"
                "2. Pre-populated rows based on current findings\n"
                "3. Notes for updating and maintaining the template"
            ),
            agent=self.integration_specialist(),
            output_file="tracking_template.xlsx"
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.researcher(),
                self.data_analyst(),
                self.reporting_analyst(),
                self.ethics_guardian(),
                self.integration_specialist()
            ],
            tasks=[
                self.research_task(),
                self.data_analysis_task(),
                self.reporting_task(),
                self.ethics_assessment_task(),
                self.master_report_task(),
                self.presentation_task(),
                self.dashboard_spec_task(),
                self.tracking_template_task()
            ],
            process=Process.sequential  # Sequential to ensure dependencies are respected
        )