"""Quick test to verify QKD simulator works"""
from qkd_simulator import QKDSimulator

print("Testing QKD Simulator...")
sim = QKDSimulator()
print("✓ QKD Simulator loaded successfully!")
print(f"✓ Using simulator: {'AerSimulator' if sim.use_aer else 'BasicSimulator (built-in)'}")
print("\nRunning quick BB84 test with 100 qubits...")

params = {
    'n_qubits': 100,
    'source_rate': 80,
    'source_efficiency': 1.0,
    'fiber_length': 0,
    'fiber_loss': 0,
    'detector_efficiency': 1.0,
    'perturb_prob': 0.0,
    'sop_deviation': 0.0,
    'qber_fraction': 0.1,
    'eavesdropping': False,
    'losses_enabled': False,
    'perturb_enabled': False,
    'sop_enabled': False
}

results = sim.simulate_bb84(params)
print(f"✓ Simulation completed!")
print(f"  Key length: {results['key_length']}")
print(f"  QBER: {results['qber']:.2f}%")

if results['qber'] == 0 and results['key_length'] > 0:
    print("\n✅ ALL CHECKS PASSED! The simulator is working correctly.")
    print("   You can now run: python qkd_gui.py")
else:
    print("\n⚠ Unexpected results - please check installation")
