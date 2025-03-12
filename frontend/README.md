# JTBD Multi-Agent System Frontend

A React-based frontend for the JTBD (Jobs To Be Done) Multi-Agent System.

## Overview

This frontend application provides a user-friendly interface for interacting with the JTBD Multi-Agent System API. Users can submit queries about various topics to analyze user needs through the Jobs To Be Done framework.

## Features

- Search interface for submitting JTBD queries
- Display of themes and jobs identified from research data
- Visualization of functional, social, and emotional jobs
- Research plan presentation when data is insufficient

## Getting Started

### Prerequisites

- Node.js 14.x or higher
- npm 6.x or higher
- The JTBD Multi-Agent System API running (Python backend)

### Installation

1. Install dependencies:
   ```
   npm install
   ```

2. Start the development server:
   ```
   npm start
   ```

3. Build for production:
   ```
   npm run build
   ```

## Usage

1. Ensure the Python backend API is running on port 8000 (`python api.py`)
2. Start the React frontend on port 3000 (`npm start`)
3. Navigate to http://localhost:3000 in your browser
4. Enter a query like "What are the jobs to be done for online grocery shopping?"
5. View the analysis results or research plan

## Project Structure

- `src/components/`: React components
  - `Header.js`: Application header
  - `SearchBar.js`: Search interface
  - `ResultsPanel.js`: Main results container
  - `ThemeSection.js`: Theme cluster visualization
  - `JobsSection.js`: Job categorization by type
  - `ResearchPlan.js`: Research plan recommendations
- `src/App.js`: Main application component
- `src/index.js`: Application entry point

## Notes

- The frontend is configured to proxy API requests to http://localhost:8000
- Make sure the Python backend is running before using the frontend
- Example queries are provided for topics with sample data 