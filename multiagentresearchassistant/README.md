# Multi-Agent Financial Market Anomaly Detection System

A customizable AI-powered system that uses multiple specialized agents to detect, analyze, and report financial market anomalies tailored to your specific needs. This project delivers personalized economic intelligence through comprehensive, actionable reports.

## Project Overview

This system leverages the CrewAI framework to coordinate multiple AI agents, each specialized in different aspects of financial market analysis. The system processes financial data from various sources, identifies anomalies specific to your area of interest, investigates their root causes, and generates a targeted report with actionable recommendations.

## Key Features

- **Customizable analysis**: Select specific markets, regions, sectors, anomaly types, and time periods
- **Multi-agent cooperation**: 7 specialized agents working together to analyze financial markets
- **Comprehensive analysis**: Covers data collection, pattern recognition, sentiment analysis, forensic investigation, and research
- **Actionable insights**: Final report includes practical recommendations tailored to your needs
- **Multiple output formats**: Choose from technical, executive, academic, or regulatory-focused reporting
- **Economic focus**: Designed to identify issues that could impact economic stability and growth
- **Scalable architecture**: Can be extended to cover additional financial markets or data sources

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- OpenRouter API key

### Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install crewai openai python-dotenv
```

3. Create a `.env` file in the project root with your API credentials:

```
MODEL=openrouter/qwen/qwen3-32b:free
OPENROUTER_API_KEY=your_openrouter_api_key
```

### Running the System

#### Interactive Mode (Recommended for First-Time Users)

Execute the main script with no arguments to enter interactive configuration mode:

```bash
python main.py
```

Follow the prompts to select your specific market focus, region, timeframe, and other parameters.

#### Configuration File Mode (For Repeated Analyses)

Create a JSON configuration file (see examples in `config_examples.json`) and run:

```bash
python main.py --config your_config.json
```

#### Default Mode (Quick Start)

To run with default settings (global markets, all sectors, last quarter):

```bash
python main.py --non-interactive
```

The system will generate a report named based on your configuration (e.g., `stock_markets_united_states_valuation_anomalies_anomaly_report.md`).

## System Architecture

### Agents

- **Data Collector**: Gathers financial data from multiple sources
- **Pattern Recognizer**: Identifies unusual patterns and potential anomalies
- **Sentiment Analyzer**: Monitors market sentiment across news and social media
- **Forensic Investigator**: Determines the nature and significance of anomalies
- **Researcher**: Provides contextual information and historical patterns
- **Reporting Analyst**: Creates comprehensive reports with visualizations
- **Coordination Manager**: Orchestrates workflow between all agents

### Process Flow

1. Data collection from multiple sources
2. Pattern recognition to identify anomalies
3. Sentiment analysis to detect market mood disconnects
4. Forensic investigation of detected anomalies
5. Research to provide context and historical precedents
6. Comprehensive report generation with recommendations
7. (Throughout) Process coordination and optimization

## Report Structure

The final report includes:

- Executive summary of findings
- Market environment overview
- Detailed analysis of detected anomalies
- Root cause analysis
- Historical precedents and comparisons
- Economic impact assessment
- Recommended interventions
- Implementation roadmap
- Appendices with detailed methodology and data

## Extending the System

This project can be extended in various ways:

- Add specialized agents for specific market segments
- Implement additional data sources
- Connect to real-time data streams
- Integrate with trading or regulatory systems

## License

[MIT License](LICENSE)

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- OpenRouter for providing access to the Qwen model