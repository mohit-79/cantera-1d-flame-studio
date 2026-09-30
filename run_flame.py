"""
1D Premixed Methane-Air Laminar Flame Simulation (Cantera)
Enhanced Informative Version with Reaction Zone Detection,
Grid Point Markers, and Full Parametric Sweep Controls.
"""

from pathlib import Path
import cantera as ct
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

# ==============================================================================
# 1. PROJECT CONTROLS (Edit settings here)
# ==============================================================================
T_UNBURNED = 300.0            # Unburned mixture inlet temperature [K]
PRESSURE = float(ct.one_atm)  # 1 atm (101325 Pa)
WIDTH = 0.03                  # 1D domain width: 3 cm [m]
MECHANISM = 'gri30.yaml'      # GRI-Mech 3.0 reaction mechanism

# Equivalence ratios to solve:
# Dense 17-point sweep with step = 0.05 for a super-smooth continuous true curve
PHI_VALUES = [
    0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 
    1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.35
]

# Adaptive Grid Refinement (Controls internal spatial point density)
REFINE_RATIO = 3.0   # Max ratio between adjacent grid spacing
REFINE_SLOPE = 0.05  # Smaller = more points where gradients are high (0.03-0.08)
REFINE_CURVE = 0.08  # Smaller = more points where curvature is high (0.05-0.12)

# Output folders
BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "flame_results"
GRAPH_DIR = OUT_DIR / "graphs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
GRAPH_DIR.mkdir(parents=True, exist_ok=True)

# Species of interest
MAJOR_SPECIES = ['CH4', 'O2', 'CO2', 'H2O', 'CO', 'H2']
RADICAL_SPECIES = ['OH', 'H', 'O', 'HO2']


# ==============================================================================
# 2. SOLVE OR RESTORE FLAME (Automatic Checkpointing)
# ==============================================================================
def solve_or_restore_flame(phi: float):
    tag = f"phi_{phi:.2f}".replace('.', 'p')
    yaml_checkpoint = OUT_DIR / f"{tag}_solution.yaml"
    csv_profile = OUT_DIR / f"{tag}_profile.csv"

    gas = ct.Solution(MECHANISM)
    flame = ct.FreeFlame(gas, width=WIDTH)

    # Resume from checkpoint if it already exists
    if yaml_checkpoint.exists():
        print(f"--> [phi={phi:.2f}] Existing checkpoint found. Restoring...")
        flame.restore(str(yaml_checkpoint), name='solution')
        source = 'restored'
    else:
        print(f"--> [phi={phi:.2f}] Solving flame... (takes ~30-60 sec)")
        gas.TP = T_UNBURNED, PRESSURE
        gas.set_equivalence_ratio(phi, 'CH4:1', 'O2:1, N2:3.76')
        flame = ct.FreeFlame(gas, width=WIDTH)

        flame.transport_model = 'mixture-averaged'
        flame.set_refine_criteria(ratio=REFINE_RATIO, slope=REFINE_SLOPE, curve=REFINE_CURVE)

        # Solve nonlinear boundary-value problem
        flame.solve(loglevel=1, auto=True)
        source = 'solved'

        # Save native checkpoint
        flame.save(str(yaml_checkpoint), name='solution', overwrite=True)

        # Build and export full spatial profile CSV
        profile_data = {
            'distance_mm': flame.grid * 1000.0,
            'temperature_K': flame.T,
            'velocity_m_s': flame.velocity,
            'density_kg_m3': flame.density,
            'heat_release_rate_W_m3': flame.heat_release_rate,
            'viscosity_Pa_s': flame.viscosity,
            'thermal_conductivity_W_mK': flame.thermal_conductivity,
            'cp_mass_J_kgK': flame.cp_mass,
        }
        for sp in MAJOR_SPECIES + RADICAL_SPECIES:
            if sp in gas.species_names:
                k = gas.species_index(sp)
                profile_data[f'X_{sp}'] = flame.X[k, :]
                profile_data[f'wdot_{sp}'] = flame.net_production_rates[k, :]

        pd.DataFrame(profile_data).to_csv(csv_profile, index=False)
        print(f"    Saved checkpoint: {yaml_checkpoint.name} & {csv_profile.name}")

    # Calculate thermal thickness (delta_T / max(|dT/dx|))
    dT_dx = np.gradient(flame.T, flame.grid)
    thermal_thickness_mm = float(np.max(flame.T) - flame.T[0]) / float(np.max(np.abs(dT_dx))) * 1000.0

    summary = {
        'phi': float(phi),
        'flame_speed_cm_s': float(flame.velocity[0] * 100.0),
        'max_temperature_K': float(np.max(flame.T)),
        'max_heat_release_W_m3': float(np.max(flame.heat_release_rate)),
        'thermal_thickness_mm': thermal_thickness_mm,
        'grid_points': int(flame.grid.size),
        'status': source,
    }
    return flame, summary


