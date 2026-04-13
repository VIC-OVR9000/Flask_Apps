
-----

# Experimental Analysis: Multi-Agent PID Stability

### Subject: Linear Time-Invariant (LTI) System Compensation

**Lead Researcher:** Samuel Victor Flores  
**Research Lab:** Agent Kamaka Computational Dynamics Group

-----

## 🔬 Executive Summary

This project investigates the stability and settling characteristics of four discrete test masses ($M_0$ through $M_3$) within a simulated planar coordinate system. By applying variable coefficients to a **Proportional-Integral-Derivative (PID)** feedback loop, we analyze the system's capacity for **Perturbation Rejection** and its return to a defined null equilibrium point.

## 📐 Mathematical Overview

The core physics engine utilizes a discrete-time integrator to solve the second-order differential equation governing each agent:

$$M \ddot{x} + \beta \dot{x} + \alpha x = F_p(t)$$

### 1\. Control Force Calculation ($F_c$)

The corrective force is derived from the error signal $e(t) = \text{Target} - \text{Current Position}$:

  * **Proportional ($\alpha$):** $e(t) \cdot K_p$ (Restorative stiffness)
  * **Integral ($\gamma$):** $\int e(t)dt \cdot K_i$ (Steady-state error elimination)
  * **Derivative ($\beta$):** $\frac{de}{dt} \cdot K_d$ (Viscous damping)

### 2\. Numerical Snapping & Quenching

To address the "Limit of Zeroes"—the machine epsilon where floating-point errors induce artificial jitter—the system employs a **Hard Threshold Quench**:

> If the Euclidean magnitude $||e(t)|| \le 0.0001$, the state vectors $[x, v, i]$ are snapped to zero. This simulates physical static friction and prevents numerical divergence during extended runtimes.

-----

## 🛠 System Architecture

  * **Computational Backend:** A Python/Flask engine performing Euler integration at 20Hz.
  * **Laboratory UI:** A monochromatic technical report interface designed for high-contrast data visualization.
  * **Telemetry (Figure 1.0):** Real-time plotting of **Directional Error Magnitude** calculated as $||e(t)|| \cdot \text{sgn}(e_y)$. This allows for precise observation of overshoot and oscillation damping.

-----

## 🎮 User Instructions: Perturbation Mapping

Researchers can manually induce external forces ($F_p$) to test the compensator's resilience using the following hardware mappings:

| Unit | Identification | Primary Control Set |
| :--- | :--- | :--- |
| **Test Mass 0** | $M_0$ (Black) | `W` `A` `S` `D` |
| **Test Mass 1** | $M_1$ (Dk Gray) | `T` `F` `G` `H` |
| **Test Mass 2** | $M_2$ (Lt Gray) | `I` `J` `K` `L` |
| **Test Mass 3** | $M_3$ (White) | **Numpad** `8` `4` `5` `6` |

### Experimental Procedure

1.  **Initialize:** Set Coefficients to baseline: $K_p: 1.07$, $K_d: 0.73$, $K_i: 0.03$.
2.  **Perturb:** Apply a directional force using the keyboard mapping.
3.  **Analyze:** Observe Figure 1.0 for the **Rise Time** and **Settling Time**. If "ringing" occurs, increase **Coefficient $\beta$**.

-----

\<div align="center"\>
\<img src="PID_controller_4/fig1.png" alt="Figure 1.0 Telemetry" width="850"\>
\<p\>\<i\>Figure 1.0: Real-time telemetry showing directional error magnitude and the execution of the 0.0001 numerical snap.\</i\>\</p\>
\</div\>

-----

### ⚠️ Operational Disclaimer

This simulation is a precursor for hardware-level implementation on **STM32** and **Raspberry Pi** platforms. It accurately models the behavior of Darlington-array driven actuators and the necessity of deadband logic in physical robotics. Avoid continuous operation beyond 60 minutes to prevent cumulative floating-point drift.
