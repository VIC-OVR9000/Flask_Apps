The **Laboratory Technical Report** interface has been updated to reflect the new control mapping for **Test Mass 3**. The perturbation logic now specifically listens for **Numpad 8, 4, 5, and 6** to drive the vertical and horizontal vectors for the fourth unit.

### Updated Laboratory Interface (`index.html`)

```html
<div class="legend">
        <span><b>M0:</b> WASD</span> | <span><b>M1:</b> TFGH</span> | 
        <span><b>M2:</b> IJKL</span> | <span><b>M3:</b> NUMPAD 8456</span>
    </div>

<script>
    // ... [Previous Initialization Code] ...

    async function loop() {
        const getPerturbation = (u, l, d, r) => ({
            x: (keys[r] ? 5 : 0) + (keys[l] ? -5 : 0),
            y: (keys[d] ? 5 : 0) + (keys[u] ? -5 : 0)
        });

        const payload = {
            kp: document.getElementById('kp').value,
            kd: document.getElementById('kd').value,
            ki: document.getElementById('ki').value,
            disturbances: [
                getPerturbation('w', 'a', 's', 'd'),
                getPerturbation('t', 'f', 'g', 'h'),
                getPerturbation('i', 'j', 'k', 'l'),
                // Mapping M3 to Numpad 8 (Up), 4 (Left), 5 (Down), 6 (Right)
                getPerturbation('8', '4', '5', '6')
            ]
        };

        // ... [Remaining Loop and Fetch Logic] ...
    }
    loop();
</script>
```

### Revised Project Documentation (`README.md`)

The following technical documentation has been revised to reflect the standardized perturbation inputs and the **Temporal Convergence** logic implemented in the backend.

---

# Experimental Analysis: Multi-Agent PID Stability
### Subject: Linear Time-Invariant (LTI) System Compensation

This repository contains a high-fidelity laboratory simulation designed to analyze the settling characteristics of four test masses ($M_0$ through $M_3$) under variable compensatory feedback.

## 🔬 Computational Methodology
The system models the interaction between **Compensatory Feedback** ($F_c$) and **External Perturbation Forces** ($F_p$). 

### Stability Timer (Zero-Thresholding)
A critical feature of this research is the **Temporal Convergence** check. Rather than assuming an absolute mathematical zero, the system monitors for statistical stability:
* **Thresholding:** When the error magnitude ($||e(t)||$) drops below $0.00001$, a stability timer increments.
* **Recursive Reset:** If the system maintains this threshold for 15 frames, it triggers an automated reset switch, re-perturbing the mass to $y = -150.0$ for repeated step-response analysis.

## 🎮 Operational Procedures
The laboratory allows for independent perturbations via the following localized inputs:

| Unit | Identification | Control Mapping |
| :--- | :--- | :--- |
| **Test Mass 0** | $M_0$ | `W` `A` `S` `D` |
| **Test Mass 1** | $M_1$ | `T` `F` `G` `H` |
| **Test Mass 2** | $M_2$ | `I` `J` `K` `L` |
| **Test Mass 3** | $M_3$ | **Numpad** `8` `4` `5` `6` |



---
**Lead Researcher:** Samuel Victor Flores (The Architect)  
**Research Branch:** SIA-V Sovereign Universe Implementation
