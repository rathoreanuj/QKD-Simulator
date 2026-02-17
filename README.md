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

## Quick Start (Windows)

### Method 1: Use the Batch File (Easiest)
Double-click `run_simulator.bat` or run it from command prompt:
```cmd
run_simulator.bat
```
This will automatically check Python installation, install dependencies, and launch the GUI.

### Method 2: Manual Setup
1. Open Command Prompt or PowerShell
2. Navigate to the project directory
3. Install dependencies and run:
```cmd
pip install -r requirements.txt
python qkd_gui.py
```

## Detailed Installation Guide

### Prerequisites

- **Python 3.8 or higher**: Download from [python.org](https://www.python.org/downloads/)
  - During installation, check "Add Python to PATH"
- **pip package manager**: Included with Python 3.8+

### Step 1: Verify Python Installation

Open Command Prompt or PowerShell and verify Python is installed:
```cmd
python --version
```
You should see output like: `Python 3.10.x` or higher

Check pip is installed:
```cmd
pip --version
```

### Step 2: Navigate to Project Directory

```cmd
cd "c:\B TECH IIITS\Sem 6\Additional project under kartik sir\QKD Simulator"
```

### Step 3: Set Up Python Virtual Environment (Recommended)

A virtual environment keeps project dependencies isolated:

**Create virtual environment:**
```cmd
python -m venv venv
```

**Activate virtual environment:**
```cmd
venv\Scripts\activate
```
You should see `(venv)` prefix in your command prompt.

**To deactivate later:**
```cmd
deactivate
```

### Step 4: Install Required Packages

**Option A - Install from requirements.txt (recommended):**
```cmd
pip install -r requirements.txt
```

**Option B - Install packages individually:**
```cmd
pip install qiskit>=1.0.0
pip install numpy>=1.26.0
pip install matplotlib>=3.7.0
pip install pillow>=10.0.0
```

**Verify installation:**
```cmd
pip list
```
You should see qiskit, numpy, matplotlib, and pillow in the list.

### Step 5: Run the Simulator

**Option A - GUI Interface (Recommended for beginners):**
```cmd
python qkd_gui.py
```

**Option B - Command-Line Interface:**
```cmd
python run_simulation.py ideal BB84
```
Available configurations: `ideal`, `short`, `long`, `noisy`  
Available protocols: `BB84`, `B92`, `E91`, `BBM92`

**Option C - Quick Test:**
```cmd
python quick_test.py
```

**Option D - Compare Protocols:**
```cmd
python compare_protocols.py
```

## Usage

### Running the GUI Application

```cmd
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

### Python Environment Issues

**Issue**: `python` command not recognized
```
'python' is not recognized as an internal or external command
```
**Solution**: 
1. Make sure Python is installed
2. Add Python to PATH:
   - Windows: Search "Environment Variables" → Edit PATH → Add Python installation directory
   - Or reinstall Python and check "Add Python to PATH" during installation

**Issue**: Multiple Python versions installed
**Solution**: 
- Use `py -3` or `py -3.10` to specify version
- Or use virtual environment to isolate project

**Issue**: Virtual environment not activating
**Solution**: 
- For PowerShell: If you get execution policy error, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Then try activating again: `venv\Scripts\activate`

### Package Installation Issues

**Issue**: Import Errors
```
ImportError: No module named 'qiskit'
```
**Solution**: 
1. Make sure virtual environment is activated (if using one)
2. Install required packages:
   ```cmd
   pip install qiskit qiskit-aer numpy matplotlib pillow
   ```

**Issue**: pip install fails with permission error
**Solution**: 
- Use `--user` flag: `pip install --user -r requirements.txt`
- Or use virtual environment (recommended)

**Issue**: Conflicting package versions
**Solution**: 
1. Create a fresh virtual environment
2. Install clean dependencies:
   ```cmd
   python -m venv venv_new
   venv_new\Scripts\activate
   pip install -r requirements.txt
   ```

### Runtime Issues

**Issue**: Slow Simulations
**Symptom**: Large number of qubits takes too long

**Solution**: 
- Start with fewer qubits (10,000 - 100,000)
- Increase for final results
- High losses require more qubits for reliable statistics

**Issue**: Unreliable QBER
**Symptom**: QBER fluctuates heavily between runs

**Solution**: Increase number of qubits to improve statistics

**Issue**: GUI Not Responding
**Symptom**: Application freezes during simulation

**Note**: This is normal for large simulations (Progress bar shows status)
- Use Abort button if needed
- Consider reducing number of qubits

**Issue**: GUI doesn't open or crashes on startup
**Solution**: 
- Make sure tkinter is installed (usually included with Python)
- Try: `python -m tkinter` to test tkinter installation
- Reinstall Python if tkinter is missing

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