# ==============================================================================
# 3. RUN SIMULATION SWEEP
# ==============================================================================
print("==================================================")
print(f"Mechanism: {MECHANISM} | P = {PRESSURE/1e5:.3f} bar | T0 = {T_UNBURNED} K")
print(f"Phi values: {PHI_VALUES}")
print("==================================================")

flames_by_phi = {}
summary_records = []

for phi in sorted(PHI_VALUES):
    flame_obj, summary = solve_or_restore_flame(phi)
    flames_by_phi[phi] = flame_obj
    summary_records.append(summary)

# Save sweep summary
summary_df = pd.DataFrame(summary_records)
summary_df.to_csv(OUT_DIR / "flame_sweep_summary.csv", index=False)
print("\n=== SUMMARY TABLE ===")
print(summary_df.to_string(index=False))

# Identify reference case (closest to phi = 1.0)
ref_phi = min(flames_by_phi.keys(), key=lambda v: abs(v - 1.0))
ref_flame = flames_by_phi[ref_phi]
ref_gas = ref_flame.gas
x_mm = ref_flame.grid * 1000.0

# ------------------------------------------------------------------------------
# AUTOMATIC REACTION ZONE DETECTION
# Defined where heat release rate >= 10% of maximum heat release
# ------------------------------------------------------------------------------
qdot_arr = ref_flame.heat_release_rate
qdot_max = float(np.max(qdot_arr))
rxn_idx = np.where(qdot_arr >= 0.10 * qdot_max)[0]
if len(rxn_idx) > 0:
    x_rxn_start = x_mm[rxn_idx[0]]
    x_rxn_end = x_mm[rxn_idx[-1]]
    rxn_width_um = (x_rxn_end - x_rxn_start) * 1000.0
else:
    x_rxn_start, x_rxn_end, rxn_width_um = 0.0, 0.0, 0.0

print(f"\n[INFO] Reference Flame (phi={ref_phi:.2f}) Spatial Analysis:")
print(f"       Grid Points: {ref_flame.grid.size}")
print(f"       Reaction Zone: {x_rxn_start:.2f} mm to {x_rxn_end:.2f} mm (Width = {rxn_width_um:.1f} um)")
print(f"       Laminar Flame Speed: {ref_flame.velocity[0]*100:.2f} cm/s")
print(f"       Max Flame Temperature: {np.max(ref_flame.T):.1f} K")


# ==============================================================================
# 4. GENERATE ENHANCED 10 GRAPHS
# ==============================================================================
print("\nGenerating enhanced graphs with reaction zone markings...")

