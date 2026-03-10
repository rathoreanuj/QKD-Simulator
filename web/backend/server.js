const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from React build (for production)
app.use(express.static(path.join(__dirname, '../frontend/build')));

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Node.js backend is running' });
});

// Python simulator path
const PYTHON_PATH = path.join(__dirname, '..', '..', 'qkd_simulator.py');

// Execute Python simulator
function runPythonSimulator(protocol, params) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', [
      '-c',
      `
import sys
import json
sys.path.append('${path.join(__dirname, '..', '..')}')
from qkd_simulator import QKDSimulator

simulator = QKDSimulator()
params = json.loads('''${JSON.stringify(params)}''')

if '${protocol}' == 'BB84':
    results = simulator.simulate_bb84(params)
elif '${protocol}' == 'B92':
    results = simulator.simulate_b92(params)
elif '${protocol}' == 'E91':
    results = simulator.simulate_e91(params)
elif '${protocol}' == 'BBM92':
    results = simulator.simulate_bbm92(params)

print(json.dumps(results))
      `
    ]);

    let output = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}\n${errorOutput}`));
      } else {
        try {
          const results = JSON.parse(output);
          resolve(results);
        } catch (e) {
          reject(new Error(`Failed to parse Python output: ${e.message}\n${output}`));
        }
      }
    });
  });
}

// Simulate all protocols endpoint
app.post('/api/simulate/all', async (req, res) => {
  try {
    const params = {
      source_rate: parseFloat(req.body.source_rate || 72.6),
      source_efficiency: parseFloat(req.body.source_efficiency || 0.05),
      fiber_length: parseFloat(req.body.fiber_length || 18.0),
      fiber_loss: parseFloat(req.body.fiber_loss || 0.53),
      detector_efficiency: parseFloat(req.body.detector_efficiency || 0.11),
      perturb_prob: parseFloat(req.body.perturb_prob || 0.05),
      sop_deviation: parseFloat(req.body.sop_deviation || 0.13),
      n_qubits: parseInt(req.body.n_qubits || 100000),
      qber_fraction: parseFloat(req.body.qber_fraction || 0.1),
      losses_enabled: req.body.losses_enabled !== false,
      perturb_enabled: req.body.perturb_enabled !== false,
      eavesdropping: req.body.eavesdropping || false,
      sop_enabled: req.body.sop_enabled !== false
    };

    const protocols = ['BB84', 'B92', 'E91', 'BBM92'];
    const results = {};

    // Run simulations sequentially
    for (const protocol of protocols) {
      const result = await runPythonSimulator(protocol, params);
      results[protocol] = result;
    }

    res.json({
      success: true,
      results: results
    });

  } catch (error) {
    console.error('Error running simulation:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Simulate single protocol endpoint
app.post('/api/simulate/:protocol', async (req, res) => {
  try {
    const protocol = req.params.protocol.toUpperCase();
    
    if (!['BB84', 'B92', 'E91', 'BBM92'].includes(protocol)) {
      return res.status(400).json({
        success: false,
        error: `Unknown protocol: ${protocol}`
      });
    }

    const params = {
      source_rate: parseFloat(req.body.source_rate || 72.6),
      source_efficiency: parseFloat(req.body.source_efficiency || 0.05),
      fiber_length: parseFloat(req.body.fiber_length || 18.0),
      fiber_loss: parseFloat(req.body.fiber_loss || 0.53),
      detector_efficiency: parseFloat(req.body.detector_efficiency || 0.11),
      perturb_prob: parseFloat(req.body.perturb_prob || 0.05),
      sop_deviation: parseFloat(req.body.sop_deviation || 0.13),
      n_qubits: parseInt(req.body.n_qubits || 100000),
      qber_fraction: parseFloat(req.body.qber_fraction || 0.1),
      losses_enabled: req.body.losses_enabled !== false,
      perturb_enabled: req.body.perturb_enabled !== false,
      eavesdropping: req.body.eavesdropping || false,
      sop_enabled: req.body.sop_enabled !== false
    };

    const results = await runPythonSimulator(protocol, params);

    res.json({
      success: true,
      protocol: protocol,
      results: results
    });

  } catch (error) {
    console.error('Error running simulation:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Serve React app for all other routes (production)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`✓ Node.js backend server running on port ${PORT}`);
  console.log(`✓ API endpoints available at http://localhost:${PORT}/api`);
});
