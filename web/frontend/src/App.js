import React, { useState } from 'react';
import './App.css';
import SimulatorForm from './components/SimulatorForm';
import ResultsDisplay from './components/ResultsDisplay';
import Header from './components/Header';
import axios from 'axios';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSimulate = async (params) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post('/api/simulate/all', params);
      
      if (response.data.success) {
        setResults(response.data.results);
      } else {
        setError(response.data.error || 'Simulation failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to connect to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />
      
      <div className="main-container">
        <div className="simulator-section">
          <SimulatorForm onSimulate={handleSimulate} loading={loading} />
        </div>

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Running simulations for all 4 protocols...</p>
            <p className="loading-subtext">This may take a moment depending on the number of qubits</p>
          </div>
        )}

        {results && !loading && (
          <ResultsDisplay results={results} />
        )}
      </div>

      <footer className="footer">
        <p>
          Based on research by Erik Åkerberg & Erik Åsgrim (2023) - 
          KTH Royal Institute of Technology
        </p>
      </footer>
    </div>
  );
}

export default App;
