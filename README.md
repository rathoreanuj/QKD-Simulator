# Quantum Key Distribution (QKD) Simulator

An educational tool for simulating quantum key distribution protocols based on the research paper by Erik Åkerberg and Erik Åsgrim (2023).

## Features
- **Four QKD Protocols**: BB84, B92, E91, BBM92
- **Realistic System Modeling**: 
  - Fiber losses and attenuation
  - Detector efficiency
  - State of polarization (SOP) deviations
  - Perturbations
  - Eavesdropping detection
- **Interactive GUI**: Two-tab interface for single and multiple simulations
- **Visualization**: View quantum circuits and plot results
- **Performance Metrics**:
  - Key length and key rate
  - Quantum Bit Error Rate (QBER)
  - S statistic for E91 protocol (Bell test)
  - Combined efficiency

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd "c:\B TECH IIITS\Sem 6\Additional project under kartik sir\Demo"
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install qiskit qiskit-aer numpy matplotlib pillow
   ```

## Usage

### Running the Application

```bash
python qkd_gui.py
```

### Single Simulation Tab

1. **System Parameters** (Left Column):
   - Source generation rate (MHz)
   - Source efficiency (%)
   - Fiber length (km)
   - Fiber loss (dB/km)
   - Detector efficiency (%)
   - Perturb probability (%)
   - SOP mean deviation (rad)

2. **Simulation Settings** (Middle Column):
   - Choose protocol: BB84, B92, E91, or BBM92
   - Enable/disable: Losses, Perturbations, Eavesdropping, SOP uncertainty
   - Number of qubits to simulate
   - QBER cross-check fraction (%)

3. **Results** (Right Column):
   - Key length (number of bits)
   - Key rate (Hz)
   - QBER (%)
   - S statistic (for E91 only)
   - Combined efficiency (%)

4. **Buttons**:
   - **Run simulation**: Execute the simulation
   - **View sample**: Display a sample quantum circuit
   - **Abort**: Stop ongoing simulation

### Multiple Simulations Tab

1. **Parameters**:
   - Select x parameter to vary (e.g., Fiber loss)
   - Select y parameter to plot (e.g., Key rate)
   - Start value for x
   - End value for x
   - Number of points to simulate

2. **Plot**:
   - Displays results as they are calculated
   - Shows relationship between varied parameter and result metric

3. **Buttons**:
   - **Run simulations**: Execute multiple simulations
   - **Abort**: Stop ongoing simulations

## Protocols Overview

### BB84 (Bennett-Brassard 1984)
- Single-qubit protocol
- Uses rectilinear and diagonal bases
- Alice encodes random bits, Bob measures randomly
- ~50% of qubits kept after basis reconciliation

### B92 (Bennett 1992)
- Simplified version of BB84
- Uses non-orthogonal states (|0⟩ and |+⟩)
- Lower key rate but simpler implementation
- ~25% of qubits kept on average

### E91 (Ekert 1991)
- Entanglement-based protocol
- Uses Bell states and CHSH test
- Provides S statistic for security verification
- ~33% of qubits kept for key

### BBM92 (Bennett-Brassard-Mermin 1992)
- Simplified entanglement-based protocol
- Similar to BB84 but uses entangled pairs
- No Bell test required
- ~50% of qubits kept after basis reconciliation

## Example Use Cases

### 1. Educational Learning
- Start with BB84 protocol
- Disable all losses and perturbations
- Run with small number of qubits (1000)
- Observe ideal QBER of 0%
- View sample circuit to see quantum gates

### 2. Eavesdropping Detection
- Enable eavesdropping
- Observe QBER increase to ~25% for BB84
- For E91: observe S statistic drop below 2 (classical limit)

### 3. System Design
- Input your experimental parameters
- Compare different protocols
- Vary fiber length to find maximum distance
- Optimize source rate and detector efficiency

### 4. Experimental Validation
- Use parameters from real QKD experiments
- Compare simulated results to experimental data
- Validate system design before implementation

## Technical Details

### Simulation Method
- Built using Qiskit library
- Uses AerSimulator for quantum circuit execution
- Implements quantum gates (X, H, CNOT, RY) to represent protocol operations
- Applies noise models for realistic behavior

### System Parameters

**Losses**: Combined effect of source efficiency, fiber attenuation, and detector efficiency
- Total efficiency: η_tot = η_S × 10^(-dL/10) × η_D

**Perturbations**: Random rotations of photon polarization
- Simulated as RY gates with random angles

**SOP Deviation**: Imperfect polarization compensation
- Normal distribution with specified mean deviation

**Eavesdropping**: Intercept-resend attack
- Eve measures in random basis and forwards measured state

## Troubleshooting

### Import Errors
```
ImportError: No module named 'qiskit'
```
**Solution**: Install required packages:
```bash
pip install qiskit qiskit-aer
```

### Slow Simulations
**Issue**: Large number of qubits takes too long

**Solution**: 
- Start with fewer qubits (10,000 - 100,000)
- Increase for final results
- High losses require more qubits for reliable statistics

### Unreliable QBER
**Issue**: QBER fluctuates heavily between runs

**Solution**: Increase number of qubits to improve statistics

### GUI Not Responding
**Issue**: Application freezes during simulation

**Note**: This is normal for large simulations (Progress bar shows status)
- Use Abort button if needed
- Consider reducing number of qubits

## References

1. Åkerberg, E., & Åsgrim, E. (2023). "Developing an educational tool for simulations of quantum key distribution systems". KTH Royal Institute of Technology.

2. Bennett, C. H., & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing".

3. Ekert, A. K. (1991). "Quantum cryptography based on Bell's theorem".

4. Nielsen, M. A., & Chuang, I. L. (2010). "Quantum Computation and Quantum Information".

## License

This is an educational tool based on academic research. Please cite the original paper if used for academic purposes.

## Authors

GUI Implementation: Based on research by Erik Åkerberg and Erik Åsgrim (2023)

## Contact

For questions about the original research, refer to the paper:
"Developing an educational tool for simulations of quantum key distribution systems"
KTH Royal Institute of Technology, 2023
