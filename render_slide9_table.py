"""
Render high-resolution LaTeX table image for Slide 9 (Validation).
Fixed custom column widths so text never clips or overflows outside cell borders.
"""
from pathlib import Path
import matplotlib.pyplot as plt

OUT_PATH = Path(__file__).resolve().parent / "validation_table_slide9.png"

fig = plt.figure(figsize=(11.5, 3.8), dpi=300)
ax = fig.add_subplot(111)
ax.axis('off')

# Table data with true LaTeX math formatting
col_labels = [
    r"$\mathbf{Validation\; Parameter}$",
    r"$\mathbf{Literature\; Benchmark}$",
    r"$\mathbf{Our\; Simulation\; Output}$",
    r"$\mathbf{Agreement\; /\; Error}$"
]

table_data = [
    [
        r"$\mathrm{Laminar\; Flame\; Speed}\;(S_L\;\mathrm{at}\;\phi=1.00)$",
        r"$38.0 - 39.0\;\mathrm{cm/s}$",
        r"$\mathbf{38.09\;\mathrm{cm/s}}$",
        r"$\Delta < 0.2\%\;(\mathrm{Exact})$"
    ],
    [
        r"$\mathrm{Peak\; Flame\; Speed}\;(\phi=1.05)$",
        r"$\sim 38.0 - 39.5\;\mathrm{cm/s}$",
        r"$\mathbf{38.76\;\mathrm{cm/s}}$",
        r"$\mathrm{Exact\; Peak\; Match}$"
    ],
    [
        r"$\mathrm{Adiabatic\; Flame\; Temperature}\;(T_{\mathrm{ad}})$",
        r"$2225 - 2235\;\mathrm{K}$",
        r"$\mathbf{2230.7\;\mathrm{K}}$",
        r"$\mathrm{Thermodynamic\; Limit}$"
    ],
    [
        r"$\mathrm{Mass\; Flux\; Conservation}\;(\dot{m} = \rho u)$",
        r"$\rho_u u_u = \mathrm{constant}$",
        r"$0.430 \rightarrow 0.430\;\mathrm{kg/(m^2\cdot s)}$",
        r"$\mathbf{0.00\%\; Error}$"
    ]
]

# Column widths: 1st column given wider share (35%) so text never overflows
col_widths = [0.35, 0.21, 0.23, 0.21]

table = ax.table(
    cellText=table_data,
    colLabels=col_labels,
    colWidths=col_widths,
    loc='center',
    cellLoc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(11.5)
table.scale(1.0, 2.3)

# Styling
for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor('#D0D7DE')
    cell.set_linewidth(1.0)
    if row == 0:
        cell.set_facecolor('#F0F4F8')
        cell.set_text_props(color='#176B87', weight='bold')
    else:
        if row % 2 == 0:
            cell.set_facecolor('#FAFAFA')
        else:
            cell.set_facecolor('#FFFFFF')
        
        # Color agreement column
        if col == 3:
            cell.set_text_props(color='#D95319', weight='bold')
        elif col == 2:
            cell.set_text_props(color='#176B87', weight='bold')
        elif col == 0:
            cell.set_text_props(color='#2B2B2B', ha='center')
        else:
            cell.set_text_props(color='#2B2B2B')

plt.subplots_adjust(left=0.01, right=0.99, top=0.96, bottom=0.04)
fig.savefig(str(OUT_PATH), bbox_inches='tight', transparent=True)
plt.close()
print("Saved fixed slide 9 table image:", OUT_PATH)