# --- Graph 1: Flame Speed & Max Temperature vs Phi ---
if len(PHI_VALUES) > 1:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Flame speed
    axes[0].plot(summary_df['phi'], summary_df['flame_speed_cm_s'], 'o-', color='#176B87', lw=2.2, ms=6)
    peak_idx = summary_df['flame_speed_cm_s'].idxmax()
    peak_phi = summary_df.loc[peak_idx, 'phi']
    peak_speed = summary_df.loc[peak_idx, 'flame_speed_cm_s']
    axes[0].annotate(f'Peak: {peak_speed:.1f} cm/s\n@ phi={peak_phi:.2f}', 
                     xy=(peak_phi, peak_speed), xytext=(peak_phi-0.12, peak_speed-4),
                     arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))
    axes[0].axvline(1.0, color='gray', linestyle=':', label='Stoichiometric (phi=1.0)')
    axes[0].set(xlabel='Equivalence ratio, $\\phi$ [-]', ylabel='Laminar flame speed, $S_L$ [cm/s]', 
                title='Laminar Flame Speed ($S_L$) vs $\\phi$')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Temperature
    axes[1].plot(summary_df['phi'], summary_df['max_temperature_K'], 's-', color='#D95319', lw=2.2, ms=6)
    axes[1].axvline(1.0, color='gray', linestyle=':', label='Stoichiometric (phi=1.0)')
    axes[1].set(xlabel='Equivalence ratio, $\\phi$ [-]', ylabel='Maximum temperature [K]', 
                title='Maximum Flame Temperature vs $\\phi$')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(GRAPH_DIR / '01_summary_vs_phi.png', dpi=200)
    plt.close()
    print("  [OK] Graph 1: Flame speed & max temperature vs phi")
else:
    print("  [-] Graph 1 skipped (requires >= 2 phi values to plot a curve)")

# --- Helper for Shading Reaction Zone on Plots ---
def shade_reaction_zone(ax, label='Reaction Zone'):
    ax.axvspan(x_rxn_start, x_rxn_end, color='orange', alpha=0.18, label=label)

# --- Graph 2: Physical Overview with Reaction Zone Highlighting ---
fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), sharex=True)
for ax in axes.flat:
    shade_reaction_zone(ax, label='Reaction Zone (q_dot > 10%)' if ax == axes[0, 0] else "")
    ax.grid(True, alpha=0.25)

# Plot actual data points (points showing adaptive mesh resolution)
axes[0, 0].plot(x_mm, ref_flame.T, color='#D95319', lw=2)
axes[0, 0].set(ylabel='Temperature [K]', title=f'Temperature (Max: {np.max(ref_flame.T):.0f} K)')
axes[0, 0].legend(loc='lower right', framealpha=0.9)

axes[0, 1].plot(x_mm, ref_flame.velocity, color='#176B87', lw=2)
axes[0, 1].set(ylabel='Velocity [m/s]', title=f'Axial Velocity ($S_L$: {ref_flame.velocity[0]*100:.1f} cm/s)')

axes[1, 0].plot(x_mm, ref_flame.density, color='#2E8B57', lw=2)
axes[1, 0].set(xlabel='Distance [mm]', ylabel='Density [kg/m³]', title='Density Drop across Flame')

axes[1, 1].plot(x_mm, ref_flame.heat_release_rate / 1e9, color='#8E44AD', lw=2)
axes[1, 1].set(xlabel='Distance [mm]', ylabel='Heat Release [$GW/m^3$]', title='Volumetric Heat Release')

fig.suptitle(f'1D Flame Overview with Marked Reaction Zone (phi={ref_phi:.2f})', fontsize=13, weight='bold')
fig.tight_layout()
fig.savefig(GRAPH_DIR / '02_physical_overview.png', dpi=200)
plt.close()
print("  [OK] Graph 2: Physical overview (Reaction zone highlighted)")

# --- Graph 3: Major Species Profiles ---
fig, ax = plt.subplots(figsize=(10, 5.5))
shade_reaction_zone(ax, label='Reaction Zone')
for sp in MAJOR_SPECIES:
    if sp in ref_gas.species_names:
        k = ref_gas.species_index(sp)
        ax.plot(x_mm, ref_flame.X[k, :], label=sp, lw=2)
ax.set(xlabel='Distance [mm]', ylabel='Mole fraction [-]', 
       title=f'Major Species Profiles & Consumption in Reaction Zone (phi={ref_phi:.2f})')
