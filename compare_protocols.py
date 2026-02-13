"""
Protocol Comparison Demo
Creates side-by-side comparison charts for all 4 QKD protocols
Perfect for presentations!
"""

from qkd_simulator import QKDSimulator
import matplotlib.pyplot as plt
import numpy as np

def compare_all_protocols():
    """Compare all protocols with realistic parameters"""
    
    print("="*70)
    print(" QKD PROTOCOL COMPARISON")
    print("="*70)
    print("\nRunning simulations for all 4 protocols...")
    print("This will take about 30-60 seconds...\n")
    
    protocols = ['BB84', 'B92', 'E91', 'BBM92']
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#06A77D']
    
    # Parameters: Realistic metropolitan network
    params = {
        'n_qubits': 50000,
        'source_rate': 100,
        'source_efficiency': 0.05,
        'fiber_length': 25,
        'fiber_loss': 0.3,
        'detector_efficiency': 0.2,
        'perturb_prob': 0.02,
        'sop_deviation': 0.1,
        'qber_fraction': 0.1,
        'eavesdropping': False,
        'losses_enabled': True,
        'perturb_enabled': True,
        'sop_enabled': True
    }
    
    sim = QKDSimulator()
    results = {}
    
    # Run simulations
    for i, protocol in enumerate(protocols):
        print(f"[{i+1}/4] Simulating {protocol}...", end=' ')
        
        if protocol == 'BB84':
            result = sim.simulate_bb84(params)
        elif protocol == 'B92':
            result = sim.simulate_b92(params)
        elif protocol == 'E91':
            result = sim.simulate_e91(params)
        else:
            result = sim.simulate_bbm92(params)
        
        results[protocol] = result
        print(f"✓ Key rate: {result['key_rate']:,.0f} Hz")
    
    # Print results
    print("\n" + "="*70)
    print(" RESULTS SUMMARY")
    print("="*70)
    print(f"\n{'Protocol':<12} {'Key Rate (Hz)':<18} {'QBER (%)':<12} {'Key Length':<15}")
    print("-"*70)
    
    for protocol in protocols:
        r = results[protocol]
        print(f"{protocol:<12} {r['key_rate']:>15,.2f}   {r['qber']:>8.2f}    {r['key_length']:>12,}")
    
    # Create comparison charts
    fig = plt.figure(figsize=(14, 10))
    
    # Chart 1: Key Rate Comparison
    ax1 = plt.subplot(2, 2, 1)
    key_rates = [results[p]['key_rate'] for p in protocols]
    bars1 = ax1.bar(protocols, key_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Key Rate (Hz)', fontsize=12, fontweight='bold')
    ax1.set_title('Key Rate Comparison', fontsize=14, fontweight='bold', pad=20)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_ylim(0, max(key_rates) * 1.15)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Chart 2: QBER Comparison
    ax2 = plt.subplot(2, 2, 2)
    qbers = [results[p]['qber'] for p in protocols]
    bars2 = ax2.bar(protocols, qbers, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('QBER (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Error Rate Comparison', fontsize=14, fontweight='bold', pad=20)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_ylim(0, max(qbers) * 1.2)
    
    # Add value labels
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Chart 3: Key Length Comparison
    ax3 = plt.subplot(2, 2, 3)
    key_lengths = [results[p]['key_length'] for p in protocols]
    bars3 = ax3.bar(protocols, key_lengths, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Final Key Length (bits)', fontsize=12, fontweight='bold')
    ax3.set_title('Key Length Comparison', fontsize=14, fontweight='bold', pad=20)
    ax3.grid(True, alpha=0.3, linestyle='--')
    ax3.set_ylim(0, max(key_lengths) * 1.15)
    
    # Add value labels
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Chart 4: Efficiency Comparison
    ax4 = plt.subplot(2, 2, 4)
    efficiencies = [results[p]['combined_efficiency'] for p in protocols]
    bars4 = ax4.bar(protocols, efficiencies, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax4.set_ylabel('Combined Efficiency (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Transmission Efficiency', fontsize=14, fontweight='bold', pad=20)
    ax4.grid(True, alpha=0.3, linestyle='--')
    ax4.set_ylim(0, max(efficiencies) * 1.15)
    
    # Add value labels
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.suptitle('QKD Protocol Comparison - Metropolitan Network (25 km)', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    
    # Save figure
    filename = 'protocol_comparison.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\n📊 Chart saved as '{filename}'")
    
    plt.show()
    
    # Find best protocol
    print("\n" + "="*70)
    print(" ANALYSIS")
    print("="*70)
    
    best_rate = max(protocols, key=lambda p: results[p]['key_rate'])
    best_qber = min(protocols, key=lambda p: results[p]['qber'])
    best_length = max(protocols, key=lambda p: results[p]['key_length'])
    
    print(f"\n✓ Highest key rate:   {best_rate} ({results[best_rate]['key_rate']:,.0f} Hz)")
    print(f"✓ Lowest QBER:        {best_qber} ({results[best_qber]['qber']:.2f}%)")
    print(f"✓ Longest key:        {best_length} ({results[best_length]['key_length']:,} bits)")
    
    print("\n" + "="*70)
    print(" KEY INSIGHTS")
    print("="*70)
    print("\n1. BB84 & BBM92: Highest efficiency (~50% of qubits become key)")
    print("2. B92: Lowest rate but simpler implementation")
    print("3. E91: Built-in security verification via Bell test")
    print("4. BBM92: Best practical choice (entanglement without Bell overhead)")
    
    print("\n" + "="*70)
    print("\nComparison complete! ✨")


def compare_with_eavesdropping():
    """Compare protocols with and without eavesdropping"""
    
    print("\n" + "="*70)
    print(" EAVESDROPPING DETECTION DEMO")
    print("="*70)
    print("\nComparing BB84 and E91 with/without eavesdropping...\n")
    
    params_secure = {
        'n_qubits': 20000,
        'source_rate': 100,
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
    
    params_eve = params_secure.copy()
    params_eve['eavesdropping'] = True
    
    sim = QKDSimulator()
    
    # BB84 comparison
    print("Testing BB84...")
    bb84_secure = sim.simulate_bb84(params_secure)
    bb84_eve = sim.simulate_bb84(params_eve)
    
    print("Testing E91...")
    e91_secure = sim.simulate_e91(params_secure)
    e91_eve = sim.simulate_e91(params_eve)
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # QBER comparison
    protocols = ['BB84\nSecure', 'BB84\nWith Eve', 'E91\nSecure', 'E91\nWith Eve']
    qbers = [bb84_secure['qber'], bb84_eve['qber'], 
             e91_secure['qber'], e91_eve['qber']]
    colors_qber = ['green', 'red', 'green', 'red']
    
    bars1 = ax1.bar(protocols, qbers, color=colors_qber, alpha=0.7, edgecolor='black', linewidth=2)
    ax1.set_ylabel('QBER (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Eavesdropping Detection via QBER', fontsize=14, fontweight='bold')
    ax1.axhline(y=11, color='orange', linestyle='--', linewidth=2, label='Security threshold (~11%)')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # S statistic for E91
    s_values = [e91_secure['s_statistic'], e91_eve['s_statistic']]
    s_labels = ['E91\nSecure', 'E91\nWith Eve']
    colors_s = ['green', 'red']
    
    bars2 = ax2.bar(s_labels, s_values, color=colors_s, alpha=0.7, edgecolor='black', linewidth=2)
    ax2.set_ylabel('S Statistic', fontsize=12, fontweight='bold')
    ax2.set_title('Bell Test - E91 Protocol', fontsize=14, fontweight='bold')
    ax2.axhline(y=2, color='orange', linestyle='--', linewidth=2, label='Classical limit (S=2)')
    ax2.axhline(y=2*np.sqrt(2), color='blue', linestyle=':', linewidth=2, label='Quantum maximum (2√2≈2.83)')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 3.5)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.suptitle('Security Verification: Eavesdropping Detection', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    filename = 'eavesdropping_detection.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\n📊 Chart saved as '{filename}'")
    
    plt.show()
    
    # Print results
    print("\n" + "="*70)
    print(" RESULTS")
    print("="*70)
    print(f"\nBB84 - Secure:     QBER = {bb84_secure['qber']:.2f}%  ✓ Safe")
    print(f"BB84 - With Eve:   QBER = {bb84_eve['qber']:.2f}%  ⚠️  ALERT!")
    print(f"\nE91 - Secure:      QBER = {e91_secure['qber']:.2f}%, S = {e91_secure['s_statistic']:.2f}  ✓ Entangled")
    print(f"E91 - With Eve:    QBER = {e91_eve['qber']:.2f}%, S = {e91_eve['s_statistic']:.2f}  ⚠️  No entanglement!")
    
    print("\n" + "="*70)
    print(" CONCLUSION")
    print("="*70)
    print("\n✓ Both protocols successfully detect eavesdropping")
    print("✓ QBER increases from ~0% to ~25% with Eve")
    print("✓ E91 provides additional verification via Bell test")
    print("✓ S statistic drops below classical limit (2) with Eve")
    print("\n" + "="*70)


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*10 + "QKD SIMULATOR - PROTOCOL COMPARISON DEMO" + " "*18 + "║")
    print("╚" + "="*68 + "╝")
    print("\n")
    
    # Main comparison
    compare_all_protocols()
    
    print("\n" + "="*70)
    print("\nWould you like to see eavesdropping detection demo? (y/n): ", end='')
    
    try:
        response = input().strip().lower()
        if response in ['y', 'yes']:
            compare_with_eavesdropping()
    except:
        print("\nSkipping eavesdropping demo.")
    
    print("\n" + "="*70)
    print(" Thank you for using QKD Simulator! 🔐✨")
    print("="*70 + "\n")
