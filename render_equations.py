"""
Generate crystal-clear LaTeX math equation image for Slide 2.
"""
from pathlib import Path
import matplotlib.pyplot as plt

OUT_PATH = Path(__file__).resolve().parent / "equations_slide2.png"

fig = plt.figure(figsize=(6.8, 4.4), dpi=300)
ax = fig.add_subplot(111)
ax.axis('off')

# Equations in genuine LaTeX formatting
eqs_text = [
    (r"$\mathbf{1.\; Continuity\; (Mass\; Conservation):}$", 0.90, '#176B87', 12, 'bold'),
    (r"$\frac{d(\rho u)}{dx} = 0 \quad \rightarrow \quad \dot{m} = \rho u = \mathrm{constant}$", 0.78, '#D95319', 13, 'normal'),
    
    (r"$\mathbf{2.\; Species\; Conservation\; (k = 1, \dots, 53):}$", 0.63, '#176B87', 12, 'bold'),
    (r"$\dot{m} \frac{d Y_k}{dx} = -\frac{d j_k}{dx} + \dot{\omega}_k W_k$", 0.51, '#D95319', 13, 'normal'),
    
    (r"$\mathbf{3.\; Energy\; Conservation:}$", 0.36, '#176B87', 12, 'bold'),
    (r"$\dot{m} c_p \frac{dT}{dx} = \frac{d}{dx}\left(\lambda \frac{dT}{dx}\right) - \sum_{k=1}^K j_k c_{p,k} \frac{dT}{dx} - \sum_{k=1}^K h_k \dot{\omega}_k W_k$", 0.24, '#D95319', 11.5, 'normal'),
    
    (r"$\mathbf{4.\; Thermal\; Equation\; of\; State\; (Ideal\; Gas\; Law):}$", 0.09, '#176B87', 12, 'bold'),
    (r"$P = \rho R_{\mathrm{spec}} T = \rho \left(\frac{R_u}{\bar{W}}\right) T$", -0.03, '#D95319', 13, 'normal'),
]

for text, y_pos, color, size, weight in eqs_text:
    ax.text(0.0, y_pos, text, color=color, fontsize=size, transform=ax.transAxes, va='center')

plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.08)
fig.savefig(str(OUT_PATH), bbox_inches='tight', transparent=True)
plt.close()
print("Saved equations image:", OUT_PATH)
