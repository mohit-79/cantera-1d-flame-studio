# 🔥 Cantera 1D Flame Studio

An interactive, open-source graphical user interface (GUI) and numerical simulation suite for **1D Premixed Laminar Flame Analysis** using [Cantera](https://cantera.org) and detailed chemical kinetics (**GRI-Mech 3.0**).

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Cantera](https://img.shields.io/badge/Cantera-3.2.0-orange)
![Streamlit](https://img.shields.io/badge/GUI-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 Features

- **Intuitive GUI Control Panel:**
  - Adjust inlet temperature ($T_u$), chamber pressure ($P$), domain width, and equivalence ratio ($\phi$) via sliders.
  - Choose between single flame inspection or full parametric sweeps ($\phi = 0.65 - 1.35$).
- **Automatic Chemical Reaction Zone Detection:**
  - Dynamically calculates the reaction zone where heat release rate $\dot{q} \ge 10\%$ of peak.
  - Highlights the sub-millimeter reaction layer ($\delta_{rxn} \approx 350\ \mu\text{m}$) across spatial plots.
- **Detailed Chemical Kinetics Diagnostics:**
  - Tracks 53 species and 325 elementary reactions.
  - Interactive radical pool log-plots ($OH, H, O, HO_2$).
  - Reaction pathway ranking ($H + O_2 \rightleftharpoons O + OH$, $CO + OH \rightleftharpoons CO_2 + H$).
- **Export & Portability:**
  - 1-Click CSV and Excel dataset export.
  - Built-in LaTeX Beamer style PDF presentation compiler (`compile_presentation.py`).
  - Automatic restart-safe checkpointing (`.yaml` and `.csv`).

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/cantera-1d-flame-studio.git
cd cantera-1d-flame-studio
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the GUI
```bash
streamlit run app.py
```
*Your browser will automatically open at `http://localhost:8501`.*

---

## 🖥️ Command-Line Simulation (Batch Mode)

To run the full 15-point parametric sweep and generate all 10 academic graphs without opening the browser:
```bash
python run_flame.py
```

To compile the 16:9 presentation PDF:
```bash
python compile_presentation.py
```

---

## 📂 Project Structure

```text
├── app.py                     # Streamlit Interactive Web GUI Dashboard
├── run_flame.py               # Core numerical solver & parametric sweep engine
├── compile_presentation.py    # Generates 16:9 widescreen presentation PDF
├── requirements.txt           # Python package dependencies
├── README.md                  # Project documentation
├── flame_results/             # Generated checkpoints, CSVs, and plots
│   ├── flame_sweep_summary.csv
│   └── graphs/                # 10 publication-quality graphs
```

---

## 👥 Authors & Contributors

- **Mohit Harjani** (Roll No: 24135079)
- **Ali Asgar Saify** (Roll No: 24134003)
- **Rishabh Raj Tripathi** (Roll No: 24135105)
- **Piyush Devra** (Roll No: 24134024)

**Under the Guidance of:**  
**Prof. Anubhav Sinha**  
*Department of Mechanical Engineering*

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
