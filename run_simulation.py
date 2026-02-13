"""
Command-line interface for running QKD simulations
Usage: python run_simulation.py [config_name] [protocol]
"""

import sys
from qkd_simulator import QKDSimulator
from example_configs import get_config, print_config_info


def run_simulation(config_name='ideal', protocol=None):
    """
    Run a QKD simulation with specified configuration
    
    Args:
        config_name: Name of configuration ('short', 'long', 'ideal', etc.)
        protocol: Protocol to use (overrides config), e.g., 'BB84', 'E91'
    """
    
    print("\n" + "="*70)
    print(f" QKD SIMULATION - {config_name.upper()}")
    print("="*70)
    
    # Get configuration
    params = get_config(config_name)
    
    # Override protocol if specified
    if protocol:
        params['protocol'] = protocol.upper()
    
    protocol_name = params['protocol']
    
    print(f"\nProtocol: {protocol_name}")
    print(f"Number of qubits: {params['n_qubits']:,}")
    print(f"Fiber length: {params['fiber_length']} km")
    print(f"Eavesdropping: {'Enabled' if params['eavesdropping'] else 'Disabled'}")
    print("\nRunning simulation...")
    
    # Create simulator
    simulator = QKDSimulator()
    
    # Run appropriate protocol
    if protocol_name == 'BB84':
        results = simulator.simulate_bb84(params)
    elif protocol_name == 'B92':
        results = simulator.simulate_b92(params)
    elif protocol_name == 'E91':
        results = simulator.simulate_e91(params)
    elif protocol_name == 'BBM92':
        results = simulator.simulate_bbm92(params)
    else:
        print(f"Error: Unknown protocol '{protocol_name}'")
        return None
    
    # Display results
    print("\n" + "-"*70)
    print(" RESULTS")
    print("-"*70)
    print(f"  Key length:          {results['key_length']:,} bits")
    print(f"  Key rate:            {results['key_rate']:,.2f} Hz")
    print(f"  QBER:                {results['qber']:.2f}%")
    
    if results['s_statistic'] is not None:
        print(f"  S statistic:         {results['s_statistic']:.2f}")
        if results['s_statistic'] > 2:
            print("                       ✓ Entanglement verified (S > 2)")
        else:
            print("                       ✗ Below classical limit (S ≤ 2)")
    
    print(f"  Combined efficiency: {results['combined_efficiency']:.2f}%")
    
    # Interpretation
    print("\n" + "-"*70)
    print(" INTERPRETATION")
    print("-"*70)
    
    if results['qber'] == 0:
        print("  • Perfect transmission - no errors detected")
    elif results['qber'] < 5:
        print("  • Good transmission quality")
    elif results['qber'] < 11:
        print("  • Acceptable error rate for QKD")
    elif results['qber'] < 20:
        print("  • High error rate - check system parameters")
    else:
        print("  • ⚠ Very high error rate - possible eavesdropping!")
    
    if results['key_rate'] < 100:
        print("  • Low key rate - consider reducing fiber length or improving efficiency")
    elif results['key_rate'] < 10000:
        print("  • Moderate key rate - suitable for low-bandwidth applications")
    else:
        print("  • High key rate - excellent for practical applications")
    
    print("="*70 + "\n")
    
    return results


def compare_protocols(config_name='comparison'):
    """Compare all four protocols with same configuration"""
    
    print("\n" + "="*70)
    print(f" PROTOCOL COMPARISON - {config_name.upper()}")
    print("="*70)
    
    protocols = ['BB84', 'B92', 'E91', 'BBM92']
    results_all = {}
    
    for protocol in protocols:
        print(f"\nRunning {protocol}...")
        results = run_simulation(config_name, protocol)
        results_all[protocol] = results
    
    # Summary comparison
    print("\n" + "="*70)
    print(" COMPARISON SUMMARY")
    print("="*70)
    print(f"\n{'Protocol':<10} {'Key Rate (Hz)':<15} {'QBER (%)':<12} {'Key Length':<15}")
    print("-"*70)
    
    for protocol in protocols:
        r = results_all[protocol]
        print(f"{protocol:<10} {r['key_rate']:>12,.2f}   {r['qber']:>8.2f}    {r['key_length']:>12,}")
    
    print("\n" + "="*70)
    
    # Find best protocol
    best_rate = max(protocols, key=lambda p: results_all[p]['key_rate'])
    best_qber = min(protocols, key=lambda p: results_all[p]['qber'])
    
    print(f"\n  Best key rate:  {best_rate} ({results_all[best_rate]['key_rate']:,.2f} Hz)")
    print(f"  Lowest QBER:    {best_qber} ({results_all[best_qber]['qber']:.2f}%)")
    print("\n" + "="*70 + "\n")


def print_help():
    """Print usage information"""
    print("\n" + "="*70)
    print(" QKD SIMULATOR - COMMAND LINE INTERFACE")
    print("="*70)
    print("\nUsage:")
    print("  python run_simulation.py [config] [protocol]")
    print("\nExamples:")
    print("  python run_simulation.py ideal")
    print("  python run_simulation.py short BB84")
    print("  python run_simulation.py long E91")
    print("  python run_simulation.py compare")
    print("\nAvailable Configs:")
    print("  short, long, free_space, ideal, eavesdrop, comparison, metro")
    print("\nAvailable Protocols:")
    print("  BB84, B92, E91, BBM92")
    print("\nSpecial Commands:")
    print("  python run_simulation.py compare         # Compare all protocols")
    print("  python run_simulation.py configs         # List all configurations")
    print("  python run_simulation.py help            # Show this help")
    print("\n" + "="*70 + "\n")


def main():
    """Main entry point"""
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        # No arguments - run default
        run_simulation('ideal', 'BB84')
    
    elif sys.argv[1].lower() in ['help', '-h', '--help']:
        print_help()
    
    elif sys.argv[1].lower() == 'configs':
        print_config_info()
    
    elif sys.argv[1].lower() == 'compare':
        config = sys.argv[2] if len(sys.argv) > 2 else 'comparison'
        compare_protocols(config)
    
    else:
        config = sys.argv[1]
        protocol = sys.argv[2] if len(sys.argv) > 2 else None
        run_simulation(config, protocol)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nFor help, run: python run_simulation.py help")
        sys.exit(1)
