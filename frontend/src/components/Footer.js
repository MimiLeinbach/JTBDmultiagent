import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Footer = () => {
  return (
    <footer className="bg-dark text-light py-4 mt-5">
      <Container>
        <Row>
          <Col md={6} className="text-center text-md-start">
            <h5>JTBD Multi-Agent System</h5>
            <p className="text-muted">
              A system to analyze user needs through the Jobs To Be Done framework.
            </p>
          </Col>
          <Col md={6} className="text-center text-md-end">
            <p className="mb-0 text-muted">
              &copy; {new Date().getFullYear()} JTBD Multi-Agent System
            </p>
            <p className="text-muted">
              Powered by Python and React
            </p>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer; 