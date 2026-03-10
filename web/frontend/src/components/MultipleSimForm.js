import React, { useState } from 'react';
import './MultipleSimForm.css';

const X_PARAMS = [
  { label: 'Source Generation Rate (MHz)', key: 'source_rate', defaultStart: 10, defaultEnd: 100 },
  { label: 'Source Efficiency (%)',         key: 'source_efficiency', defaultStart: 1, defaultEnd: 20 },
  { label: 'Fiber Length (km)',             key: 'fiber_length', defaultStart: 5, defaultEnd: 50 },
  { label: 'Fiber Loss (dB/km)',            key: 'fiber_loss', defaultStart: 0, defaultEnd: 1 },
  { label: 'Detector Efficiency (%)',       key: 'detector_efficiency', defaultStart: 5, defaultEnd: 25 },
  { label: 'Perturb Probability (%)',       key: 'perturb_prob', defaultStart: 0, defaultEnd: 15 },
  { label: 'SOP Mean Deviation (rad)',      key: 'sop_deviation', defaultStart: 0, defaultEnd: 0.5 },
  { label: 'QBER Cross-check Fraction (%)', key: 'qber_fraction', defaultStart: 5, defaultEnd: 30 },
];

const Y_PARAMS = [
  { label: 'Key Length',               key: 'key_length' },
  { label: 'Key Rate (Hz)',            key: 'key_rate' },
  { label: 'QBER (%)',                 key: 'qber' },
  { label: 'Combined Efficiency (%)',  key: 'combined_efficiency' },
];