ax.legend(ncol=3, loc='center right', framealpha=0.9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(GRAPH_DIR / '03_major_species.png', dpi=200)
plt.close()
print("  [OK] Graph 3: Major species")

# --- Graph 4: Radicals on Log Scale (Focused & Cleaned) ---
fig, ax = plt.subplots(figsize=(10, 5.5))
shade_reaction_zone(ax, label='Reaction Zone')
for sp in RADICAL_SPECIES:
    if sp in ref_gas.species_names:
        k = ref_gas.species_index(sp)
        # Clean physical threshold at 1e-8 to eliminate unburned floor noise
        ax.semilogy(x_mm, ref_flame.X[k, :], label=sp, lw=2.2, marker='.', ms=5)

ax.set(xlabel='Distance [mm]', ylabel='Mole fraction [-] (log scale)', 
       title=f'Radical Pool Concentrations Across Reaction Zone (phi={ref_phi:.2f})')
ax.set_ylim(1e-8, 3e-2) # Cut off non-physical floor noise below 10^-8
ax.set_xlim(max(0, x_rxn_start - 6), min(np.max(x_mm), x_rxn_end + 14)) # Zoom to active flame front
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, which='both', alpha=0.3)
fig.tight_layout()
fig.savefig(GRAPH_DIR / '04_radicals_log_scale.png', dpi=200)
plt.close()
print("  [OK] Graph 4: Radicals (Cleaned & zoomed into reaction zone)")

# --- Graph 5: Species Production / Consumption Rates ---
fig, ax = plt.subplots(figsize=(10, 5.5))
shade_reaction_zone(ax, label='Reaction Zone')
rate_species = ['CH4', 'O2', 'CO', 'CO2', 'OH']
for sp in rate_species:
    if sp in ref_gas.species_names:
        k = ref_gas.species_index(sp)
        ax.plot(x_mm, ref_flame.net_production_rates[k, :], label=sp, lw=2)
ax.axhline(0.0, color='black', lw=0.8, linestyle='--')
ax.set(xlabel='Distance [mm]', ylabel='Net production rate [kmol/m³/s]', 
       title=f'Species Creation (+) and Consumption (-) in Reaction Zone (phi={ref_phi:.2f})')
