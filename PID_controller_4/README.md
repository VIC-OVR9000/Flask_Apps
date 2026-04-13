
***

# Experimental Analysis: Multi-Agent PID Stability
### Subject: Linear Time-Invariant (LTI) System Compensation

This repository contains a discrete-time simulation environment designed to analyze the stability and settling characteristics of multiple test masses ($M_0$ through $M_3$) under variable compensatory feedback.

## 🔬 Computational Methodology

The system models the interaction between **Compensatory Feedback** ($F_c$) and **External Perturbation Forces** ($F_p$). Each test mass follows second-order differential dynamics, integrating velocity and position at a 20Hz refresh rate.

### Numerical Snapping (The 0.0001 Limit)
A critical feature of this implementation is the **Surgical Quenching** logic, designed to manage the precision floor of the digital controller:

* **The Threshold:** When the raw error magnitude drops below **0.0001**, the system identifies the mass as having reached its null equilibrium point.
* **State Override:** To prevent "Machine Epsilon" jitter, the system snaps the mass to the target coordinates ($x, y$) and instantly zero-thresholds the velocity vectors ($v_x, v_y$).
* **Integral Reset:** The accumulative error integral ($i_x, i_y$) is cleared upon snapping. This prevents "ghost forces" from releasing when the next perturbation is applied.

## 🛠 System Architecture

* **Computational Backend:** A Flask-based engine performing Euler integration. It utilizes directional magnitude calculations—`raw_mag * (ey/abs(ey))`—to provide polarized telemetry for overshoot analysis.
* **Laboratory Interface:** A formal technical report view featuring an engineering grid and high-fidelity real-time telemetry.
* **Figure 1.0:** A Chart.js implementation visualizing the directional error magnitude, allowing researchers to observe the damping effect of $\beta$ in real-time.

## 🎮 Operational Procedures

The laboratory allows for independent, real-time perturbations via localized inputs:

| Unit | ID | Identification | Control Mapping |
| :--- | :--- | :--- | :--- |
| **Test Mass 0** | $M_0$ | Black | `W` `A` `S` `D` |
| **Test Mass 1** | $M_1$ | Dk Gray | `T` `F` `G` `H` |
| **Test Mass 2** | $M_2$ | Lt Gray | `I` `J` `K` `L` |
| **Test Mass 3** | $M_3$ | White | **Numpad** `8` `4` `5` `6` |

## 📐 Experimental Parameters

* **Coefficient $\alpha$ (P-Gain):** Restorative "stiffness" relative to the target station.
* **Coefficient $\beta$ (D-Damp):** Viscous friction applied to the derivative of the error to suppress ringing.
* **Coefficient $\gamma$ (I-Int):** Accumulative feedback used to eliminate steady-state offsets.

---

### ⚠️ Operational Note
The "Numerical Snapping" logic ensures that the system reaches a true rest state. However, researchers should observe the **Figure 1.0** chart for high-frequency oscillations prior to the $0.0001$ snap, as these indicate an underdamped system ($\beta$ is too low).

---
**Lead Researcher:** Samuel Victor Flores (The Architect)  
**Research Branch:** SIA-V Sovereign Universe Implementation



## 📘 User Operational Instructions

The simulation is designed as a repetitive step-response experiment. Follow these procedures to analyze the stability of the fleet:

### 1. Initial Setup
* **Startup:** Ensure the Flask server is running on `port 8011`.
* **Environment:** Open the browser to the local host. The masses will initialize at $y = -0.0001$ to test immediate low-threshold stability.

### 2. Perturbation Inputs (Inducing Error)
To study the recovery dynamics, apply external force vectors using the localized control mappings:
* **Mass 0-2:** Standard WASD, TFGH, and IJKL mappings.
* **Mass 3:** Use the **Numpad** keys (`8` Up, `4` Left, `5` Down, `6` Right).
* **Action:** Apply a sustained perturbation to move a mass away from its station, then release to observe the **Settling Time**.

### 3. Tuning the Coefficients
Adjust the sliders in the **Control Panel** to modify the fleet's personality:
* **Increase $\alpha$ (P-Gain):** If the mass returns too slowly to the station.
* **Increase $\beta$ (D-Damp):** If the mass "rings" or oscillates around the station after release.
* **Increase $\gamma$ (I-Int):** If the mass stops short of the station (Steady-State Error) due to friction or persistent external force.

---

## 📐 Mathematical Overview: The Physics Engine

The `app.py` backend functions as a discrete-time integrator for a **Second-Order Linear Time-Invariant (LTI) System**.



### 1. The Error Signal ($e$)
The engine calculates the instantaneous displacement from the null equilibrium point:
$$e(t) = Target - CurrentPosition$$

### 2. The Feedback Control Force ($F_c$)
The total corrective force applied to the test mass is the sum of three components:
$$F_c = (e \cdot K_p) + (\int e \, dt \cdot K_i) + (\frac{de}{dt} \cdot K_d)$$

* **Proportional:** Corrects based on current position.
* **Integral:** Corrects based on accumulated past error (eliminates offset).
* **Derivative:** Corrects based on predicted future error (provides damping).

### 3. Numerical Snapping & Quenching
To resolve the **"Limit of Zeroes"** irony, we implement a hard floor for the Euclidean magnitude ($||e(t)|| = \sqrt{e_x^2 + e_y^2}$):

$$\text{If } ||e(t)|| \le 0.0001 \rightarrow \text{Set } [v, i, e] = 0$$

This "Snapping" logic simulates physical static friction. It prevents the controller from attempting to solve for values smaller than the precision limits of the system, effectively quenching all kinetic energy ($E_k = \frac{1}{2}mv^2$) once the mass is "close enough" to be considered at rest.



### 4. Telemetry Polarity
The error magnitude shown in **Figure 1.0** is polarized using the sign of the vertical displacement:
$$Telemetry = ||e(t)|| \cdot \text{sgn}(e_y)$$
This allows you to see on the chart whether the mass overshot the station (crossing the zero line) or merely approached it from one side.