function MultipleSimForm({ onSimulate, loading }) {
  const [baseParams, setBaseParams] = useState({
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
    sop_enabled: true,
  });

  const [xParam, setXParam] = useState('fiber_loss');
  const [yParam, setYParam] = useState('key_length');
  const [startVal, setStartVal] = useState(0.0);
  const [endVal, setEndVal] = useState(1.0);
  const [nPoints, setNPoints] = useState(10);

  const handleBaseChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === 'checkbox') {
      setBaseParams(prev => ({ ...prev, [name]: checked }));
    } else {
      setBaseParams(prev => ({ ...prev, [name]: parseFloat(value) || value }));
    }
  };

  const handleXParamChange = (e) => {
    const key = e.target.value;
    setXParam(key);
    const found = X_PARAMS.find(p => p.key === key);
    if (found) {
      setStartVal(found.defaultStart);
      setEndVal(found.defaultEnd);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const processedBase = {
      ...baseParams,
      source_efficiency: baseParams.source_efficiency / 100,
      detector_efficiency: baseParams.detector_efficiency / 100,
      perturb_prob: baseParams.perturb_prob / 100,
      qber_fraction: baseParams.qber_fraction / 100,
    };
    onSimulate({
      base_params: processedBase,
      x_param: xParam,
      y_param: yParam,
      start_val: parseFloat(startVal),
      end_val: parseFloat(endVal),
      n_points: parseInt(nPoints),
    });
  };

  const selectedXLabel = X_PARAMS.find(p => p.key === xParam)?.label || xParam;
  const selectedYLabel = Y_PARAMS.find(p => p.key === yParam)?.label || yParam;

  return (
    <form onSubmit={handleSubmit} className="multi-sim-form">
      <h2>Multiple Simulations – Parameter Sweep</h2>
      <p className="multi-sim-subtitle">
        Vary one parameter over a range and compare results across all 4 QKD protocols simultaneously.
      </p>

      <div className="multi-form-grid">
        {/* System Parameters */}
        <div className="form-section">
          <h3>System Parameters</h3>

          <div className="form-group">
            <label>Source Generation Rate (MHz)</label>
            <input type="number" step="0.01" name="source_rate"
              value={baseParams.source_rate} onChange={handleBaseChange} required />
          </div>
          <div className="form-group">
            <label>Source Efficiency (%)</label>
            <input type="number" step="0.01" name="source_efficiency"
              value={baseParams.source_efficiency} onChange={handleBaseChange} required />
          </div>
          <div className="form-group">
            <label>Fiber Length (km)</label>
            <input type="number" step="0.01" name="fiber_length"
              value={baseParams.fiber_length} onChange={handleBaseChange} required />
          </div>
          <div className="form-group">
            <label>Fiber Loss (dB/km)</label>
            <input type="number" step="0.01" name="fiber_loss"
              value={baseParams.fiber_loss} onChange={handleBaseChange} required />
          </div>
          <div className="form-group">
            <label>Detector Efficiency (%)</label>
            <input type="number" step="0.01" name="detector_efficiency"
              value={baseParams.detector_efficiency} onChange={handleBaseChange} required />
          </div>
          <div className="form-group">
            <label>Perturb Probability (%)</label>
            <input type="number" step="0.01" name="perturb_prob"
              value={baseParams.perturb_prob} onChange={handleBaseChange} required />
          </div>
          <div className="form-group">
            <label>SOP Mean Deviation (rad)</label>
            <input type="number" step="0.01" name="sop_deviation"
              value={baseParams.sop_deviation} onChange={handleBaseChange} required />
          </div>
        </div>

        {/* Simulation Settings */}
        <div className="form-section">
          <h3>Simulation Settings</h3>

          <div className="form-group">
            <label>Number of Qubits</label>
            <input type="number" name="n_qubits"
              value={baseParams.n_qubits} onChange={handleBaseChange} required />
          </div>
          <div className="form-group">
            <label>QBER Cross-check Fraction (%)</label>
            <input type="number" step="0.01" name="qber_fraction"
              value={baseParams.qber_fraction} onChange={handleBaseChange} required />
          </div>

          <div className="form-group checkbox-group">
            <label>
              <input type="checkbox" name="losses_enabled"
                checked={baseParams.losses_enabled} onChange={handleBaseChange} />
              <span>Losses Enabled</span>
            </label>
          </div>
          <div className="form-group checkbox-group">
            <label>
              <input type="checkbox" name="perturb_enabled"
                checked={baseParams.perturb_enabled} onChange={handleBaseChange} />
              <span>Perturbations Enabled</span>
            </label>
          </div>
          <div className="form-group checkbox-group">
            <label>
              <input type="checkbox" name="eavesdropping"
                checked={baseParams.eavesdropping} onChange={handleBaseChange} />
              <span>Eavesdropping Enabled</span>
            </label>
          </div>
          <div className="form-group checkbox-group">
            <label>
              <input type="checkbox" name="sop_enabled"
                checked={baseParams.sop_enabled} onChange={handleBaseChange} />
              <span>SOP Uncertainty Enabled</span>
            </label>
          </div>
        </div>

        {/* Sweep Parameters */}
        <div className="form-section sweep-section">
          <h3>Sweep Parameters</h3>

          <div className="form-group">
            <label>X Parameter (varied)</label>
            <select className="param-select" value={xParam} onChange={handleXParamChange}>
              {X_PARAMS.map(p => (
                <option key={p.key} value={p.key}>{p.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Y Parameter (plotted)</label>
            <select className="param-select" value={yParam} onChange={(e) => setYParam(e.target.value)}>
              {Y_PARAMS.map(p => (
                <option key={p.key} value={p.key}>{p.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Start Value — {selectedXLabel}</label>
            <input type="number" step="any" value={startVal}
              onChange={(e) => setStartVal(e.target.value)} required />
          </div>

          <div className="form-group">
            <label>End Value — {selectedXLabel}</label>
            <input type="number" step="any" value={endVal}
              onChange={(e) => setEndVal(e.target.value)} required />
          </div>

          <div className="form-group">
            <label>Number of Points</label>
            <input type="number" min="2" max="50" value={nPoints}
              onChange={(e) => setNPoints(e.target.value)} required />
          </div>

          <div className="sweep-summary">
            <span>
              Plotting <strong>{selectedYLabel}</strong> vs <strong>{selectedXLabel}</strong>
            </span>
            <span>{nPoints} points × 4 protocols = <strong>{nPoints * 4} simulations</strong></span>
          </div>
        </div>
      </div>

      <button type="submit" className="submit-button" disabled={loading}>
        {loading ? 'Running simulations…' : 'Run Simulations'}
      </button>
    </form>
  );
}

export default MultipleSimForm;
