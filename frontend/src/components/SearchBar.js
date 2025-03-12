import React, { useState } from 'react';
import { Form, InputGroup, Button } from 'react-bootstrap';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  const exampleQueries = [
    'What are the jobs to be done for online grocery shopping?',
    'What are the jobs to be done for fitness tracking apps?',
    'What are the jobs to be done for video conferencing tools?',
    'What are the jobs to be done for project management software?',
    'What are the jobs to be done for meal kit delivery services?'
  ];

  const handleExampleClick = (example) => {
    setQuery(example);
    onSearch(example);
  };

  return (
    <div>
      <Form onSubmit={handleSubmit}>
        <InputGroup className="mb-3">
          <Form.Control
            type="text"
            placeholder="Enter your JTBD question (e.g., What are the jobs to be done for online grocery shopping?)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            size="lg"
          />
          <Button variant="primary" type="submit" size="lg">
            Analyze
          </Button>
        </InputGroup>
      </Form>
      
      <div className="text-center mt-3 mb-4">
        <p className="text-light">Try one of these examples:</p>
        <div className="d-flex flex-wrap justify-content-center gap-2">
          {exampleQueries.map((example, index) => (
            <Button 
              key={index} 
              variant="outline-light" 
              size="sm" 
              onClick={() => handleExampleClick(example)}
            >
              {example.replace('What are the jobs to be done for ', '')}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SearchBar; 