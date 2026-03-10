import React, { useState } from 'react';
import './SimulatorForm.css';

function SimulatorForm({ onSimulate, loading }) {
  const [params, setParams] = useState({
    source_rate: 72.6,
    source_efficiency: 5.0,
    fiber_length: 18.0,
    fiber_loss: 0.53,
    detector_efficiency: 11.0,
    perturb_prob: 5.0,
    sop_deviation: 0.13,
    n_qubits: 100000,
    qber_fraction: 10.0,
    losses_enabled: true,
    perturb_enabled: true,
    eavesdropping: false,
    sop_enabled: true
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === 'checkbox') {
      setParams(prev => ({ ...prev, [name]: checked }));
    } else {
      setParams(prev => ({ ...prev, [name]: parseFloat(value) || value }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Convert percentages to fractions for backend
    const processedParams = {
      ...params,
      source_efficiency: params.source_efficiency / 100,
      detector_efficiency: params.detector_efficiency / 100,
      perturb_prob: params.perturb_prob / 100,
      qber_fraction: params.qber_fraction / 100
    };
    
    onSimulate(processedParams);
  };

  return (
    <form onSubmit={handleSubmit} className="simulator-form">
      <h2>Simulation Parameters</h2>
      
      <div className="form-grid">
        {/* System Parameters */}
        <div className="form-section">
          <h3>System Parameters</h3>
          
          <div className="form-group">
            <label>Source Generation Rate (MHz)</label>
            <input
              type="number"
              step="0.01"
              name="source_rate"
              value={params.source_rate}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Source Efficiency (%)</label>
            <input
              type="number"
              step="0.01"
              name="source_efficiency"
              value={params.source_efficiency}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Fiber Length (km)</label>
            <input
              type="number"
              step="0.01"
              name="fiber_length"
              value={params.fiber_length}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Fiber Loss (dB/km)</label>
            <input
              type="number"
              step="0.01"
              name="fiber_loss"
              value={params.fiber_loss}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Detector Efficiency (%)</label>
            <input
              type="number"
              step="0.01"
              name="detector_efficiency"
              value={params.detector_efficiency}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Perturb Probability (%)</label>
            <input
              type="number"
              step="0.01"
              name="perturb_prob"
              value={params.perturb_prob}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>SOP Mean Deviation (rad)</label>
            <input
              type="number"
              step="0.01"
              name="sop_deviation"
              value={params.sop_deviation}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        {/* Simulation Settings */}
        <div className="form-section">
          <h3>Simulation Settings</h3>

          <div className="form-group">
            <label>Number of Qubits</label>
            <input
              type="number"
              name="n_qubits"
              value={params.n_qubits}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>QBER Cross-check Fraction (%)</label>
            <input
              type="number"
              step="0.01"
              name="qber_fraction"
              value={params.qber_fraction}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="losses_enabled"
                checked={params.losses_enabled}
                onChange={handleChange}
              />
              <span>Losses Enabled</span>
            </label>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="perturb_enabled"
                checked={params.perturb_enabled}
                onChange={handleChange}
              />
              <span>Perturbations Enabled</span>
            </label>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="eavesdropping"
                checked={params.eavesdropping}
                onChange={handleChange}
              />
              <span>Eavesdropping Enabled</span>
            </label>
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input
                type="checkbox"
                name="sop_enabled"
                checked={params.sop_enabled}
                onChange={handleChange}
              />
              <span>SOP Uncertainty Enabled</span>
            </label>
          </div>
        </div>
      </div>

      <button 
        type="submit" 
        className="submit-button"
        disabled={loading}
      >
        {loading ? 'Running Simulations...' : 'Run Simulations for All Protocols'}
      </button>
    </form>
  );
}

export default SimulatorForm;
