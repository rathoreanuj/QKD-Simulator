"""
Quantum Key Distribution (QKD) Simulator
Educational tool for simulating QKD protocols: BB84, B92, E91, BBM92
Based on Qiskit library
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
try:
    from qiskit_aer import AerSimulator
    USE_AER = True
except ImportError:
    from qiskit.providers.basic_provider import BasicProvider
    USE_AER = False
import random
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')


class QKDSimulator:
    """Main class for simulating QKD protocols"""
    
    def __init__(self):
        if USE_AER:
            self.simulator = AerSimulator()
            self.use_aer = True
        else:
            self.backend = BasicProvider().get_backend('basic_simulator')
            self.use_aer = False
        self.results = {}
        
    def simulate_bb84(self, params: Dict) -> Dict:
        """
        Simulate BB84 protocol
        
        Parameters in params dict:
        - n_qubits: number of qubits to generate
        - source_rate: source generation rate (MHz)
        - source_efficiency: source efficiency (0-1)
        - fiber_length: fiber length (km)
        - fiber_loss: fiber loss (dB/km)
        - detector_efficiency: detector efficiency (0-1)
        - perturb_prob: perturbation probability (0-1)
        - sop_deviation: SOP mean deviation (radians)
        - qber_fraction: fraction for QBER check (0-1)
        - eavesdropping: enable eavesdropping (bool)
        - losses_enabled: enable losses (bool)
        - perturb_enabled: enable perturbations (bool)
        - sop_enabled: enable SOP deviation (bool)
        """
        
        n_qubits = params['n_qubits']
        qber_fraction = params['qber_fraction']
        
        # Store Alice's bits and bases
        alice_bits = []
        alice_bases = []
        bob_bases = []
        bob_measurements = []
        
        # Calculate loss probability
        if params['losses_enabled']:
            eta_s = params['source_efficiency']
            d = params['fiber_length']
            L = params['fiber_loss']
            eta_d = params['detector_efficiency']
            loss_prob = 1 - (eta_s * (10 ** (-d * L / 10)) * eta_d)
        else:
            loss_prob = 0
        
        # Generate and measure qubits
        for i in range(n_qubits):
            # Check if qubit is lost
            if random.random() < loss_prob:
                continue
                
            # Alice generates random bit and basis
            alice_bit = random.randint(0, 1)
            alice_basis = random.randint(0, 1)  # 0: rectilinear, 1: diagonal
            
            alice_bits.append(alice_bit)
            alice_bases.append(alice_basis)
            
            # Create quantum circuit
            qc = QuantumCircuit(1, 1)
            
            # Alice encodes the bit
            if alice_bit == 1:
                qc.x(0)  # Apply X gate for bit 1
            if alice_basis == 1:
                qc.h(0)  # Apply H gate for diagonal basis
            
            # Apply SOP deviation
            if params['sop_enabled']:
                sigma = params['sop_deviation'] * (2 / np.pi)
                theta = np.random.normal(0, sigma)
                qc.ry(2 * theta, 0)
            
            # Apply perturbations
            if params['perturb_enabled']:
                if random.random() < params['perturb_prob']:
                    theta = random.uniform(0, np.pi)
                    qc.ry(2 * theta, 0)
            
            # Eavesdropping
            if params['eavesdropping']:
                eve_choice = random.random()
                if eve_choice < 0.25:
                    qc.h(0)
                elif eve_choice < 0.5:
                    qc.x(0)
                    qc.h(0)
                    qc.x(0)
            
            # Bob measures in random basis
            bob_basis = random.randint(0, 1)
            bob_bases.append(bob_basis)
            
            if bob_basis == 1:
                qc.h(0)  # Change to diagonal basis
            
            qc.measure(0, 0)
            
            # Run circuit
            if self.use_aer:
                job = self.simulator.run(qc, shots=1)
                result = job.result()
                counts = result.get_counts()
                bob_bit = int(list(counts.keys())[0])
            else:
                # Use transpile and execute for basic simulator
                from qiskit import transpile
                qc_transpiled = transpile(qc, self.backend)
                job = self.backend.run(qc_transpiled, shots=1)
                result = job.result()
                counts = result.get_counts()
                bob_bit = int(list(counts.keys())[0])
            bob_measurements.append(bob_bit)
        
        # Sift key - keep only matching bases
        sifted_alice = []
        sifted_bob = []
        
        for i in range(len(alice_bits)):
            if alice_bases[i] == bob_bases[i]:
                sifted_alice.append(alice_bits[i])
                sifted_bob.append(bob_measurements[i])
        
        if len(sifted_alice) == 0:
            return {
                'key_length': 0,
                'qber': 0,
                'key_rate': 0,
                'combined_efficiency': 0,
                's_statistic': None
            }
        
        # Calculate QBER using a fraction of the key
        qber_check_size = int(len(sifted_alice) * qber_fraction)
        if qber_check_size > 0:
            errors = sum(sifted_alice[i] != sifted_bob[i] for i in range(qber_check_size))
            qber = errors / qber_check_size if qber_check_size > 0 else 0
            
            # Remove checked bits
            final_alice = sifted_alice[qber_check_size:]
            final_bob = sifted_bob[qber_check_size:]
        else:
            qber = 0
            final_alice = sifted_alice
            final_bob = sifted_bob
        
        key_length = len(final_alice)
        
        # Calculate combined efficiency
        eta_tot = (1 - loss_prob) if params['losses_enabled'] else 1.0
        
        # Calculate key rate
        key_rate = params['source_rate'] * 1e6 * eta_tot * (1 - qber_fraction) if (n_qubits > 0 and params['source_rate'] > 0) else 0
        
        return {
            'key_length': key_length,
            'qber': qber * 100,  # Convert to percentage
            'key_rate': key_rate,
            'combined_efficiency': eta_tot * 100,  # Convert to percentage
            's_statistic': None
        }
    
    def simulate_b92(self, params: Dict) -> Dict:
        """Simulate B92 protocol"""
        
        n_qubits = params['n_qubits']
        qber_fraction = params['qber_fraction']
        
        alice_bits = []
        bob_measurements = []
        bob_bases = []
        valid_measurements = []
        
        # Calculate loss probability
        if params['losses_enabled']:
            eta_s = params['source_efficiency']
            d = params['fiber_length']
            L = params['fiber_loss']
            eta_d = params['detector_efficiency']
            loss_prob = 1 - (eta_s * (10 ** (-d * L / 10)) * eta_d)
        else:
            loss_prob = 0
        
        for i in range(n_qubits):
            if random.random() < loss_prob:
                continue
            
            # Alice encodes: 0 -> |0>, 1 -> |+>
            alice_bit = random.randint(0, 1)
            alice_bits.append(alice_bit)
            
            qc = QuantumCircuit(1, 1)
            
            if alice_bit == 1:
                qc.h(0)  # |+> state
            
            # Apply SOP deviation
            if params['sop_enabled']:
                sigma = params['sop_deviation'] * (2 / np.pi)
                theta = np.random.normal(0, sigma)
                qc.ry(2 * theta, 0)
            
            # Apply perturbations
            if params['perturb_enabled']:
                if random.random() < params['perturb_prob']:
                    theta = random.uniform(0, np.pi)
                    qc.ry(2 * theta, 0)
            
            # Eavesdropping
            if params['eavesdropping']:
                eve_choice = random.random()
                if eve_choice < 0.25:
                    qc.h(0)
                elif eve_choice < 0.5:
                    qc.x(0)
                    qc.h(0)
                    qc.x(0)
            
            # Bob measures in random basis
            bob_basis = random.randint(0, 1)
            bob_bases.append(bob_basis)
            
            if bob_basis == 1:
                qc.h(0)
            
            qc.measure(0, 0)
            
            if self.use_aer:
                job = self.simulator.run(qc, shots=1)
                result = job.result()
                counts = result.get_counts()
                bob_bit = int(list(counts.keys())[0])
            else:
                from qiskit import transpile
                qc_transpiled = transpile(qc, self.backend)
                job = self.backend.run(qc_transpiled, shots=1)
                result = job.result()
                counts = result.get_counts()
                bob_bit = int(list(counts.keys())[0])
            bob_measurements.append(bob_bit)
            
            # B92 specific: only keep if Bob measured |-> or |1>
            if (bob_basis == 1 and bob_bit == 1) or (bob_basis == 0 and bob_bit == 1):
                valid_measurements.append((alice_bit, bob_bit))
        
        if len(valid_measurements) == 0:
            return {
                'key_length': 0,
                'qber': 0,
                'key_rate': 0,
                'combined_efficiency': 0,
                's_statistic': None
            }
        
        # Extract valid bits
        sifted_alice = [v[0] for v in valid_measurements]
        sifted_bob = [v[1] for v in valid_measurements]
        
        # Calculate QBER
        qber_check_size = int(len(sifted_alice) * qber_fraction)
        if qber_check_size > 0:
            errors = sum(sifted_alice[i] != sifted_bob[i] for i in range(qber_check_size))
            qber = errors / qber_check_size if qber_check_size > 0 else 0
            final_alice = sifted_alice[qber_check_size:]
        else:
            qber = 0
            final_alice = sifted_alice
        
        key_length = len(final_alice)
        eta_tot = (1 - loss_prob) if params['losses_enabled'] else 1.0
        key_rate = params['source_rate'] * 1e6 * eta_tot * (1 - qber_fraction) * 0.25 if params['source_rate'] > 0 else 0  # Lower for B92
        
        return {
            'key_length': key_length,
            'qber': qber * 100,
            'key_rate': key_rate,
            'combined_efficiency': eta_tot * 100,
            's_statistic': None
        }
    
    def simulate_e91(self, params: Dict) -> Dict:
        """Simulate E91 protocol with Bell test"""
        
        n_qubits = params['n_qubits']
        qber_fraction = params['qber_fraction']
        
        # Calculate loss probability
        if params['losses_enabled']:
            eta_s = params['source_efficiency']
            d = params['fiber_length']
            L = params['fiber_loss']
            eta_d = params['detector_efficiency']
            loss_prob = 1 - (eta_s * (10 ** (-d * L / 10)) * eta_d)
        else:
            loss_prob = 0
        
        alice_measurements = []
        bob_measurements = []
        alice_angles = []
        bob_angles = []
        
        # E91 angles
        alice_angle_choices = [0, np.pi/8, np.pi/4]
        bob_angle_choices = [np.pi/8, np.pi/4, 3*np.pi/8]
        
        for i in range(n_qubits):
            if random.random() < loss_prob:
                continue
            
            # Create Bell state |Φ+> = (|00> + |11>) / sqrt(2)
            qc = QuantumCircuit(2, 2)
            qc.h(0)
            qc.cx(0, 1)
            
            # Eavesdropping - replace with classical bits
            if params['eavesdropping']:
                qc.reset(0)
                qc.reset(1)
                if random.random() < 0.5:
                    qc.x(0)
                    qc.x(1)
            
            # Alice chooses random measurement angle
            alice_angle = random.choice(alice_angle_choices)
            alice_angles.append(alice_angle)
            qc.ry(-2 * alice_angle, 0)
            
            # Bob chooses random measurement angle
            bob_angle = random.choice(bob_angle_choices)
            bob_angles.append(bob_angle)
            qc.ry(-2 * bob_angle, 1)
            
            # Apply SOP deviation
            if params['sop_enabled']:
                sigma = params['sop_deviation'] * (2 / np.pi)
                theta1 = np.random.normal(0, sigma)
                theta2 = np.random.normal(0, sigma)
                qc.ry(2 * theta1, 0)
                qc.ry(2 * theta2, 1)
            
            # Apply perturbations
            if params['perturb_enabled']:
                if random.random() < params['perturb_prob']:
                    theta = random.uniform(0, np.pi)
                    qc.ry(2 * theta, 0)
                if random.random() < params['perturb_prob']:
                    theta = random.uniform(0, np.pi)
                    qc.ry(2 * theta, 1)
            
            qc.measure([0, 1], [0, 1])
            
            if self.use_aer:
                job = self.simulator.run(qc, shots=1)
                result = job.result()
                counts = result.get_counts()
                measurement = list(counts.keys())[0]
            else:
                from qiskit import transpile
                qc_transpiled = transpile(qc, self.backend)
                job = self.backend.run(qc_transpiled, shots=1)
                result = job.result()
                counts = result.get_counts()
                measurement = list(counts.keys())[0]
            
            alice_measurements.append(int(measurement[1]))
            bob_measurements.append(int(measurement[0]))
        
        if len(alice_measurements) == 0:
            return {
                'key_length': 0,
                'qber': 0,
                'key_rate': 0,
                'combined_efficiency': 0,
                's_statistic': 0
            }
        
        # Sift - keep matching angles
        sifted_alice = []
        sifted_bob = []
        bell_test_data = []
        
        for i in range(len(alice_measurements)):
            if alice_angles[i] == bob_angles[i]:
                sifted_alice.append(alice_measurements[i])
                sifted_bob.append(bob_measurements[i])
            else:
                bell_test_data.append((alice_angles[i], bob_angles[i], 
                                      alice_measurements[i], bob_measurements[i]))
        
        # Calculate S statistic for Bell test
        s_statistic = self._calculate_s_statistic(bell_test_data)
        
        # Calculate QBER
        if len(sifted_alice) > 0:
            qber_check_size = int(len(sifted_alice) * qber_fraction)
            if qber_check_size > 0:
                errors = sum(sifted_alice[i] != sifted_bob[i] for i in range(qber_check_size))
                qber = errors / qber_check_size if qber_check_size > 0 else 0
                final_alice = sifted_alice[qber_check_size:]
            else:
                qber = 0
                final_alice = sifted_alice
            key_length = len(final_alice)
        else:
            qber = 0
            key_length = 0
        
        eta_tot = (1 - loss_prob) if params['losses_enabled'] else 1.0
        key_rate = params['source_rate'] * 1e6 * eta_tot * (1 - qber_fraction) * 0.33 if params['source_rate'] > 0 else 0  # ~1/3 for E91
        
        return {
            'key_length': key_length,
            'qber': qber * 100,
            'key_rate': key_rate,
            'combined_efficiency': eta_tot * 100,
            's_statistic': s_statistic
        }
    
    def _calculate_s_statistic(self, data: List) -> float:
        """Calculate CHSH S statistic for Bell test"""
        
        if len(data) == 0:
            return 0
        
        # Group by angle pairs
        angle_pairs = {}
        for alice_angle, bob_angle, alice_bit, bob_bit in data:
            key = (alice_angle, bob_angle)
            if key not in angle_pairs:
                angle_pairs[key] = {'++': 0, '+-': 0, '-+': 0, '--': 0}
            
            # Convert to +/- notation (0 -> +, 1 -> -)
            alice_sign = '+' if alice_bit == 0 else '-'
            bob_sign = '+' if bob_bit == 0 else '-'
            angle_pairs[key][alice_sign + bob_sign] += 1
        
        # Calculate E values
        E_values = {}
        for angles, counts in angle_pairs.items():
            total = sum(counts.values())
            if total > 0:
                E = (counts['++'] - counts['+-'] - counts['-+'] + counts['--']) / total if total > 0 else 0
                E_values[angles] = E
            else:
                E_values[angles] = 0
        
        # Calculate S = E(a1,b1) - E(a1,b2) + E(a2,b1) + E(a2,b2)
        # a1=0, a2=π/4, b1=π/8, b2=3π/8
        try:
            E_a1_b1 = E_values.get((0, np.pi/8), 0)
            E_a1_b2 = E_values.get((0, 3*np.pi/8), 0)
            E_a2_b1 = E_values.get((np.pi/4, np.pi/8), 0)
            E_a2_b2 = E_values.get((np.pi/4, 3*np.pi/8), 0)
            
            S = abs(E_a1_b1 - E_a1_b2 + E_a2_b1 + E_a2_b2)
            return S
        except:
            return 0
    
    def simulate_bbm92(self, params: Dict) -> Dict:
        """Simulate BBM92 protocol"""
        
        n_qubits = params['n_qubits']
        qber_fraction = params['qber_fraction']
        
        # Calculate loss probability
        if params['losses_enabled']:
            eta_s = params['source_efficiency']
            d = params['fiber_length']
            L = params['fiber_loss']
            eta_d = params['detector_efficiency']
            loss_prob = 1 - (eta_s * (10 ** (-d * L / 10)) * eta_d)
        else:
            loss_prob = 0
        
        alice_measurements = []
        bob_measurements = []
        alice_bases = []
        bob_bases = []
        
        for i in range(n_qubits):
            if random.random() < loss_prob:
                continue
            
            # Create Bell state
            qc = QuantumCircuit(2, 2)
            qc.h(0)
            qc.cx(0, 1)
            
            # Eavesdropping
            if params['eavesdropping']:
                qc.reset(0)
                qc.reset(1)
                if random.random() < 0.5:
                    qc.x(0)
                    qc.x(1)
            
            # Apply SOP deviation
            if params['sop_enabled']:
                sigma = params['sop_deviation'] * (2 / np.pi)
                theta1 = np.random.normal(0, sigma)
                theta2 = np.random.normal(0, sigma)
                qc.ry(2 * theta1, 0)
                qc.ry(2 * theta2, 1)
            
            # Apply perturbations
            if params['perturb_enabled']:
                if random.random() < params['perturb_prob']:
                    theta = random.uniform(0, np.pi)
                    qc.ry(2 * theta, 0)
                if random.random() < params['perturb_prob']:
                    theta = random.uniform(0, np.pi)
                    qc.ry(2 * theta, 1)
            
            # Random basis choice
            alice_basis = random.randint(0, 1)
            bob_basis = random.randint(0, 1)
            
            alice_bases.append(alice_basis)
            bob_bases.append(bob_basis)
            
            if alice_basis == 1:
                qc.h(0)
            if bob_basis == 1:
                qc.h(1)
            
            qc.measure([0, 1], [0, 1])
            
            if self.use_aer:
                job = self.simulator.run(qc, shots=1)
                result = job.result()
                counts = result.get_counts()
                measurement = list(counts.keys())[0]
            else:
                from qiskit import transpile
                qc_transpiled = transpile(qc, self.backend)
                job = self.backend.run(qc_transpiled, shots=1)
                result = job.result()
                counts = result.get_counts()
                measurement = list(counts.keys())[0]
            
            alice_measurements.append(int(measurement[1]))
            bob_measurements.append(int(measurement[0]))
        
        # Sift - keep matching bases
        sifted_alice = []
        sifted_bob = []
        
        for i in range(len(alice_measurements)):
            if alice_bases[i] == bob_bases[i]:
                sifted_alice.append(alice_measurements[i])
                sifted_bob.append(bob_measurements[i])
        
        if len(sifted_alice) == 0:
            return {
                'key_length': 0,
                'qber': 0,
                'key_rate': 0,
                'combined_efficiency': 0,
                's_statistic': None
            }
        
        # Calculate QBER
        qber_check_size = int(len(sifted_alice) * qber_fraction)
        if qber_check_size > 0:
            errors = sum(sifted_alice[i] != sifted_bob[i] for i in range(qber_check_size))
            qber = errors / qber_check_size if qber_check_size > 0 else 0
            final_alice = sifted_alice[qber_check_size:]
        else:
            qber = 0
            final_alice = sifted_alice
        
        key_length = len(final_alice)
        eta_tot = (1 - loss_prob) if params['losses_enabled'] else 1.0
        key_rate = params['source_rate'] * 1e6 * eta_tot * (1 - qber_fraction) * 0.5 if params['source_rate'] > 0 else 0
        
        return {
            'key_length': key_length,
            'qber': qber * 100,
            'key_rate': key_rate,
            'combined_efficiency': eta_tot * 100,
            's_statistic': None
        }
    
    def get_sample_circuit(self, protocol: str, params: Dict) -> QuantumCircuit:
        """Generate a sample circuit for visualization"""
        
        if protocol == "BB84":
            qc = QuantumCircuit(10, 10)
            qc.barrier()
            # Encoding
            for i in range(10):
                if random.random() < 0.5:
                    qc.x(i)
                if random.random() < 0.5:
                    qc.h(i)
            qc.barrier()
            # Perturbations
            if params['perturb_enabled']:
                for i in range(10):
                    if random.random() < params['perturb_prob']:
                        qc.ry(random.uniform(0, 2*np.pi), i)
            qc.barrier()
            # Eavesdropping
            if params['eavesdropping']:
                for i in range(10):
                    choice = random.random()
                    if choice < 0.25:
                        qc.h(i)
            qc.barrier()
            # Decoding
            for i in range(10):
                if random.random() < 0.5:
                    qc.h(i)
            qc.barrier()
            qc.measure(range(10), range(10))
            
        elif protocol == "E91":
            qc = QuantumCircuit(4, 4)
            # Create 2 Bell pairs
            qc.barrier()
            for i in range(0, 4, 2):
                qc.h(i)
                qc.cx(i, i+1)
            qc.barrier()
            # Measurements
            for i in range(4):
                angle = random.choice([0, np.pi/8, np.pi/4, 3*np.pi/8])
                qc.ry(-2*angle, i)
            qc.barrier()
            qc.measure(range(4), range(4))
            
        else:  # BBM92 or B92
            qc = QuantumCircuit(10, 10)
            qc.barrier()
            for i in range(10):
                if random.random() < 0.5:
                    qc.h(i)
            qc.barrier()
            for i in range(10):
                if random.random() < 0.5:
                    qc.h(i)
            qc.barrier()
            qc.measure(range(10), range(10))
        
        return qc
