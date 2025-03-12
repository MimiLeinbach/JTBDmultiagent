import React, { useState } from 'react';
import { Card, ListGroup, Badge, Row, Col, Accordion, Button } from 'react-bootstrap';

const ResearchPlan = ({ researchPlan, topic }) => {
  const [showAllQuestions, setShowAllQuestions] = useState(false);

  if (!researchPlan) {
    return null;
  }

  // Function to render research methods with priority
  const renderResearchMethods = (methods) => {
    if (!methods || methods.length === 0) {
      return <p>No research methods recommended.</p>;
    }

    return (
      <Row>
        {methods.map((method, index) => (
          <Col md={6} key={index}>
            <Card className="method-card">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-start">
                  <Card.Title>{method.method}</Card.Title>
                  <Badge 
                    bg={
                      method.priority === 'High' 
                        ? 'danger' 
                        : method.priority === 'Medium' 
                          ? 'warning' 
                          : 'secondary'
                    }
                  >
                    {method.priority} Priority
                  </Badge>
                </div>
                <Card.Text>{method.description}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    );
  };

  // Function to render sample size recommendations
  const renderSampleSizes = (sampleSizes) => {
    if (!sampleSizes) {
      return <p>No sample size recommendations available.</p>;
    }

    return (
      <ListGroup variant="flush">
        {Object.entries(sampleSizes).map(([method, details], index) => (
          <ListGroup.Item key={index}>
            <h6 className="mb-2 text-capitalize">{method}</h6>
            <div className="d-flex justify-content-between">
              <span>Minimum: <Badge bg="secondary">{details.min}</Badge></span>
              <span>Ideal: <Badge bg="primary">{details.ideal}</Badge></span>
            </div>
            <div className="text-muted small mt-2">{details.justification}</div>
          </ListGroup.Item>
        ))}
      </ListGroup>
    );
  };

  return (
    <div className="research-plan">
      <h2 className="mb-4">
        Research Plan for: {topic || researchPlan.topic}
      </h2>
      
      <Card className="mb-4">
        <Card.Body>
          <Card.Title>Research Goals</Card.Title>
          <ListGroup variant="flush">
            {researchPlan.research_goals?.map((goal, index) => (
              <ListGroup.Item key={index}>{goal}</ListGroup.Item>
            ))}
          </ListGroup>
        </Card.Body>
      </Card>
      
      <Row className="mb-4">
        <Col md={12}>
          <h3 className="research-heading">Recommended Research Methods</h3>
          {renderResearchMethods(researchPlan.recommended_methods)}
        </Col>
      </Row>
      
      <Row className="mb-4">
        <Col md={12}>
          <Card>
            <Card.Body>
              <Card.Title>Sample Size Recommendations</Card.Title>
              {renderSampleSizes(researchPlan.sample_size_recommendations)}
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      <Accordion defaultActiveKey="0" className="mb-4">
        <Accordion.Item eventKey="0">
          <Accordion.Header>Interview Questions ({researchPlan.interview_questions?.length || 0})</Accordion.Header>
          <Accordion.Body>
            <ListGroup variant="flush">
              {researchPlan.interview_questions?.slice(0, showAllQuestions ? undefined : 5).map((question, index) => (
                <ListGroup.Item key={index}>{question}</ListGroup.Item>
              ))}
            </ListGroup>
            {!showAllQuestions && researchPlan.interview_questions?.length > 5 && (
              <Button 
                variant="link" 
                onClick={() => setShowAllQuestions(true)}
                className="mt-2"
              >
                Show all {researchPlan.interview_questions.length} questions
              </Button>
            )}
          </Accordion.Body>
        </Accordion.Item>
        <Accordion.Item eventKey="1">
          <Accordion.Header>Survey Questions ({researchPlan.survey_questions?.length || 0})</Accordion.Header>
          <Accordion.Body>
            <ListGroup variant="flush">
              {researchPlan.survey_questions?.slice(0, 5).map((question, index) => (
                <ListGroup.Item key={index}>
                  <div className="mb-1">{question.question}</div>
                  <Badge bg="info">{question.type}</Badge>
                  {question.options && (
                    <div className="mt-2 small text-muted">
                      Options: {question.options.join(", ")}
                    </div>
                  )}
                </ListGroup.Item>
              ))}
              {researchPlan.survey_questions?.length > 5 && (
                <ListGroup.Item className="text-center text-muted">
                  + {researchPlan.survey_questions.length - 5} more survey questions available
                </ListGroup.Item>
              )}
            </ListGroup>
          </Accordion.Body>
        </Accordion.Item>
      </Accordion>
    </div>
  );
};

export default ResearchPlan; 