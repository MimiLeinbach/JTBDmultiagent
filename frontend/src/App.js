import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import SearchBar from './components/SearchBar';
import ResultsPanel from './components/ResultsPanel';
import Header from './components/Header';
import Footer from './components/Footer';
import './App.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      console.error('Error fetching results:', err);
      setError('An error occurred while processing your request. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App d-flex flex-column min-vh-100">
      <Header />
      <main className="flex-grow-1">
        <Container fluid className="search-container">
          <Container>
            <Row className="justify-content-center">
              <Col md={8}>
                <h1 className="text-center mb-4">Jobs To Be Done Analysis</h1>
                <SearchBar onSearch={handleSearch} />
              </Col>
            </Row>
          </Container>
        </Container>
        
        <Container className="jtbd-container">
          <ResultsPanel 
            results={results} 
            loading={loading} 
            error={error} 
          />
        </Container>
      </main>
      <Footer />
    </div>
  );
}

export default App; 