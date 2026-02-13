"""
Test script for QKD Simulator
Run this to verify installation and basic functionality
"""

from qkd_simulator import QKDSimulator
import time

def test_bb84():
    """Test BB84 protocol"""
    print("\n" + "="*50)
    print("Testing BB84 Protocol")
    print("="*50)
    
    simulator = QKDSimulator()
    
    params = {
        'n_qubits': 10000,
        'source_rate': 72.6,
        'source_efficiency': 0.058,
        'fiber_length': 18,
        'fiber_loss': 0.53,
        'detector_efficiency': 0.11,
        'perturb_prob': 0.05,
        'sop_deviation': 0.13,
        'qber_fraction': 0.1,
        'eavesdropping': False,
        'losses_enabled': True,
        'perturb_enabled': True,
        'sop_enabled': True
    }
    
    print("\nRunning simulation with 10,000 qubits...")
    start_time = time.time()
    
    results = simulator.simulate_bb84(params)
    
    elapsed = time.time() - start_time
    
    print(f"\nResults (completed in {elapsed:.2f}s):")
    print(f"  Key length: {results['key_length']}")
    print(f"  Key rate: {results['key_rate']:.2f} Hz")
    print(f"  QBER: {results['qber']:.2f}%")
    print(f"  Combined efficiency: {results['combined_efficiency']:.2f}%")
    
    return results['key_length'] > 0

def test_e91():
    """Test E91 protocol"""
    print("\n" + "="*50)
    print("Testing E91 Protocol")
    print("="*50)
    
    simulator = QKDSimulator()
    
    params = {
        'n_qubits': 10000,
        'source_rate': 72.6,
        'source_efficiency': 0.058,
        'fiber_length': 18,
        'fiber_loss': 0.53,
        'detector_efficiency': 0.11,
        'perturb_prob': 0.05,
        'sop_deviation': 0.13,
        'qber_fraction': 0.1,
        'eavesdropping': False,
        'losses_enabled': True,
        'perturb_enabled': True,
        'sop_enabled': True
    }
    
    print("\nRunning simulation with 10,000 qubits...")
    start_time = time.time()
    
    results = simulator.simulate_e91(params)
    
    elapsed = time.time() - start_time
    
    print(f"\nResults (completed in {elapsed:.2f}s):")
    print(f"  Key length: {results['key_length']}")
    print(f"  Key rate: {results['key_rate']:.2f} Hz")
    print(f"  QBER: {results['qber']:.2f}%")
    print(f"  S statistic: {results['s_statistic']:.2f}")
    print(f"  Combined efficiency: {results['combined_efficiency']:.2f}%")
    
    return results['key_length'] > 0

def test_eavesdropping():
    """Test eavesdropping detection"""
    print("\n" + "="*50)
    print("Testing Eavesdropping Detection (BB84)")
    print("="*50)
    
    simulator = QKDSimulator()
    
    params = {
        'n_qubits': 10000,
        'source_rate': 72.6,
        'source_efficiency': 0.058,
        'fiber_length': 18,
        'fiber_loss': 0.53,
        'detector_efficiency': 0.11,
        'perturb_prob': 0.0,
        'sop_deviation': 0.0,
        'qber_fraction': 0.1,
        'eavesdropping': True,
        'losses_enabled': True,
        'perturb_enabled': False,
        'sop_enabled': False
    }
    
    print("\nRunning simulation with eavesdropping enabled...")
    start_time = time.time()
    
    results = simulator.simulate_bb84(params)
    
    elapsed = time.time() - start_time
    
    print(f"\nResults (completed in {elapsed:.2f}s):")
    print(f"  QBER: {results['qber']:.2f}%")
    print(f"\n  Expected QBER ~25% with eavesdropping")
    
    if results['qber'] > 15:
        print("  ✓ Eavesdropping successfully detected!")
        return True
    else:
        print("  ✗ Eavesdropping detection failed")
        return False

def test_ideal_case():
    """Test ideal case (no losses, no errors)"""
    print("\n" + "="*50)
    print("Testing Ideal Case (No Losses/Errors)")
    print("="*50)
    
    simulator = QKDSimulator()
    
    params = {
        'n_qubits': 1000,
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
    
    print("\nRunning simulation with ideal parameters...")
    start_time = time.time()
    
    results = simulator.simulate_bb84(params)
    
    elapsed = time.time() - start_time
    
    print(f"\nResults (completed in {elapsed:.2f}s):")
    print(f"  Key length: {results['key_length']}")
    print(f"  QBER: {results['qber']:.2f}%")
    print(f"  Combined efficiency: {results['combined_efficiency']:.2f}%")
    
    if results['qber'] == 0:
        print("  ✓ Ideal case successful - 0% QBER!")
        return True
    else:
        print(f"  ⚠ Warning: Expected 0% QBER but got {results['qber']:.2f}%")
        return False

def main():
    print("\n" + "="*70)
    print(" QKD SIMULATOR - TEST SUITE")
    print("="*70)
    print("\nThis will test basic functionality of the QKD simulator.")
    print("Each test will run a quick simulation with 1,000-10,000 qubits.")
    
    results = []
    
    try:
        # Test 1: Ideal case
        results.append(("Ideal Case", test_ideal_case()))
        
        # Test 2: BB84 with realistic parameters
        results.append(("BB84 Protocol", test_bb84()))
        
        # Test 3: E91 with Bell test
        results.append(("E91 Protocol", test_e91()))
        
        # Test 4: Eavesdropping detection
        results.append(("Eavesdropping Detection", test_eavesdropping()))
        
        # Summary
        print("\n" + "="*70)
        print(" TEST SUMMARY")
        print("="*70)
        
        for test_name, passed in results:
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {test_name:<30} {status}")
        
        total_passed = sum(results)
        total_tests = len(results)
        
        print(f"\n  Total: {total_passed}/{total_tests} tests passed")
        
        if total_passed == total_tests:
            print("\n  🎉 All tests passed! Simulator is working correctly.")
            print("  You can now run the GUI with: python qkd_gui.py")
        else:
            print("\n  ⚠ Some tests failed. Check error messages above.")
        
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        print("\nMake sure all required packages are installed:")
        print("  pip install -r requirements.txt")
        return False
    
    return total_passed == total_tests

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
