
-----

# Multi-Agent PID Stability Analysis

### Subject: Linear Time-Invariant (LTI) System Compensation

**Lead Researcher:** Samuel Victor Flores  
**Technical Specifications:** HP Z840 Workstation | Debian Linux Environment

-----

## 🔬 Executive Summary

This research evaluates the transient response and steady-state stability of a distributed multi-agent system. By utilizing a **Proportional-Integral-Derivative (PID)** control architecture, the study analyzes the efficacy of various damping and restorative coefficients in maintaining a null equilibrium point against external stochastic perturbations.

## 📐 Mathematical Framework

The simulation environment utilizes a discrete-time Euler integrator (20Hz) to solve the second-order differential equations governing the kinematic state of each agent ($M_0$–$M_3$).

### 1\. Governing Equation of Motion

Each test mass is modeled according to the following dynamic equilibrium:
$$M \ddot{x} + \beta \dot{x} + \alpha x = F_{ext}(t)$$
Where $M$ represents system mass, $\beta$ the viscous damping coefficient, and $\alpha$ the restorative stiffness.

### 2\. Feedback Control Signal ($F_c$)

The corrective force is derived from the error signal $e(t) = \text{Target} - \text{Current Position}$:

  * **Proportional ($\alpha$):** $e(t) \cdot K_p$ modulates the speed of the restorative response.
  * **Integral ($\gamma$):** $\int e(t)dt \cdot K_i$ eliminates residual steady-state error.
  * **Derivative ($\beta$):** $\frac{de}{dt} \cdot K_d$ suppresses high-frequency oscillations (ringing).

### 3\. Numerical Snapping and State Quenching

To mitigate numerical instability at the machine epsilon boundary ($10^{-16}$), the system implements a **Hard Threshold Deadband**:

> If $||e(t)|| \le 0.0001$, the state vectors $[x, v, i]$ are programmatically snapped to zero. This simulates physical static friction and ensures a stable steady-state baseline for longitudinal analysis.

-----

## 🛠 System Implementation & Telemetry

  * **Architecture:** Decoupled Python/Flask computational backend with a high-contrast Laboratory UI.
  * **Telemetry Mapping:** Figure 1.0 visualizes **Directional Error Magnitude**, defined as $||e(t)|| \cdot \text{sgn}(e_y)$. This polarization allows for the precise observation of overshoot relative to the equilibrium axis.

-----

## 🎮 Operational Parameters: Perturbation Mapping

Manual perturbations ($F_{ext}$) are induced via localized hardware inputs to test compensatory resilience:

| Agent | Identification | Control Mapping |
| :--- | :--- | :--- |
| **Mass 0** | $M_0$ (Black) | `W` `A` `S` `D` |
| **Mass 1** | $M_1$ (Dk Gray) | `T` `F` `G` `H` |
| **Mass 2** | $M_2$ (Lt Gray) | `I` `J` `K` `L` |
| **Mass 3** | $M_3$ (White) | **Numpad** `8` `4` `5` `6` |

-----

#\<div align="center"\>
#\<img src="PID\_controller\_4/fig1.png" alt="Figure 1.0: Stability Analysis" width="850"\>
#\<p\>\<i\>\<b\>Figure 1.0:\</b\> Transient response telemetry for Agent $M_3$. The plot illustrates the transition from an underdamped state to absolute equilibrium via the 0.0001 numerical snap.\</i\>\</p\>
#\</div\>

-----

### ⚠️ Technical Disclaimer

This simulation serves as a computational precursor for hardware-level implementation on **STM32** and **embedded architectures**. The deadband logic successfully models the requirements of Darlington-array driven actuators. Prolonged execution may lead to cumulative floating-point drift; periodic system resets are recommended.
