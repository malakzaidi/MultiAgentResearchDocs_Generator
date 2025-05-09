from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any, Optional
from datetime import datetime


@CrewBase
class FinancialAnomalyDetectionCrew():
    """Multi-Agent Financial Market Anomaly Detection System"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self, config: Optional[Dict[str, Any]] = None, output_file: Optional[str] = None):
        """Initialize the crew with a configuration"""
        self.user_config = config or {}
        self.output_filename = output_file or "comprehensive_financial_anomaly_report.md"
        super().__init__()

    @agent
    def data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['data_collector'],
            verbose=True
        )

    @agent
    def pattern_recognizer(self) -> Agent:
        return Agent(
            config=self.agents_config['pattern_recognizer'],
            verbose=True
        )

    @agent
    def sentiment_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['sentiment_analyzer'],
            verbose=True
        )

    @agent
    def forensic_investigator(self) -> Agent:
        return Agent(
            config=self.agents_config['forensic_investigator'],
            verbose=True
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )

    @agent
    def coordination_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['coordination_manager'],
            verbose=True
        )

    @task
    def collect_data_task(self) -> Task:
        task_config = dict(self.tasks_config['collect_data_task'])

        # Enhance task description with user configuration for data collection
        if self.user_config:
            data_collection_details = []
            if 'market_focus' in self.user_config:
                data_collection_details.append(f"Focus on {self.user_config['market_focus']} data")
            if 'region_focus' in self.user_config:
                region = self.user_config['region_focus']
                if 'country_focus' in self.user_config and self.user_config['country_focus']:
                    region += f" with special emphasis on {self.user_config['country_focus']}"
                data_collection_details.append(f"Collect data from {region}")
            if 'sector_focus' in self.user_config and self.user_config['sector_focus'] != "All Sectors":
                data_collection_details.append(f"Prioritize {self.user_config['sector_focus']} sector")
            if 'timeframe' in self.user_config:
                timeframe = self.user_config['timeframe']
                if timeframe == "Custom Period" and 'custom_start_date' in self.user_config:
                    timeframe = f"from {self.user_config['custom_start_date']} to {self.user_config['custom_end_date']}"
                data_collection_details.append(f"Data timeframe: {timeframe}")

            enhanced_description = task_config.get('description', '') + "\n\nData collection parameters: " + \
                                   "; ".join(data_collection_details)

            task_config['description'] = enhanced_description

        return Task(
            config=task_config
        )

    @task
    def detect_patterns_task(self) -> Task:
        return Task(
            config=self.tasks_config['detect_patterns_task']
        )

    @task
    def analyze_sentiment_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_sentiment_task']
        )

    @task
    def investigate_anomalies_task(self) -> Task:
        return Task(
            config=self.tasks_config['investigate_anomalies_task']
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )

    @task
    def reporting_task(self) -> Task:
        task_config = dict(self.tasks_config['reporting_task'])

        # Enhance task description with user configuration
        if self.user_config:
            config_details = []
            if 'market_focus' in self.user_config:
                config_details.append(f"Market focus: {self.user_config['market_focus']}")
            if 'region_focus' in self.user_config:
                region = self.user_config['region_focus']
                if 'country_focus' in self.user_config and self.user_config['country_focus']:
                    region += f" ({self.user_config['country_focus']})"
                config_details.append(f"Region focus: {region}")
            if 'sector_focus' in self.user_config:
                config_details.append(f"Sector focus: {self.user_config['sector_focus']}")
            if 'analysis_focus' in self.user_config:
                config_details.append(f"Analysis focus: {self.user_config['analysis_focus']}")
            if 'timeframe' in self.user_config:
                config_details.append(f"Timeframe: {self.user_config['timeframe']}")
            if 'analysis_purpose' in self.user_config:
                config_details.append(f"Purpose: {self.user_config['analysis_purpose']}")
            if 'output_format' in self.user_config:
                config_details.append(f"Format style: {self.user_config['output_format']}")

            enhanced_description = task_config.get('description', '') + "\n\nUser configuration: " + \
                                   "; ".join(config_details)
            if 'additional_notes' in self.user_config and self.user_config['additional_notes']:
                enhanced_description += f"\n\nAdditional instructions: {self.user_config['additional_notes']}"

            task_config['description'] = enhanced_description

        return Task(
            config=task_config,
            output_file=self.output_filename
        )

    @task
    def coordination_task(self) -> Task:
        return Task(
            config=self.tasks_config['coordination_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Financial Anomaly Detection crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # Uncomment below for hierarchical process with coordination_manager as manager
            # process=Process.hierarchical,
            # manager=self.coordination_manager
        )

    @before_kickoff
    def setup(self):
        """Run before the crew starts working"""
        print("🚀 Starting Financial Market Anomaly Detection System")
        print("🔍 Initializing agents and preparing for data collection...")

    @after_kickoff
    def wrap_up(self):
        """Run after the crew completes all tasks"""
        print("✅ Financial Market Anomaly Detection System completed its analysis")
        print("📊 Check the generated report for detailed findings and recommendations")