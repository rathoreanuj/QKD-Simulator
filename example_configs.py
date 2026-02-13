"""
Example configurations for QKD simulations
Based on real experimental setups from the research paper
"""

# Configuration 1: Short-distance, high-rate system (Ref [25] from paper)
CONFIG_SHORT_DISTANCE = {
    'protocol': 'BB84',
    'n_qubits': 1000000,
    'source_rate': 72.6,  # MHz
    'source_efficiency': 0.058,  # 5.8%
    'fiber_length': 18,  # km
    'fiber_loss': 0.53,  # dB/km
    'detector_efficiency': 0.0627,  # 6.27%
    'perturb_prob': 0.05,  # 5%
    'sop_deviation': 0.13,  # rad
    'qber_fraction': 0.1,  # 10%
    'eavesdropping': False,
    'losses_enabled': True,
    'perturb_enabled': True,
    'sop_enabled': True
}

# Configuration 2: Long-distance system (Ref [26] from paper)
CONFIG_LONG_DISTANCE = {
    'protocol': 'BB84',
    'n_qubits': 1000000,
    'source_rate': 160.7,  # MHz
    'source_efficiency': 0.0142,  # 1.42%
    'fiber_length': 52,  # km
    'fiber_loss': 0.19,  # dB/km
    'detector_efficiency': 0.6525,  # 65.25%
    'perturb_prob': 0.006,  # 0.6%
    'sop_deviation': 0.13,  # rad
    'qber_fraction': 0.1,  # 10%
    'eavesdropping': False,
    'losses_enabled': True,
    'perturb_enabled': True,
    'sop_enabled': True
}

# Configuration 3: Free-space QKD (Ref [27] from paper)
CONFIG_FREE_SPACE = {
    'protocol': 'BB84',
    'n_qubits': 1000000,
    'source_rate': 80,  # MHz
    'source_efficiency': 0.08,  # 8%
    'fiber_length': 9.6,  # km (equivalent distance for attenuation)
    'fiber_loss': 1.0,  # dB/km (equivalent loss)
    'detector_efficiency': 0.24,  # 24%
    'perturb_prob': 0.0,  # N/A for free-space
    'sop_deviation': 0.0,  # N/A for free-space
    'qber_fraction': 0.1,  # 10%
    'eavesdropping': False,
    'losses_enabled': True,
    'perturb_enabled': False,
    'sop_enabled': False
}

# Configuration 4: Ideal (educational/theoretical)
CONFIG_IDEAL = {
    'protocol': 'BB84',
    'n_qubits': 10000,
    'source_rate': 100,  # MHz
    'source_efficiency': 1.0,  # 100%
    'fiber_length': 0,  # km
    'fiber_loss': 0,  # dB/km
    'detector_efficiency': 1.0,  # 100%
    'perturb_prob': 0.0,  # 0%
    'sop_deviation': 0.0,  # rad
    'qber_fraction': 0.1,  # 10%
    'eavesdropping': False,
    'losses_enabled': False,
    'perturb_enabled': False,
    'sop_enabled': False
}

# Configuration 5: Eavesdropping detection demo
CONFIG_EAVESDROP_DEMO = {
    'protocol': 'E91',
    'n_qubits': 100000,
    'source_rate': 80,  # MHz
    'source_efficiency': 0.1,  # 10%
    'fiber_length': 10,  # km
    'fiber_loss': 0.5,  # dB/km
    'detector_efficiency': 0.5,  # 50%
    'perturb_prob': 0.0,  # 0%
    'sop_deviation': 0.0,  # rad
    'qber_fraction': 0.2,  # 20% (more for Bell test)
    'eavesdropping': True,
    'losses_enabled': True,
    'perturb_enabled': False,
    'sop_enabled': False
}

