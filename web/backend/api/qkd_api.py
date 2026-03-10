"""
Flask API wrapper for QKD Simulator
Provides REST endpoints for the Node.js backend to call
"""

import sys
import os

# Add parent directory to path to import qkd_simulator
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from flask import Flask, request, jsonify
from flask_cors import CORS
from qkd_simulator import QKDSimulator

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

simulator = QKDSimulator()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "QKD Simulator API is running"})


@app.route('/api/simulate/all', methods=['POST'])
def simulate_all_protocols():
    """
    Run simulation for all 4 protocols with given parameters
    """
    try:
        data = request.json
        
        # Extract parameters
        params = {
            'source_rate': float(data.get('source_rate', 72.6)),
            'source_efficiency': float(data.get('source_efficiency', 0.05)),
            'fiber_length': float(data.get('fiber_length', 18.0)),
            'fiber_loss': float(data.get('fiber_loss', 0.53)),
            'detector_efficiency': float(data.get('detector_efficiency', 0.11)),
            'perturb_prob': float(data.get('perturb_prob', 0.05)),
            'sop_deviation': float(data.get('sop_deviation', 0.13)),
            'n_qubits': int(data.get('n_qubits', 100000)),
            'qber_fraction': float(data.get('qber_fraction', 0.1)),
            'losses_enabled': bool(data.get('losses_enabled', True)),
            'perturb_enabled': bool(data.get('perturb_enabled', True)),
            'eavesdropping': bool(data.get('eavesdropping', False)),
            'sop_enabled': bool(data.get('sop_enabled', True))
        }
        
        # Run simulations for all protocols
        results = {}
        protocols = ['BB84', 'B92', 'E91', 'BBM92']
        
        for protocol in protocols:
            if protocol == 'BB84':
                result = simulator.simulate_bb84(params)
            elif protocol == 'B92':
                result = simulator.simulate_b92(params)
            elif protocol == 'E91':
                result = simulator.simulate_e91(params)
            elif protocol == 'BBM92':
                result = simulator.simulate_bbm92(params)
            
            results[protocol] = result
        
        return jsonify({
            "success": True,
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/simulate/<protocol>', methods=['POST'])
def simulate_protocol(protocol):
    """
    Run simulation for a specific protocol
    """
    try:
        data = request.json
        
        # Extract parameters
        params = {
            'source_rate': float(data.get('source_rate', 72.6)),
            'source_efficiency': float(data.get('source_efficiency', 0.05)),
            'fiber_length': float(data.get('fiber_length', 18.0)),
            'fiber_loss': float(data.get('fiber_loss', 0.53)),
            'detector_efficiency': float(data.get('detector_efficiency', 0.11)),
            'perturb_prob': float(data.get('perturb_prob', 0.05)),
            'sop_deviation': float(data.get('sop_deviation', 0.13)),
            'n_qubits': int(data.get('n_qubits', 100000)),
            'qber_fraction': float(data.get('qber_fraction', 0.1)),
            'losses_enabled': bool(data.get('losses_enabled', True)),
            'perturb_enabled': bool(data.get('perturb_enabled', True)),
            'eavesdropping': bool(data.get('eavesdropping', False)),
            'sop_enabled': bool(data.get('sop_enabled', True))
        }
        
        # Run simulation based on protocol
        protocol = protocol.upper()
        if protocol == 'BB84':
            results = simulator.simulate_bb84(params)
        elif protocol == 'B92':
            results = simulator.simulate_b92(params)
        elif protocol == 'E91':
            results = simulator.simulate_e91(params)
        elif protocol == 'BBM92':
            results = simulator.simulate_bbm92(params)
        else:
            return jsonify({
                "success": False,
                "error": f"Unknown protocol: {protocol}"
            }), 400
        
        return jsonify({
            "success": True,
            "protocol": protocol,
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
