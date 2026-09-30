# 1D Premixed Methane-Air Combustion Simulation
## Numerical Study using Detailed Chemical Kinetics (Cantera & GRI-Mech 3.0)

**Presenter:** [Your Name / Roll No]  
**Course / Department:** Combustion / Thermal Engineering  

---

### Slide 1: Problem Definition & Objectives

#### Objective
- Model and analyze a stationary, **1D freely-propagating premixed laminar methane-air flame**.
- Investigate the effect of mixture strength (equivalence ratio $\phi = 0.70$ to $1.30$) on flame dynamics.

#### Key Physical Quantities Evaluated
- **Laminar Flame Speed ($S_L$)**
- **Adiabatic & Peak Flame Temperatures ($T_{max}$)**
- **Spatial Structure:** Preheat layer, chemical reaction zone, and radical pool ($OH, H, O$).
- **Dominant elementary chemical reactions** driving heat release and flame propagation.

---

### Slide 2: Computational Model & Governing Equations

#### Configuration
- **Domain:** 1D planar flow, width $L = 30\text{ mm}$ ($0.03\text{ m}$).
- **Boundary Conditions:**
  - Inlet ($x = 0$): $T_u = 300\text{ K}$, $P = 1\text{ atm}$, unburned fuel-air mixture.
  - Outlet ($x = L$): Zero-gradient Neumann condition ($\partial / \partial x = 0$) for burned equilibrium products.

#### Governing Equations Solved
1. **Continuity:**
   $$\frac{d(\rho u)}{dx} = 0 \implies \dot{m} = \rho u = \text{constant}$$
2. **Species Conservation (for all 53 species):**
   $$\dot{m}\frac{d Y_k}{dx} = -\frac{d j_k}{dx} + \dot{\omega}_k W_k$$
3. **Energy Conservation:**
   $$\dot{m} c_p \frac{dT}{dx} = \frac{d}{dx}\left(\lambda \frac{dT}{dx}\right) - \sum_k j_k c_{p,k} \frac{dT}{dx} - \sum_k h_k \dot{\omega}_k W_k$$

---

### Slide 3: Chemical Kinetic Mechanism & Solver Setup

#### Kinetic Model: GRI-Mech 3.0
- **53 chemical species**, **325 elementary reactions**.
- Standard benchmark for methane ($CH_4$) oxidation.
- Includes thermal, prompt, and intermediate nitrogen chemistry ($NO_x$ precursors).

#### Numerical Method (Cantera BVP Solver)
- **Eigenvalue Problem:** Flame speed $S_L = u(0)$ is solved iteratively as an eigenvalue via damped Newton-Raphson method.
- **Adaptive Grid Refinement:**
  - Starts with a coarse 16-point mesh.
  - Automatically inserts grid points based on local gradient (`slope = 0.05`) and curvature (`curve = 0.08`).
  - Final converged grids: **196 to 236 non-uniform points** clustered tightly inside the reaction zone.

---

### Slide 4: Results — Flame Speed & Temperature vs Mixture Strength ($\phi$)

*(Insert Graph: `01_summary_vs_phi.png`)*

#### Summary Data Table
| Equivalence Ratio ($\phi$) | Mixture Regime | Flame Speed $S_L$ [cm/s] | Peak Temperature [K] | Thermal Thickness [mm] |
|:---:|:---:|:---:|:---:|:---:|
| 0.70 | Lean | 19.44 | 1841.4 | 0.66 |
| 0.80 | Lean | 27.35 | 2001.6 | 0.53 |
| 0.90 | Lean | 34.03 | 2139.3 | 0.46 |
| **1.00** | **Stoichiometric** | **38.09** | **2230.7** | **0.44** |
| **1.10** | **Slightly Rich** | **38.36 (Peak)** | **2213.4** | **0.43** |
| 1.20 | Rich | 33.68 | 2134.3 | 0.46 |
| 1.30 | Rich | 23.64 | 2054.1 | 0.62 |

#### Physical Observations
- **Temperature peaks at $\phi = 1.00$ ($2230.7\text{ K}$):** Complete stoichiometric conversion with minimal excess air dilution.
- **Flame speed peaks at $\phi = 1.10$ ($38.36\text{ cm/s}$):** Slightly rich conditions maximize the radical pool ($H, OH$), increasing the overall chemical reaction rate.

---

### Slide 5: Results — Flame Physical Structure Overview

*(Insert Graph: `02_physical_overview.png`)*

#### Reference Case: $\phi = 1.00$
- **Inflow state:** $T_u = 300\text{ K}$, $u_u = 0.38\text{ m/s}$, $\rho_u = 1.13\text{ kg/m}^3$.
- **Burned state:** $T_b = 2230.7\text{ K}$, $u_b = 2.87\text{ m/s}$, $\rho_b = 0.15\text{ kg/m}^3$.

