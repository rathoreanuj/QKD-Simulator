import React, { useState } from 'react';
import './App.css';
import SimulatorForm from './components/SimulatorForm';
import ResultsDisplay from './components/ResultsDisplay';
import MultipleSimForm from './components/MultipleSimForm';
import MultipleSimResults from './components/MultipleSimResults';
import Header from './components/Header';
import axios from 'axios';

const X_PARAM_LABELS = {
  source_rate:        'Source Rate (MHz)',
  source_efficiency:  'Source Efficiency (%)',
  fiber_length:       'Fiber Length (km)',
  fiber_loss:         'Fiber Loss (dB/km)',
  detector_efficiency:'Detector Efficiency (%)',
  perturb_prob:       'Perturb Probability (%)',
  sop_deviation:      'SOP Deviation (rad)',
  qber_fraction:      'QBER Fraction (%)',
};

const Y_PARAM_LABELS = {
  key_length:           'Key Length',
  key_rate:             'Key Rate (Hz)',
  qber:                 'QBER (%)',
  combined_efficiency:  'Combined Efficiency (%)',
};

function App() {
  const [activeTab, setActiveTab] = useState('single');

  // Single simulation state
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Multiple simulation state
  const [multiResults, setMultiResults] = useState(null);
  const [multiLoading, setMultiLoading] = useState(false);
  const [multiError, setMultiError] = useState(null);
  const [multiLabels, setMultiLabels] = useState({ xLabel: '', yLabel: '' });
  const [multiNPoints, setMultiNPoints] = useState(10);

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

  const handleMultiSimulate = async (params) => {
    setMultiLoading(true);
    setMultiError(null);
    setMultiResults(null);
    setMultiNPoints(params.n_points);
    setMultiLabels({
      xLabel: X_PARAM_LABELS[params.x_param] || params.x_param,
      yLabel: Y_PARAM_LABELS[params.y_param] || params.y_param,
    });

    try {
      const response = await axios.post('/api/simulate/multi', params);
      if (response.data.success) {
        setMultiResults(response.data);
      } else {
        setMultiError(response.data.error || 'Simulation failed');
      }
    } catch (err) {
      setMultiError(err.response?.data?.error || err.message || 'Failed to connect to server');
    } finally {
      setMultiLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />

      <div className="tab-nav">
        <button
          className={`tab-btn${activeTab === 'single' ? ' active' : ''}`}
          onClick={() => setActiveTab('single')}
        >
          Single Simulation
        </button>
        <button
          className={`tab-btn${activeTab === 'multiple' ? ' active' : ''}`}
          onClick={() => setActiveTab('multiple')}
        >
          Multiple Simulations
        </button>
      </div>

      <div className="main-container">
        {activeTab === 'single' && (
          <>
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
          </>
        )}

        {activeTab === 'multiple' && (
          <>
            <div className="simulator-section">
              <MultipleSimForm onSimulate={handleMultiSimulate} loading={multiLoading} />
            </div>

            {multiError && (
              <div className="error-message">
                <strong>Error:</strong> {multiError}
              </div>
            )}

            {multiLoading && (
              <div className="loading-container">
                <div className="spinner"></div>
                <p>Running parameter sweep for all 4 protocols...</p>
                <p className="loading-subtext">
                  {multiNPoints} points × 4 protocols = {multiNPoints * 4} simulations. This may take a while.
                </p>
              </div>
            )}

            {multiResults && !multiLoading && (
              <MultipleSimResults
                results={multiResults}
                xLabel={multiLabels.xLabel}
                yLabel={multiLabels.yLabel}
              />
            )}
          </>
        )}
      </div>

      <footer className="footer">
        <p>@copyright Dr. Kartick Sutradhar</p>
      </footer>
    </div>
  );
}

export default App;
