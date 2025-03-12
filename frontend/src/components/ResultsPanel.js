import React from 'react';
import { Spinner, Alert, Row, Col, Card, Badge, ListGroup, Tabs, Tab } from 'react-bootstrap';
import ThemeSection from './ThemeSection';
import JobsSection from './JobsSection';
import ResearchPlan from './ResearchPlan';

const ResultsPanel = ({ results, loading, error }) => {
  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" role="status" variant="primary" className="loading-spinner">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Analyzing Jobs To Be Done...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="danger" className="mt-4">
        <Alert.Heading>Error</Alert.Heading>
        <p>{error}</p>
      </Alert>
    );
  }

  if (!results) {
    return (
      <div className="text-center mt-5">
        <Card className="p-4 shadow-sm">
          <Card.Body>
            <Card.Title>Welcome to the JTBD Multi-Agent System</Card.Title>
            <Card.Text>
              Enter a query above to analyze user needs through the Jobs To Be Done framework.
            </Card.Text>
          </Card.Body>
        </Card>
      </div>
    );
  }

  // Check if the result has research suggestions only
  if (!results.jtbd_analysis && results.research_goals) {
    return <ResearchPlan researchPlan={results} topic={results.topic} />;
  }

  // Check if the result has both jtbd_analysis and research_suggestions
  if (results.jtbd_analysis && results.research_suggestions) {
    // This is a partial analysis with research suggestions
    return (
      <div>
        <h2 className="mb-4">
          Analysis for: {results.jtbd_analysis.topic}
          <Badge 
            bg="warning" 
            text="dark" 
            className="ms-2 reliability-badge"
          >
            Partial Analysis
          </Badge>
        </h2>
        
        <Alert variant="info">
          <Alert.Heading>Limited Data Available</Alert.Heading>
          <p>{results.note}</p>
        </Alert>
        
        <Tabs defaultActiveKey="analysis" id="results-tabs" className="mb-4">
          <Tab eventKey="analysis" title="JTBD Analysis">
            <ThemeSection themes={results.jtbd_analysis.themes} />
            <JobsSection 
              functionalJobs={results.jtbd_analysis.functional_jobs}
              socialJobs={results.jtbd_analysis.social_jobs}
              emotionalJobs={results.jtbd_analysis.emotional_jobs}
            />
          </Tab>
          <Tab eventKey="research" title="Research Suggestions">
            <ResearchPlan researchPlan={results.research_suggestions} topic={results.jtbd_analysis.topic} />
          </Tab>
        </Tabs>
      </div>
    );
  }

  // This is a full analysis
  return (
    <div>
      <h2 className="mb-4">
        Analysis for: {results.topic}
        <Badge 
          bg="success" 
          className="ms-2 reliability-badge"
        >
          Complete Analysis
        </Badge>
      </h2>
      
      <ThemeSection themes={results.themes} />
      <JobsSection 
        functionalJobs={results.functional_jobs}
        socialJobs={results.social_jobs}
        emotionalJobs={results.emotional_jobs}
      />
    </div>
  );
};

export default ResultsPanel; 