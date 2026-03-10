"""
GUI for QKD Simulator
Creates a two-tab interface for single and multiple simulations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading
from qkd_simulator import QKDSimulator
from qiskit.visualization import circuit_drawer
import PIL.Image
import PIL.ImageTk


class QKDSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QKD Simulator")
        self.root.geometry("1200x700")
        
        self.simulator = QKDSimulator()
        self.abort_flag = False
        self.sample_circuit = None
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.single_tab = ttk.Frame(self.notebook)
        self.multiple_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.single_tab, text='Single simulation')
        self.notebook.add(self.multiple_tab, text='Multiple simulations')
        
        self.create_single_simulation_tab()
        self.create_multiple_simulation_tab()
        
    def create_single_simulation_tab(self):
        """Create the single simulation tab with two rows"""
        
        # Row 0: System Parameters and Simulation Settings
        left_frame = ttk.Frame(self.single_tab, padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5)
        
        middle_frame = ttk.Frame(self.single_tab, padding="10")
        middle_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5)
        
        # Row 1: Results for all 4 protocols
        results_row_frame = ttk.Frame(self.single_tab, padding="10")
        results_row_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=10)
        
        # Progress bar at bottom
        self.progress_frame = ttk.Frame(self.single_tab)
        self.progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.E, tk.W), pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, 
                                           maximum=100, mode='determinate')
        self.progress_bar.pack(fill='x', padx=10)
        
        # Configure column weights
        self.single_tab.columnconfigure(0, weight=1)
        self.single_tab.columnconfigure(1, weight=1)
        self.single_tab.rowconfigure(0, weight=1)
        self.single_tab.rowconfigure(1, weight=1)
        
        # LEFT COLUMN - System Parameters
        ttk.Label(left_frame, text="System parameters", font=('Arial', 12, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=10)
        
        self.system_params = {}
        params_config = [
            ("Source generation rate", "72.60 MHz", "source_rate", "MHz"),
            ("Source efficiency", "5.00 %", "source_efficiency", "%"),
            ("Fiber length", "18.00 km", "fiber_length", "km"),
            ("Fiber loss", "0.53 db/km", "fiber_loss", "db/km"),
            ("Detector efficiency", "11.00 %", "detector_efficiency", "%"),
            ("Perturb probability", "5.00 %", "perturb_prob", "%"),
            ("SOP mean deviation", "0.13 rad", "sop_deviation", "rad")
        ]
        
        row = 1
        for label, default, key, unit in params_config:
            ttk.Label(left_frame, text=label).grid(row=row, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(left_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=row, column=1, pady=5, padx=5)
            self.system_params[key] = (entry, unit)
            row += 1
        
        # MIDDLE COLUMN - Simulation Settings
        ttk.Label(middle_frame, text="Simulation settings", font=('Arial', 12, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=10)
        
        row = 1
        
        # Checkboxes for enabling features
        self.losses_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(middle_frame, text="Losses enabled", variable=self.losses_enabled).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        self.perturb_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(middle_frame, text="Perturbations enabled", variable=self.perturb_enabled).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        self.eavesdrop_enabled = tk.BooleanVar(value=False)
        ttk.Checkbutton(middle_frame, text="Eavesdropping enabled", variable=self.eavesdrop_enabled).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        self.sop_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(middle_frame, text="SOP uncertainty enabled", variable=self.sop_enabled).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Number of qubits
        ttk.Label(middle_frame, text="Number of qubits").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.n_qubits_entry = ttk.Entry(middle_frame, width=15)
        self.n_qubits_entry.insert(0, "1000000")
        self.n_qubits_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1
        
        # QBER cross-check fraction
        ttk.Label(middle_frame, text="QBER cross-check fraction").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.qber_fraction_entry = ttk.Entry(middle_frame, width=15)
        self.qber_fraction_entry.insert(0, "10.00 %")
        self.qber_fraction_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1
        
        # Buttons
        ttk.Button(middle_frame, text="Run simulation", command=self.run_single_simulation).grid(
            row=row, column=0, columnspan=2, pady=20, sticky=(tk.E, tk.W))
        row += 1
        
        ttk.Button(middle_frame, text="View sample", command=self.view_sample).grid(
            row=row, column=0, columnspan=2, pady=5, sticky=(tk.E, tk.W))
        row += 1
        
        ttk.Button(middle_frame, text="Abort", command=self.abort_simulation).grid(
            row=row, column=0, columnspan=2, pady=5, sticky=(tk.E, tk.W))
        
        # RESULTS ROW - 4 columns for 4 protocols
        protocols = ["BB84", "B92", "E91", "BBM92"]
        self.results_labels = {}
        
        for col, protocol in enumerate(protocols):
            # Create frame for each protocol
            protocol_frame = ttk.Frame(results_row_frame, padding="10", relief="groove", borderwidth=2)
            protocol_frame.grid(row=0, column=col, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5)
            results_row_frame.columnconfigure(col, weight=1)
            
            # Protocol header
            ttk.Label(protocol_frame, text=protocol, font=('Arial', 14, 'bold')).grid(
                row=0, column=0, columnspan=2, pady=10)
            
            # Results for this protocol
            self.results_labels[protocol] = {}
            results_config = [
                ("Key length", "key_length", ""),
                ("Key rate", "key_rate", "Hz"),
                ("QBER", "qber", "%"),
                ("S", "s_statistic", ""),
                ("Combined efficiency", "combined_efficiency", "%")
            ]
            
            result_row = 1
            for label, key, unit in results_config:
                ttk.Label(protocol_frame, text=label).grid(row=result_row, column=0, sticky=tk.W, pady=3, padx=5)
                result_label = ttk.Label(protocol_frame, text="-", font=('Arial', 9))
                result_label.grid(row=result_row, column=1, sticky=tk.E, pady=3, padx=5)
                self.results_labels[protocol][key] = (result_label, unit)
                result_row += 1
    
    def create_multiple_simulation_tab(self):
        """Create the multiple simulations tab"""
        
        # Left side - Parameters
        left_frame = ttk.Frame(self.multiple_tab, padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Right side - Plot
        right_frame = ttk.Frame(self.multiple_tab, padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Progress bar
        progress_frame = ttk.Frame(self.multiple_tab)
        progress_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.E, tk.W), pady=5)
        
        self.multi_progress_var = tk.DoubleVar()
        self.multi_progress_bar = ttk.Progressbar(progress_frame, variable=self.multi_progress_var,
                                                 maximum=100, mode='determinate')
        self.multi_progress_bar.pack(fill='x', padx=10)
        
        # Configure weights
        self.multiple_tab.columnconfigure(0, weight=1)
        self.multiple_tab.columnconfigure(1, weight=2)
        self.multiple_tab.rowconfigure(0, weight=1)
        
        # Parameters section
        ttk.Label(left_frame, text="Parameters", font=('Arial', 12, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=10)
        
        row = 1
        
        # Select x parameter
        ttk.Label(left_frame, text="Select x parameter").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.x_param_var = tk.StringVar(value="Fiber loss")
        x_param_combo = ttk.Combobox(left_frame, textvariable=self.x_param_var, width=20, state='readonly',
                                    values=["Source generation rate", "Source efficiency", "Fiber length",
                                           "Fiber loss", "Detector efficiency", "Perturb probability",
                                           "SOP mean deviation", "QBER cross-check fraction"])
        x_param_combo.grid(row=row, column=1, pady=5, padx=5)
        row += 1
        
        # Select y parameter
        ttk.Label(left_frame, text="Select y parameter").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.y_param_var = tk.StringVar(value="Key length")
        y_param_combo = ttk.Combobox(left_frame, textvariable=self.y_param_var, width=20, state='readonly',
                                    values=["Key length", "Key rate", "QBER", "Combined efficiency"])
        y_param_combo.grid(row=row, column=1, pady=5, padx=5)
        row += 1
        
        # Start value
        ttk.Label(left_frame, text="Start value x").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.start_value_entry = ttk.Entry(left_frame, width=22)
        self.start_value_entry.insert(0, "0.00 dB/km")
        self.start_value_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1
        
        # End value
        ttk.Label(left_frame, text="End value x").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.end_value_entry = ttk.Entry(left_frame, width=22)
        self.end_value_entry.insert(0, "1.00 dB/km")
        self.end_value_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1
        
        # Number of points
        ttk.Label(left_frame, text="Number of points").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.n_points_entry = ttk.Entry(left_frame, width=22)
        self.n_points_entry.insert(0, "10")
        self.n_points_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1
        
        # Buttons
        ttk.Button(left_frame, text="Run simulations", command=self.run_multiple_simulations).grid(
            row=row, column=0, columnspan=2, pady=20, sticky=(tk.E, tk.W))
        row += 1
        
        ttk.Button(left_frame, text="Abort", command=self.abort_simulation).grid(
            row=row, column=0, columnspan=2, pady=5, sticky=(tk.E, tk.W))
        
        # Plot section
        ttk.Label(right_frame, text="Results", font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.fig = Figure(figsize=(10, 7), dpi=100)
        protocols = ["BB84", "B92", "E91", "BBM92"]
        self.axes = {}
        for idx, protocol in enumerate(protocols):
            ax = self.fig.add_subplot(2, 2, idx + 1)
            ax.set_title(protocol, fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
            self.axes[protocol] = ax
        self.fig.tight_layout(pad=2.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def parse_value(self, entry_widget, unit_type):
        """Parse value from entry widget and convert to float"""
        value_str = entry_widget.get().strip()
        # Remove units (order matters: remove compound units before single units)
        value_str = value_str.replace('dB/km', '').replace('db/km', '').replace('MHz', '').replace('%', '').replace('km', '').replace('rad', '').strip()
        try:
            value = float(value_str)
            # Convert percentages to fractions
            if unit_type == '%':
                value = value / 100.0
            return value
        except ValueError:
            raise ValueError(f"Invalid value: {entry_widget.get()}")
    
    def get_simulation_params(self):
        """Gather all simulation parameters"""
        params = {}
        
        # System parameters
        for key, (entry, unit) in self.system_params.items():
            params[key] = self.parse_value(entry, unit)
        
        # Simulation settings
        params['n_qubits'] = int(self.n_qubits_entry.get())
        params['qber_fraction'] = self.parse_value(self.qber_fraction_entry, '%')
        params['losses_enabled'] = self.losses_enabled.get()
        params['perturb_enabled'] = self.perturb_enabled.get()
        params['eavesdropping'] = self.eavesdrop_enabled.get()
        params['sop_enabled'] = self.sop_enabled.get()
        
        return params
    
    def run_single_simulation(self):
        """Run simulations for all 4 protocols"""
        self.abort_flag = False
        
        try:
            params = self.get_simulation_params()
            
            # Clear previous results for all protocols
            for protocol in ["BB84", "B92", "E91", "BBM92"]:
                for key, (label, unit) in self.results_labels[protocol].items():
                    label.config(text="-")
            
            # Run in thread
            thread = threading.Thread(target=self._run_all_protocols_thread, args=(params,))
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _run_all_protocols_thread(self, params):
        """Thread function for running all 4 protocols"""
        protocols = ["BB84", "B92", "E91", "BBM92"]
        try:
            for i, protocol in enumerate(protocols):
                if self.abort_flag:
                    self.progress_var.set(0)
                    return
                
                # Update progress (each protocol gets 25% of the bar)
                self.progress_var.set(i * 25)
                
                # Run simulation for this protocol
                if protocol == "BB84":
                    results = self.simulator.simulate_bb84(params)
                elif protocol == "B92":
                    results = self.simulator.simulate_b92(params)
                elif protocol == "E91":
                    results = self.simulator.simulate_e91(params)
                elif protocol == "BBM92":
                    results = self.simulator.simulate_bbm92(params)
                
                # Update results for this protocol
                self.root.after(0, self._update_protocol_results, protocol, results)
                
                # Update progress after completion
                self.progress_var.set((i + 1) * 25)
            
            # Generate sample circuit for BB84
            self.sample_circuit = self.simulator.get_sample_circuit("BB84", params)
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", str(e))
        finally:
            self.progress_var.set(0)
    
    def _update_protocol_results(self, protocol, results):
        """Update result labels for a specific protocol"""
        for key, (label, unit) in self.results_labels[protocol].items():
            value = results.get(key)
            if value is None:
                label.config(text="-")
            elif key == 'key_rate':
                # Format with thousands separator
                label.config(text=f"{value:,.0f} {unit}")
            elif key == 'key_length':
                label.config(text=f"{int(value)}")
            elif key == 's_statistic':
                if value is not None:
                    label.config(text=f"{value:.2f}")
                else:
                    label.config(text="-")
            else:
                label.config(text=f"{value:.2f} {unit}")
    
    def view_sample(self):
        """Display sample circuit in new window"""
        if self.sample_circuit is None:
            messagebox.showwarning("Warning", "No circuit available. Run a simulation first.")
            return
        
        # Create new window
        window = tk.Toplevel(self.root)
        window.title("Sample Circuit")
        window.geometry("1000x600")
        
        try:
            # Draw circuit
            circuit_drawer(self.sample_circuit, output='mpl', style={'name': 'iqp'})
            
            fig = plt.gcf()
            fig.set_size_inches(12, 6)
            
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not display circuit: {str(e)}")
            window.destroy()
    
    def abort_simulation(self):
        """Abort ongoing simulation"""
        self.abort_flag = True
        self.progress_var.set(0)
        self.multi_progress_var.set(0)
    
    def run_multiple_simulations(self):
        """Run multiple simulations with varying parameter"""
        self.abort_flag = False
        
        try:
            # Get parameters
            x_param = self.x_param_var.get()
            y_param = self.y_param_var.get()
            
            start_str = self.start_value_entry.get().strip()
            end_str = self.end_value_entry.get().strip()
            
            # Parse start and end values
            start_val = float(start_str.split()[0])
            end_val = float(end_str.split()[0])
            n_points = int(self.n_points_entry.get())
            
            # Map parameter names to internal keys
            param_map = {
                "Source generation rate": "source_rate",
                "Source efficiency": "source_efficiency",
                "Fiber length": "fiber_length",
                "Fiber loss": "fiber_loss",
                "Detector efficiency": "detector_efficiency",
                "Perturb probability": "perturb_prob",
                "SOP mean deviation": "sop_deviation",
                "QBER cross-check fraction": "qber_fraction"
            }
            
            result_map = {
                "Key length": "key_length",
                "Key rate": "key_rate",
                "QBER": "qber",
                "Combined efficiency": "combined_efficiency"
            }
            
            x_key = param_map[x_param]
            y_key = result_map[y_param]
            
            # Run in thread
            thread = threading.Thread(target=self._run_multiple_thread,
                                     args=(x_key, y_key, start_val, end_val, n_points))
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _run_multiple_thread(self, x_key, y_key, start_val, end_val, n_points):
        """Thread function for running multiple simulations across all 4 protocols"""
        protocols = ["BB84", "B92", "E91", "BBM92"]
        simulate_fn = {
            "BB84": self.simulator.simulate_bb84,
            "B92": self.simulator.simulate_b92,
            "E91": self.simulator.simulate_e91,
            "BBM92": self.simulator.simulate_bbm92,
        }
        try:
            # Generate x values
            x_values = [start_val] if n_points == 1 else list(np.linspace(start_val, end_val, n_points))
            
            # y_values_all[protocol] grows as simulations complete
            y_values_all = {p: [] for p in protocols}
            
            base_params = self.get_simulation_params()
            total_steps = n_points * len(protocols)
            step = 0
            
            for i, x_val in enumerate(x_values):
                if self.abort_flag:
                    break
                
                # Build params for this x value
                params = dict(base_params)
                params[x_key] = x_val / 100.0 if x_key in ['source_efficiency', 'detector_efficiency', 'perturb_prob', 'qber_fraction'] else x_val
                
                for protocol in protocols:
                    if self.abort_flag:
                        break
                    results = simulate_fn[protocol](params)
                    y_values_all[protocol].append(results[y_key])
                    step += 1
                    self.multi_progress_var.set(step / total_steps * 100)
                
                # Update all 4 plots with data collected so far
                self.root.after(0, self._update_plot,
                                x_values[:i + 1],
                                {p: list(y_values_all[p]) for p in protocols},
                                x_key, y_key)
            
            if not self.abort_flag:
                self.multi_progress_var.set(100)
            else:
                self.multi_progress_var.set(0)
                
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", str(e))
        finally:
            if not self.abort_flag:
                self.root.after(1000, lambda: self.multi_progress_var.set(0))
    
    def _update_plot(self, x_values, y_values_all, x_label, y_label):
        """Update all 4 protocol subplots with new data"""
        colors = {"BB84": "steelblue", "B92": "darkorange", "E91": "forestgreen", "BBM92": "crimson"}
        for protocol, ax in self.axes.items():
            ax.clear()
            ax.set_title(protocol, fontsize=11, fontweight='bold')
            y_vals = y_values_all.get(protocol, [])
            if y_vals:
                ax.plot(x_values[:len(y_vals)], y_vals,
                        color=colors[protocol], linewidth=2, marker='o', markersize=4)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.grid(True, alpha=0.3)
        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = QKDSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