ax.legend(ncol=3, framealpha=0.9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(GRAPH_DIR / '05_species_production_rates.png', dpi=200)
plt.close()
print("  [OK] Graph 5: Species production rates")

# --- Graph 6: Top 10 Most Active Reactions ---
net_rop = ref_flame.net_rates_of_progress
integrated_activity = np.trapezoid(np.abs(net_rop), x=ref_flame.grid, axis=1)
top_indices = np.argsort(integrated_activity)[-10:]
equations = np.array(ref_gas.reaction_equations())[top_indices]
values = integrated_activity[top_indices]

fig, ax = plt.subplots(figsize=(11, 6))
ax.barh(equations, values, color='#6C5CE7')
ax.set(xlabel='Integrated absolute rate [kmol/m²/s]', title=f'Top 10 Most Active Reactions (phi={ref_phi:.2f})')
ax.grid(True, axis='x', alpha=0.3)
fig.tight_layout()
fig.savefig(GRAPH_DIR / '06_top_reactions.png', dpi=200)
plt.close()
print("  [OK] Graph 6: Top active reactions")

# --- Graph 7: Transport Properties ---
fig, axes = plt.subplots(3, 1, figsize=(9, 8.5), sharex=True)
for ax in axes:
    shade_reaction_zone(ax)
    ax.grid(True, alpha=0.3)

axes[0].plot(x_mm, ref_flame.viscosity * 1e5, color='#34495E', lw=2)
axes[0].set(ylabel='Viscosity [$10^{-5}$ Pa·s]', title='Dynamic Viscosity (Increases with T)')

axes[1].plot(x_mm, ref_flame.thermal_conductivity, color='#E67E22', lw=2)
axes[1].set(ylabel='$\\lambda$ [W/m·K]', title='Thermal Conductivity (Controls Preheat Zone)')

axes[2].plot(x_mm, ref_flame.cp_mass, color='#16A085', lw=2)
axes[2].set(xlabel='Distance [mm]', ylabel='$c_p$ [J/kg·K]', title='Mass-specific Heat Capacity')

fig.suptitle(f'Transport & Thermodynamic Properties (phi={ref_phi:.2f})', fontsize=13, weight='bold')
fig.tight_layout()
fig.savefig(GRAPH_DIR / '07_transport_properties.png', dpi=200)
plt.close()
print("  [OK] Graph 7: Transport properties")

# --- Graph 8: Multi-phi Comparison ---
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for phi, fl in sorted(flames_by_phi.items()):
    x_local = fl.grid * 1000.0
    axes[0].plot(x_local, fl.T, label=f'$\\phi$={phi:.2f}', lw=1.8)
    qdot = fl.heat_release_rate
    scale = max(float(np.max(np.abs(qdot))), 1e-10)
    axes[1].plot(x_local, qdot / scale, label=f'$\\phi$={phi:.2f}', lw=1.8)

axes[0].set(xlabel='Distance [mm]', ylabel='Temperature [K]', title='Temperature Profiles Across $\\phi$')
axes[0].legend(ncol=2)
axes[0].grid(True, alpha=0.3)

axes[1].set(xlabel='Distance [mm]', ylabel='Normalized Heat Release [-]', title='Flame Position & Reaction Zone Shape Across $\\phi$')
axes[1].legend(ncol=2)
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(GRAPH_DIR / '08_multi_phi_profiles.png', dpi=200)
plt.close()
print("  [OK] Graph 8: Multi-phi comparison")

# --- Graph 9: Reaction-Zone Diagnostics ---
dT_dx = np.gradient(ref_flame.T, ref_flame.grid)
grad_norm = np.abs(dT_dx) / max(float(np.max(np.abs(dT_dx))), 1e-10)
q_norm = ref_flame.heat_release_rate / max(float(np.max(np.abs(ref_flame.heat_release_rate))), 1e-10)

fig, ax = plt.subplots(figsize=(10, 5.5))
shade_reaction_zone(ax, label=f'Reaction Zone ({rxn_width_um:.0f} µm wide)')
ax.plot(x_mm, grad_norm, label='|dT/dx| / max (|dT/dx|) [Thermal Preheat Zone]', lw=2.2, color='#D95319')
ax.plot(x_mm, q_norm, label='Heat Release / max (Heat Release) [Chemical Reaction Zone]', lw=2.2, color='#176B87')

ax.set(xlabel='Distance [mm]', ylabel='Normalized value [-]', 
       title=f'Reaction-Zone Diagnostics: Preheat Conduction vs Chemical Heat Release (phi={ref_phi:.2f})')
ax.legend(framealpha=0.9)
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(GRAPH_DIR / '09_reaction_zone.png', dpi=200)
plt.close()
print("  [OK] Graph 9: Reaction-zone diagnostics (Preheat vs Chemical layer)")

# --- Graph 10: Interactive HTML Temperature Curve with Shaded Zone ---
interactive_df = pd.DataFrame({
    'Distance_mm': x_mm,
    'Temperature_K': ref_flame.T,
})
fig_interactive = px.line(
    interactive_df,
    x='Distance_mm',
    y='Temperature_K',
    title=f'Interactive Flame Temperature Profile (phi={ref_phi:.2f}, Reaction Zone: {x_rxn_start:.2f}-{x_rxn_end:.2f} mm)',
    labels={'Distance_mm': 'Distance [mm]', 'Temperature_K': 'Temperature [K]'}
)
fig_interactive.add_vrect(x0=x_rxn_start, x1=x_rxn_end, fillcolor="orange", opacity=0.2, line_width=0, annotation_text="Reaction Zone")
fig_interactive.write_html(str(GRAPH_DIR / '10_interactive_temperature.html'))
print("  [OK] Graph 10: Interactive temperature profile (HTML)")

print(f"\n==================================================")
print(f"All enhanced outputs generated successfully!")
print(f"Results Directory: {OUT_DIR.resolve()}")
print(f"Graphs Directory:  {GRAPH_DIR.resolve()}")
print(f"==================================================")