# Configuration 6: Protocol comparison baseline
CONFIG_PROTOCOL_COMPARISON = {
    'protocol': 'BB84',  # Change to compare BB84, B92, E91, BBM92
    'n_qubits': 100000,
    'source_rate': 100,  # MHz
    'source_efficiency': 0.05,  # 5%
    'fiber_length': 25,  # km
    'fiber_loss': 0.3,  # dB/km
    'detector_efficiency': 0.2,  # 20%
    'perturb_prob': 0.02,  # 2%
    'sop_deviation': 0.1,  # rad
    'qber_fraction': 0.1,  # 10%
    'eavesdropping': False,
    'losses_enabled': True,
    'perturb_enabled': True,
    'sop_enabled': True
}

# Configuration 7: Metropolitan network (typical city distances)
CONFIG_METROPOLITAN = {
    'protocol': 'BBM92',
    'n_qubits': 500000,
    'source_rate': 150,  # MHz
    'source_efficiency': 0.03,  # 3%
    'fiber_length': 30,  # km (typical metro distance)
    'fiber_loss': 0.25,  # dB/km (good fiber)
    'detector_efficiency': 0.4,  # 40%
    'perturb_prob': 0.03,  # 3%
    'sop_deviation': 0.12,  # rad
    'qber_fraction': 0.15,  # 15%
    'eavesdropping': False,
    'losses_enabled': True,
    'perturb_enabled': True,
    'sop_enabled': True
}


def get_config(name='ideal'):
    """
    Get a configuration by name
    
    Available configs:
    - 'short': Short-distance high-rate system
    - 'long': Long-distance system
    - 'free_space': Free-space QKD
    - 'ideal': Ideal theoretical case
    - 'eavesdrop': Eavesdropping detection demo
    - 'comparison': Protocol comparison baseline
    - 'metro': Metropolitan network
    
    Returns:
        dict: Configuration parameters
    """
    configs = {
        'short': CONFIG_SHORT_DISTANCE,
        'long': CONFIG_LONG_DISTANCE,
        'free_space': CONFIG_FREE_SPACE,
        'ideal': CONFIG_IDEAL,
        'eavesdrop': CONFIG_EAVESDROP_DEMO,
        'comparison': CONFIG_PROTOCOL_COMPARISON,
        'metro': CONFIG_METROPOLITAN
    }
    
    return configs.get(name.lower(), CONFIG_IDEAL)


def print_config_info():
    """Print information about all available configurations"""
    print("Available Configurations:")
    print("\n1. SHORT DISTANCE (18 km, 13 kHz expected)")
    print("   - Based on experimental setup from Zahidy et al.")
    print("   - High source rate, moderate losses")
    print("   - Use: get_config('short')")
    
    print("\n2. LONG DISTANCE (52 km, 69 kHz expected)")
    print("   - Based on experimental setup from Morrison et al.")
    print("   - Very low source efficiency, high detector efficiency")
    print("   - Use: get_config('long')")
    
    print("\n3. FREE SPACE")
    print("   - Non-fiber based system")
    print("   - No polarization effects")
    print("   - Use: get_config('free_space')")
    
    print("\n4. IDEAL (Educational)")
    print("   - No losses, no errors")
    print("   - Perfect for learning protocols")
    print("   - Use: get_config('ideal')")
    
    print("\n5. EAVESDROPPING DEMO")
    print("   - E91 protocol with eavesdropper")
    print("   - Shows security features")
    print("   - Use: get_config('eavesdrop')")
    
    print("\n6. PROTOCOL COMPARISON")
    print("   - Baseline for comparing different protocols")
    print("   - Moderate realistic parameters")
    print("   - Use: get_config('comparison')")
    
    print("\n7. METROPOLITAN NETWORK")
    print("   - Typical city-scale distances")
    print("   - BBM92 protocol")
    print("   - Use: get_config('metro')")


if __name__ == "__main__":
    print("="*60)
    print(" QKD SIMULATOR - EXAMPLE CONFIGURATIONS")
    print("="*60)
    print()
    print_config_info()
    print()
    print("="*60)
    print()
    print("Usage in Python:")
    print("  from example_configs import get_config")
    print("  from qkd_simulator import QKDSimulator")
    print()
    print("  simulator = QKDSimulator()")
    print("  params = get_config('short')")
    print("  results = simulator.simulate_bb84(params)")
    print("="*60)
