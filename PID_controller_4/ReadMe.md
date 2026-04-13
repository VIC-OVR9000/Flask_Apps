# Experimental Analysis: Multi-Agent PID Stability
### Subject: Linear Time-Invariant (LTI) System Compensation

This repository contains a discrete-time simulation environment designed to analyze the stability and settling characteristics of multiple test masses ($M_0$ through $M_3$) under variable compensatory feedback. The project bridges classical mechanics with modern computational control theory.

## 🔬 Computational Methodology

The system models the interaction between **Compensatory Feedback** ($F_c$) and **External Perturbation Forces** ($F_p$). Each mass is treated as an independent agent governed by a second-order differential equation.

### The Stability Timer (Zero-Thresholding)
A critical feature of this research is the **Temporal Convergence** check, implemented to manage the floating-point limits (Machine Epsilon) inherent in digital controllers:

* **Thresholding:** When the error magnitude ($||e(t)||$) drops below $0.00001$, a stability timer begins incrementing.
* **Recursive Reset:** If the system maintains this threshold for a required duration (15 frames), it assumes statistical equilibrium and triggers a reset switch.
* **Re-Perturbation:** Upon reset, the mass is re-launched to its initial vertical perturbation point ($y = -150.0$), allowing for continuous, automated step-response analysis.

## 🛠 System Architecture

The simulation utilize a decoupled architecture to maintain high-frequency physics integrity:

* **Computational Backend (`App.ipynb`):** A Flask-based physics engine performing Euler integration for four discrete test masses at 20Hz.
* **Laboratory Interface (`index.html`):** A formal technical report view utilizing an engineering grid and real-time telemetry.
* **Figure 1.0 (Telemetry):** A Chart.js implementation that visualizes the Euclidean magnitude of the error vector, essential for calculating settling time and damping ratios.

## 🎮 Operational Procedures

The laboratory allows for independent, real-time perturbations via localized inputs:

| Unit | ID | Identification | Control Mapping |
| :--- | :--- | :--- | :--- |
| **Test Mass 0** | $M_0$ | Black | `W` `A` `S` `D` |
| **Test Mass 1** | $M_1$ | Dk Gray | `T` `F` `G` `H` |
| **Test Mass 2** | $M_2$ | Lt Gray | `I` `J` `K` `L` |
| **Test Mass 3** | $M_3$ | White | **Numpad** `8` `4` `5` `6` |

## 📐 Experimental Parameters

* **Coefficient $\alpha$ (P-Gain):** Modulates the restorative "stiffness" of the null equilibrium.
* **Coefficient $\beta$ (D-Damp):** Applies viscous friction to prevent oscillation and "ringing."
* **Coefficient $\gamma$ (I-Int):** Accumulates historic error to eliminate steady-state offsets.

---

### ⚠️ Stability Disclaimer
Zero-thresholding is manually controlled via the Stability Timer. Running the simulation for extended durations without monitoring may lead to numerical divergence once machine precision limits are reached.

---
**Lead Researcher:** Samuel Victor Flores (The Architect)  
**Research Branch:** SIA-V Sovereign Universe Implementation
