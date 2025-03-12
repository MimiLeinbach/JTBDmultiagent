import React, { useState } from 'react';
import { Row, Col, Card, Badge, Button, Collapse, ListGroup } from 'react-bootstrap';

const ThemeSection = ({ themes }) => {
  const [openThemes, setOpenThemes] = useState({});

  const toggleTheme = (themeIndex) => {
    setOpenThemes({
      ...openThemes,
      [themeIndex]: !openThemes[themeIndex]
    });
  };

  if (!themes || themes.length === 0) {
    return (
      <Card className="mb-4">
        <Card.Body>
          <Card.Title>No Themes Found</Card.Title>
          <Card.Text>No theme clusters were identified in the available data.</Card.Text>
        </Card.Body>
      </Card>
    );
  }

  return (
    <div className="mb-5">
      <h3 className="mb-4 theme-heading">Theme Clusters</h3>
      <Row>
        {themes.map((theme, index) => (
          <Col md={6} key={index}>
            <Card className="theme-card mb-4">
              <Card.Header className="d-flex justify-content-between align-items-center">
                <h5 className="mb-0">{theme.name}</h5>
                <Badge bg="primary" pill>
                  {theme.job_count} jobs
                </Badge>
              </Card.Header>
              <Card.Body>
                <Card.Text>{theme.description}</Card.Text>
                <Button 
                  variant="outline-primary" 
                  size="sm" 
                  onClick={() => toggleTheme(index)}
                  aria-controls={`theme-jobs-${index}`}
                  aria-expanded={!!openThemes[index]}
                >
                  {openThemes[index] ? 'Hide Jobs' : 'Show Jobs'}
                </Button>
                <Collapse in={!!openThemes[index]}>
                  <div id={`theme-jobs-${index}`} className="mt-3">
                    <ListGroup variant="flush">
                      {theme.jobs?.slice(0, 5).map((job, jobIndex) => (
                        <ListGroup.Item key={jobIndex} className={`${job.type}-job`}>
                          <div className="d-flex justify-content-between">
                            <div>
                              "{job.statement}"
                              <Badge 
                                bg={job.type === 'functional' ? 'success' : job.type === 'social' ? 'purple' : 'primary'}
                                className="ms-2"
                              >
                                {job.type}
                              </Badge>
                            </div>
                            <Badge bg="secondary" pill>
                              {job.frequency}×
                            </Badge>
                          </div>
                          <div className="text-muted small mt-1">Source: {job.source}</div>
                        </ListGroup.Item>
                      ))}
                      {theme.jobs?.length > 5 && (
                        <ListGroup.Item className="text-center text-muted">
                          + {theme.jobs.length - 5} more jobs in this theme
                        </ListGroup.Item>
                      )}
                    </ListGroup>
                  </div>
                </Collapse>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default ThemeSection; 