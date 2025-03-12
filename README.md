# JTBD Multi-Agent System

A multi-agent system designed to analyze user needs through the Jobs to Be Done (JTBD) framework.
<img width="494" alt="image" src="https://github.com/user-attachments/assets/cd533466-7b8d-4be4-a1a5-1e0a38451a22" />
<img width="456" alt="image" src="https://github.com/user-attachments/assets/e3c5c291-2672-4f2e-9484-22730f91f8e1" />



## Overview

This system processes user inquiries about specific topics and analyzes research data to identify functional, social, and emotional jobs according to the JTBD framework.

### Agent Architecture

1. **Triage Agent**: Processes user questions and routes them to the appropriate agent
2. **JTBD Agent**: Analyzes complete or partial datasets to identify jobs-to-be-done
3. **Researcher Agent**: Provides research plans when data is insufficient

### Data Processing Flow

- User inputs a question/topic
- Triage Agent assesses the request and checks available data
- Based on data completeness (Complete/Partial/None), the request is routed to the appropriate agent
- The system returns insights or research suggestions based on available data

## Features

- Analysis of unstructured research data
- Identification of functional, social, and emotional jobs
- Theme clustering and ranking
- Data sufficiency assessment
- Research plan generation for insufficient data

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys (if needed)
4. Run the application: `python main.py`

## Project Structure

- `main.py`: Entry point for the application
- `agents/`: Contains agent implementation files
  - `triage_agent.py`: Routes user questions
  - `jtbd_agent.py`: Analyzes data for JTBD insights
  - `researcher_agent.py`: Generates research plans
- `data/`: Contains test research data
- `utils/`: Utility functions and helpers
- `services/`: Core services for data processing 