#### Key Physical Regions Identified
1. **Preheat Zone ($x < 21.06\text{ mm}$):** Heat conducted upstream from the flame heats the cold reactants from $300\text{ K}$ to $\sim 1300\text{ K}$ without significant fuel consumption.
2. **Reaction Zone ($21.06\text{ mm} \le x \le 21.41\text{ mm}$):**
   - High volumetric heat release rate (peaks at $4.50\text{ GW/m}^3$).
   - Thickness: $\delta_{rxn} \approx 352\ \mu\text{m}$ (less than $0.4\text{ mm}$!).
3. **Burned Equilibrium Zone ($x > 21.41\text{ mm}$):** Hot products achieve thermodynamic equilibrium. Gas velocity accelerates by a factor of $\sim 7.5\times$ to conserve mass flux ($\rho u = \text{const}$).

---

### Slide 6: Results — Species Profiles & Radical Pool

*(Insert Graphs: `03_major_species.png` & `04_radicals_log_scale.png`)*

#### Major Species Evolution
- $CH_4$ and $O_2$ remain unreacted throughout the preheat zone.
- Rapid depletion occurs inside the $350\ \mu\text{m}$ reaction layer.
- $CO$ acts as an essential intermediate, peaking in the reaction zone before oxidizing to $CO_2$.
- $CO_2$ and $H_2O$ reach equilibrium plateaus downstream.

#### Radical Pool ($OH, H, O, HO_2$)
- Radical mole fractions are low ($10^{-3}$ to $10^{-6}$), requiring logarithmic representation.
- Concentrations peak sharply inside the heat release zone.
- Radicals diffuse upstream into the preheat zone, initiating low-temperature fuel breakdown.

---

### Slide 7: Results — Chemical Kinetics & Reaction Diagnostics

*(Insert Graphs: `05_species_production_rates.png` & `06_top_reactions.png`)*

#### Primary Governing Elementary Reactions
1. **Chain Branching (Flame Speed Governor):**
   $$\text{H} + \text{O}_2 \rightleftharpoons \text{O} + \text{OH}$$
   *(Converts one radical into two; critical for flame propagation).*
2. **Main Exothermic Heat Release:**
   $$\text{CO} + \text{OH} \rightleftharpoons \text{CO}_2 + \text{H}$$
   *(Accounts for the majority of the chemical heat release in hydrocarbon combustion).*
3. **Radical Recombination:**
   $$\text{H} + \text{OH} + \text{M} \rightleftharpoons \text{H}_2\text{O} + \text{M}$$

---

### Slide 8: Multi-Equivalence Ratio Comparison

*(Insert Graph: `08_multi_phi_profiles.png`)*

#### Comparative Insights Across $\phi$
- **Reaction Zone Thickness:**
  - Near stoichiometric ($\phi = 1.0 - 1.1$), thermal thickness is minimum ($\approx 0.43\text{ mm}$).
  - In lean ($\phi = 0.7$) and rich ($\phi = 1.3$) mixtures, the reaction zone widens significantly ($\approx 0.62 - 0.66\text{ mm}$).
- **Flame Speed Correlation:**
  - Thinner reaction zone $\longleftrightarrow$ Higher temperature gradient $\longleftrightarrow$ Faster laminar flame speed.

---

### Slide 9: Model Validation Against Standard Literature

#### Numerical Checks Performed
1. **Laminar Flame Speed ($S_L$):**
   - GRI-Mech 3.0 literature benchmark: $38.0 - 39.0\text{ cm/s}$ at $\phi = 1.0$.
   - **Our Simulation:** **$38.09\text{ cm/s}$** ($\Delta < 0.2\%$).
2. **Adiabatic Flame Temperature ($T_{ad}$):**
   - Literature equilibrium calculation: $\sim 2225 - 2235\text{ K}$.
   - **Our Simulation:** **$2230.7\text{ K}$** (Thermodynamic equilibrium fully satisfied).
3. **Mass Flux Conservation:**
   - $\rho_u u_u = 1.13\text{ kg/m}^3 \times 0.3809\text{ m/s} = 0.430\text{ kg/(m}^2\cdot\text{s})$.
   - $\rho_b u_b = 0.15\text{ kg/m}^3 \times 2.871\text{ m/s} = 0.430\text{ kg/(m}^2\cdot\text{s})$.
   - Error: $0.00\%$.

---

### Slide 10: Conclusions

1. **Successful 1D Flame Modeling:** Successfully simulated freely-propagating laminar methane-air flames across $\phi = 0.70$ to $1.30$ using detailed GRI-Mech 3.0 chemistry.
2. **Peak Phenomena Discrepancy:**
   - Maximum temperature occurs at **$\phi = 1.00$** ($2230.7\text{ K}$).
   - Maximum flame speed occurs at slightly rich **$\phi = 1.10$** ($38.36\text{ cm/s}$) due to radical enhancement.
3. **Distinct Flame Layers:** Quantified that the chemical reaction zone is extremely thin ($\approx 352\ \mu\text{m}$), preceded by a convective-diffusive preheat zone.
4. **Validation:** All calculated speeds, temperatures, and mass fluxes accurately match standard literature data.

---

### Questions & Discussion
*Thank You.*
