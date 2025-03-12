import React from 'react';
import { Card, ListGroup, Badge, Row, Col, Tab, Nav } from 'react-bootstrap';

const JobsSection = ({ functionalJobs, socialJobs, emotionalJobs }) => {
  // Helper function to render a list of jobs
  const renderJobList = (jobs, jobType) => {
    if (!jobs || jobs.length === 0) {
      return (
        <Card className="mb-4">
          <Card.Body>
            <Card.Text>No {jobType} jobs found in the data.</Card.Text>
          </Card.Body>
        </Card>
      );
    }

    return (
      <ListGroup variant="flush">
        {jobs.map((job, index) => (
          <ListGroup.Item key={index} className={`${jobType}-job job-card`}>
            <div className="d-flex justify-content-between">
              <div>
                <div className="mb-1">"{job.statement}"</div>
                <div className="text-muted small">
                  Context: {job.context || 'Not specified'}
                </div>
              </div>
              <Badge bg="secondary" pill className="align-self-start mt-1">
                {job.frequency}×
              </Badge>
            </div>
            <div className="text-muted small mt-1">Source: {job.source}</div>
          </ListGroup.Item>
        ))}
      </ListGroup>
    );
  };

  return (
    <div className="mt-5">
      <h3 className="mb-4 theme-heading">Jobs by Type</h3>
      
      <Tab.Container defaultActiveKey="functional">
        <Row>
          <Col sm={12}>
            <Nav variant="tabs" className="mb-3">
              <Nav.Item>
                <Nav.Link eventKey="functional">
                  Functional Jobs
                  <Badge bg="success" className="ms-2">
                    {functionalJobs?.length || 0}
                  </Badge>
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="social">
                  Social Jobs
                  <Badge bg="purple" className="ms-2">
                    {socialJobs?.length || 0}
                  </Badge>
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="emotional">
                  Emotional Jobs
                  <Badge bg="primary" className="ms-2">
                    {emotionalJobs?.length || 0}
                  </Badge>
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>
          <Col sm={12}>
            <Tab.Content>
              <Tab.Pane eventKey="functional">
                <Card>
                  <Card.Body>
                    <Card.Title>Functional Jobs</Card.Title>
                    <Card.Text>
                      These are the practical tasks that users are trying to accomplish.
                    </Card.Text>
                    {renderJobList(functionalJobs, 'functional')}
                  </Card.Body>
                </Card>
              </Tab.Pane>
              <Tab.Pane eventKey="social">
                <Card>
                  <Card.Body>
                    <Card.Title>Social Jobs</Card.Title>
                    <Card.Text>
                      These relate to how users want to be perceived by others.
                    </Card.Text>
                    {renderJobList(socialJobs, 'social')}
                  </Card.Body>
                </Card>
              </Tab.Pane>
              <Tab.Pane eventKey="emotional">
                <Card>
                  <Card.Body>
                    <Card.Title>Emotional Jobs</Card.Title>
                    <Card.Text>
                      These relate to how users want to feel when using the product or service.
                    </Card.Text>
                    {renderJobList(emotionalJobs, 'emotional')}
                  </Card.Body>
                </Card>
              </Tab.Pane>
            </Tab.Content>
          </Col>
        </Row>
      </Tab.Container>
    </div>
  );
};

export default JobsSection; 