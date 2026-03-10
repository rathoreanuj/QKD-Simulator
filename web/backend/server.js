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

// Execute multi-protocol parameter sweep in a single Python process
function runMultiSimulator(config) {
  return new Promise((resolve, reject) => {
    const simDir = path.join(__dirname, '..', '..');
    const pythonCode = `import sys
import json
import numpy as np
sys.path.insert(0, ${JSON.stringify(simDir)})
from qkd_simulator import QKDSimulator

data_in = json.loads(sys.stdin.read())
base_params = data_in['base_params']
x_param = data_in['x_param']
y_param = data_in['y_param']
start_val = float(data_in['start_val'])
end_val = float(data_in['end_val'])
n_points = int(data_in['n_points'])
PERCENT_PARAMS = {'source_efficiency', 'detector_efficiency', 'perturb_prob', 'qber_fraction'}
if n_points == 1:
    x_values = [start_val]
else:
    x_values = list(np.linspace(start_val, end_val, n_points))
simulator = QKDSimulator()
sim_fns = {
    'BB84': simulator.simulate_bb84,
    'B92': simulator.simulate_b92,
    'E91': simulator.simulate_e91,
    'BBM92': simulator.simulate_bbm92,
}
data = {'BB84': [], 'B92': [], 'E91': [], 'BBM92': []}
for x_val in x_values:
    params = dict(base_params)
    params[x_param] = x_val / 100.0 if x_param in PERCENT_PARAMS else x_val
    for protocol in ['BB84', 'B92', 'E91', 'BBM92']:
        result = sim_fns[protocol](params)
        y = result.get(y_param)
        data[protocol].append(float(y) if y is not None else 0.0)
print(json.dumps({'x_values': [float(v) for v in x_values], 'data': data}))
`;

    const pythonProcess = spawn('python', ['-c', pythonCode]);
    let output = '';
    let errorOutput = '';

    pythonProcess.stdin.write(JSON.stringify(config));
    pythonProcess.stdin.end();

    pythonProcess.stdout.on('data', (data) => { output += data.toString(); });
    pythonProcess.stderr.on('data', (data) => { errorOutput += data.toString(); });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python process exited with code ${code}\n${errorOutput}`));
      } else {
        try {
          resolve(JSON.parse(output));
        } catch (e) {
          reject(new Error(`Failed to parse Python output: ${e.message}\n${output}`));
        }
      }
    });
  });
}

// Multi-simulation endpoint (parameter sweep, all 4 protocols)
app.post('/api/simulate/multi', async (req, res) => {
  try {
    const { x_param, y_param, start_val, end_val, n_points, base_params } = req.body;

    if (!x_param || !y_param || start_val === undefined || end_val === undefined || !n_points || !base_params) {
      return res.status(400).json({ success: false, error: 'Missing required parameters' });
    }

    const config = {
      base_params: {
        source_rate: parseFloat(base_params.source_rate || 72.6),
        source_efficiency: parseFloat(base_params.source_efficiency || 0.05),
        fiber_length: parseFloat(base_params.fiber_length || 18.0),
        fiber_loss: parseFloat(base_params.fiber_loss || 0.53),
        detector_efficiency: parseFloat(base_params.detector_efficiency || 0.11),
        perturb_prob: parseFloat(base_params.perturb_prob || 0.05),
        sop_deviation: parseFloat(base_params.sop_deviation || 0.13),
        n_qubits: parseInt(base_params.n_qubits || 100000),
        qber_fraction: parseFloat(base_params.qber_fraction || 0.1),
        losses_enabled: base_params.losses_enabled !== false,
        perturb_enabled: base_params.perturb_enabled !== false,
        eavesdropping: base_params.eavesdropping || false,
        sop_enabled: base_params.sop_enabled !== false,
      },
      x_param,
      y_param,
      start_val: parseFloat(start_val),
      end_val: parseFloat(end_val),
      n_points: parseInt(n_points),
    };

    const result = await runMultiSimulator(config);
    res.json({ success: true, ...result });
  } catch (error) {
    console.error('Error running multi simulation:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

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
