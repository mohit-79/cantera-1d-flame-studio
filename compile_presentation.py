"""
Compile LaTeX-style presentation directly to 16:9 PDF using ReportLab.
Redesigned Page 1, Larger Typography Across All Pages.
"""

from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent
GRAPH_DIR = BASE_DIR / "flame_results" / "graphs"
PDF_FILE = BASE_DIR / "Combustion_Project_Presentation.pdf"

# 16:9 Widescreen dimension in points (10 inch x 5.625 inch)
PAGE_WIDTH = 10 * 72
PAGE_HEIGHT = 5.625 * 72

# Minimal Academic Palette (LaTeX Whale/Madrid style)
NAVY = colors.HexColor("#176B87")
CHARCOAL = colors.HexColor("#2B2B2B")
GRAY = colors.HexColor("#555555")
ORANGE = colors.HexColor("#D95319")
LINE_COLOR = colors.HexColor("#D0D7DE")
BG_LIGHT = colors.HexColor("#F6F8FA")
ACCENT_BLUE = colors.HexColor("#EBF3F5")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        if self._pageNumber > 1:
            # Header line
            self.setStrokeColor(LINE_COLOR)
            self.setLineWidth(1.0)
            self.line(36, PAGE_HEIGHT - 56, PAGE_WIDTH - 36, PAGE_HEIGHT - 56)

            # Footer line
            self.line(36, 32, PAGE_WIDTH - 36, 32)
            
            # Footer text (increased font size)
            self.setFont("Helvetica-Bold", 8.5)
            self.setFillColor(NAVY)
            self.drawString(36, 18, "1D Premixed Methane-Air Combustion Simulation (Cantera & GRI-Mech 3.0)")
            self.setFont("Helvetica-Bold", 9)
            self.setFillColor(GRAY)
            page_text = f"{self._pageNumber} / {total_pages}"
            self.drawRightString(PAGE_WIDTH - 36, 18, page_text)

def build_pdf():
    doc = SimpleDocTemplate(
        str(PDF_FILE),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=36,
        rightMargin=36,
        topMargin=18,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    # Enhanced & Larger Typography
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=25,
        leading=29,
        textColor=NAVY,
        alignment=1 # Center
    )
    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13.5,
        leading=17,
        textColor=CHARCOAL,
        alignment=1
    )
    slide_cat = ParagraphStyle(
        'SlideCat',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11,
        textColor=ORANGE,
    )
    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY,
    )
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=NAVY,
    )
    body = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14.5,
        textColor=CHARCOAL,
    )
    bullet = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14.5,
        textColor=CHARCOAL,
        leftIndent=12,
        firstLineIndent=-12
    )
    formula = ParagraphStyle(
        'Formula',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=13,
        textColor=ORANGE,
        leftIndent=14
    )

    story = []

    def make_header(title, category="NUMERICAL COMBUSTION SIMULATION"):
        return [
            Paragraph(category.upper(), slide_cat),
            Paragraph(title, slide_title),
            Spacer(1, 14)
        ]

    # =========================================================================
    # Slide 1: Redesigned Minimal Academic Title Slide
    # =========================================================================
    story.append(Spacer(1, 12))
    
    # Department Header at top
    dept_header = ParagraphStyle('DeptHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=ORANGE, alignment=1)
    story.append(Paragraph("DEPARTMENT OF MECHANICAL ENGINEERING", dept_header))
    story.append(Spacer(1, 14))

    # Main Project Title
    story.append(Paragraph("1D Premixed Methane-Air Combustion Simulation", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Numerical Study using Detailed Chemical Kinetics (Cantera &amp; GRI-Mech 3.0)", subtitle_style))
    story.append(Spacer(1, 22))

    # Redesigned Clean Team Table with Guidance
    students_data = [
        [Paragraph("<b>Student Name</b>", body_bold), Paragraph("<b>Roll Number</b>", body_bold)],
        [Paragraph("Ali Asgar Saify", body), Paragraph("24134003", body)],
        [Paragraph("Mohit Harjani", body), Paragraph("24135079", body)],
        [Paragraph("Rishabh Raj Tripathi", body), Paragraph("24135105", body)],
        [Paragraph("Piyush Devra", body), Paragraph("24134024", body)],
    ]
    t_students = Table(students_data, colWidths=[210, 130])
    t_students.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('LINEBELOW', (0,0), (-1,0), 1.5, NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
    ]))

    guide_box = [
        Spacer(1, 8),
        Paragraph("<b>Under the Guidance of:</b>", body_bold),
        Spacer(1, 4),
        Paragraph("<b>Prof. Anubhav Sinha</b>", ParagraphStyle('Prof', parent=body, fontSize=13, leading=16, textColor=CHARCOAL)),
        Spacer(1, 4),
        Paragraph("Department of Mechanical Engineering", ParagraphStyle('DeptSub', parent=body, fontSize=10.5, leading=13, textColor=GRAY)),
        Spacer(1, 8),
        Paragraph("<b>Tools:</b> Python 3.10 &bull; Cantera 3.2 &bull; GRI-Mech 3.0", ParagraphStyle('Tools', parent=body, fontSize=9.5, leading=12, textColor=NAVY)),
    ]

    t_front = Table([[t_students, guide_box]], colWidths=[360, 280])
    t_front.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (1,0), (1,0), 25),
    ]))
    story.append(t_front)
    story.append(PageBreak())

    # =========================================================================
    # Slide 2: Objectives & Governing Equations
    # =========================================================================
    story.extend(make_header("Problem Definition &amp; Governing Equations"))
    col1 = [
        Paragraph("<b>Physical Scope:</b>", body_bold),
        Spacer(1, 5),
        Paragraph("&bull; Planar, 1D freely-propagating laminar flame.", bullet),
        Paragraph("&bull; Inflow: T<sub>u</sub> = 300 K, P = 1 atm (101325 Pa).", bullet),
        Paragraph("&bull; Dry Air mixture: O<sub>2</sub> : N<sub>2</sub> = 1 : 3.76.", bullet),
        Paragraph("&bull; Domain width: L = 30 mm.", bullet),
        Paragraph("&bull; Dense sweep: &phi; = 0.65 to 1.35 (15 points).", bullet),
        Spacer(1, 10),
        Paragraph("<b>Primary Objectives:</b>", body_bold),
        Spacer(1, 5),
        Paragraph("&bull; Compute laminar flame speed S<sub>L</sub> as an eigenvalue.", bullet),
        Paragraph("&bull; Determine peak and adiabatic temperatures.", bullet),
        Paragraph("&bull; Resolve internal flame preheat vs reaction zones.", bullet),
    ]
    img_eq_path = BASE_DIR / "equations_slide2.png"
    col2 = [
        Image(str(img_eq_path), width=355, height=225) if img_eq_path.exists() else Paragraph("Equations", body)
    ]
    t2 = Table([[col1, col2]], colWidths=[290, 360])
    t2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t2)
    story.append(PageBreak())

    # =========================================================================
    # Slide 3: Chemical Kinetics & Numerical Strategy
    # =========================================================================
    story.extend(make_header("Chemical Mechanism &amp; Adaptive Numerical Grid"))
    col3_1 = [
        Paragraph("<b>Detailed Kinetic Mechanism (GRI-Mech 3.0):</b>", body_bold),
        Spacer(1, 6),
        Paragraph("&bull; <b>GRI:</b> <i>Gas Research Institute</i> (GRI-Mech 3.0 benchmark).", bullet),
        Paragraph("&bull; <b>53 chemical species</b>, <b>325 elementary reactions</b>.", bullet),
        Paragraph("&bull; Industry standard for natural gas and methane combustion modeling.", bullet),
        Paragraph("&bull; Includes comprehensive NO<sub>x</sub> intermediate pathways.", bullet),
        Paragraph("&bull; NASA polynomials for thermodynamic state (H, S, c<sub>p</sub>).", bullet),
        Paragraph("&bull; Mixture-averaged transport formulation (&lambda;, &mu;, D<sub>km</sub>).", bullet),
    ]
    col3_2 = [
        Paragraph("<b>Cantera Numerical Methodology:</b>", body_bold),
        Spacer(1, 6),
        Paragraph("&bull; <b>Boundary Value Problem (BVP):</b> Solved using a hybrid damped Newton-Raphson iteration.", bullet),
        Paragraph("&bull; <b>Eigenvalue Problem:</b> Inlet velocity u(0) = S<sub>L</sub> is solved to balance flame propagation.", bullet),
        Paragraph("&bull; <b>Adaptive Mesh Refinement:</b>", bullet),
        Paragraph("&nbsp;&nbsp;&nbsp;&bull; Initial uniform grid: 16 points.", bullet),
        Paragraph("&nbsp;&nbsp;&nbsp;&bull; Refinement criteria: slope=0.05, curve=0.08.", bullet),
        Paragraph("&nbsp;&nbsp;&nbsp;&bull; Final converged mesh: <b>196 to 240 points</b> concentrated strictly within the reaction zone.", bullet),
    ]
    t3 = Table([[col3_1, col3_2]], colWidths=[320, 330])
    t3.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t3)
    story.append(PageBreak())

    # =========================================================================
    # Slide 4: Results — Flame Speed & Max Temperature vs Phi
    # =========================================================================
    story.extend(make_header("Results: Flame Speed &amp; Temperature vs Mixture Strength"))
    img1_path = GRAPH_DIR / "01_summary_vs_phi.png"
    img1 = Image(str(img1_path), width=355, height=200) if img1_path.exists() else Paragraph("Image 1", body)

    data_table = [
        ['&phi;', 'Regime', 'S<sub>L</sub> [cm/s]', 'T_max [K]'],
        ['0.65', 'Lean Limit', '15.41', '1755.8'],
        ['0.80', 'Lean', '27.35', '2001.6'],
        ['0.90', 'Lean', '34.03', '2139.3'],
        ['1.00', 'Stoichiometric', '38.09', '2230.7'],
        ['1.05', 'Peak Speed &amp; T', '38.76', '2237.1'],
        ['1.10', 'Slightly Rich', '38.36', '2213.4'],
        ['1.20', 'Rich', '33.68', '2134.3'],
        ['1.35', 'Rich Limit', '18.28', '2014.3'],
    ]
    formatted_table = [[Paragraph(f"<b>{c}</b>" if i==0 else c, body) for c in row] for i, row in enumerate(data_table)]
    t_data = Table(formatted_table, colWidths=[42, 92, 82, 82])
    t_data.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('LINEBELOW', (0,0), (-1,0), 1.2, NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BACKGROUND', (0,4), (-1,4), ACCENT_BLUE),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#FDEEE8")),
    ]))

    notes_4 = [
        t_data,
        Spacer(1, 8),
        Paragraph("&bull; <b>Dense 15-point sweep (&Delta;&phi; = 0.05)</b> yields a continuous smooth curve.", bullet),
        Paragraph("&bull; <b>Global peak occurs at &phi; = 1.05</b> (S<sub>L</sub> = 38.76 cm/s, T_max = 2237.1 K).", bullet),
    ]
    t4 = Table([[img1, notes_4]], colWidths=[355, 300])
    t4.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t4)
    story.append(PageBreak())

    # =========================================================================
    # Slide 5: Results — Flame Physical Structure Overview
    # =========================================================================
    story.extend(make_header("Results: 1D Flame Physical Structure (&phi; = 1.00)"))
    img2_path = GRAPH_DIR / "02_physical_overview.png"
    img2 = Image(str(img2_path), width=360, height=220) if img2_path.exists() else Paragraph("Image 2", body)

    notes_5 = [
        Paragraph("<b>Three Characteristic Layers:</b>", body_bold),
        Spacer(1, 6),
        Paragraph("&bull; <b>Preheat Zone (x &lt; 21.06 mm):</b> Upstream conduction heats cold reactants from 300 K to ~1300 K without fuel consumption.", bullet),
        Spacer(1, 5),
        Paragraph("&bull; <b>Reaction Zone (21.06 to 21.41 mm):</b> Marked by orange shading. Thickness &delta;_rxn = <b>352 &mu;m</b> (only 0.35 mm). Volumetric heat release peaks at <b>4.50 GW/m&sup3;</b>.", bullet),
        Spacer(1, 5),
        Paragraph("&bull; <b>Burned Zone (x &gt; 21.41 mm):</b> Thermal expansion causes density drop (1.13 &rarr; 0.15 kg/m&sup3;) and velocity acceleration (0.38 &rarr; 2.87 m/s) to conserve mass flux.", bullet),
    ]
    t5 = Table([[img2, notes_5]], colWidths=[365, 285])
    t5.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t5)
    story.append(PageBreak())

    # =========================================================================
    # Slide 6: Results — Major Species & Radicals
    # =========================================================================
    story.extend(make_header("Results: Major Species &amp; Radical Pool Evolution"))
    img3_path = GRAPH_DIR / "03_major_species.png"
    img4_path = GRAPH_DIR / "04_radicals_log_scale.png"
    img3 = Image(str(img3_path), width=315, height=190) if img3_path.exists() else Paragraph("Image 3", body)
    img4 = Image(str(img4_path), width=315, height=190) if img4_path.exists() else Paragraph("Image 4", body)

    t6_imgs = Table([[img3, img4]], colWidths=[325, 325])
    t6_imgs.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t6_imgs)
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Physical Insight:</b> CH<sub>4</sub> and O<sub>2</sub> deplete sharply within the 350 &mu;m reaction layer. Intermediate CO peaks inside the zone before oxidizing to CO<sub>2</sub>. Radicals (OH, H, O, HO<sub>2</sub>) exist at low mole fractions (10<sup>-3</sup> to 10<sup>-6</sup>) and peak strictly within the heat release zone to sustain chain branching.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # Slide 7: Results — Elementary Reaction Kinetics
    # =========================================================================
    story.extend(make_header("Results: Elementary Chemical Kinetics Ranking"))
    img6_path = GRAPH_DIR / "06_top_reactions.png"
    img6 = Image(str(img6_path), width=360, height=215) if img6_path.exists() else Paragraph("Image 6", body)

    notes_7 = [
        Paragraph("<b>Dominant Elementary Reactions:</b>", body_bold),
        Spacer(1, 7),
        Paragraph("<b>1. H + O2 &hArr; O + OH</b>", body_bold),
        Paragraph("Primary chain-branching reaction. Converts 1 radical into 2. Governs overall laminar flame speed.", formula),
        Spacer(1, 7),
        Paragraph("<b>2. CO + OH &hArr; CO2 + H</b>", body_bold),
        Paragraph("Primary exothermic heat release reaction. Produces the bulk of thermal energy in hydrocarbon combustion.", formula),
        Spacer(1, 7),
        Paragraph("<b>3. OH + H2 &hArr; H2O + H</b>", body_bold),
        Paragraph("Rapid radical propagation producing stable water vapor.", formula),
    ]
    t7 = Table([[img6, notes_7]], colWidths=[365, 285])
    t7.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t7)
    story.append(PageBreak())

    # =========================================================================
    # Slide 8: Results — Multi-Phi Comparison
    # =========================================================================
    story.extend(make_header("Results: Flame Structure Across Equivalence Ratios"))
    img8_path = GRAPH_DIR / "08_multi_phi_profiles.png"
    img8 = Image(str(img8_path), width=375, height=200) if img8_path.exists() else Paragraph("Image 8", body)

    notes_8 = [
        Paragraph("<b>Cross-Phi Dynamics:</b>", body_bold),
        Spacer(1, 7),
        Paragraph("&bull; Near stoichiometric (&phi; = 1.0 - 1.1), thermal gradients are steepest, resulting in the thinnest reaction layers (&delta;_T &approx; 0.43 mm).", bullet),
        Spacer(1, 7),
        Paragraph("&bull; In lean (&phi; = 0.7) and rich (&phi; = 1.3) regimes, reaction layers broaden significantly (&delta;_T &approx; 0.62 - 0.66 mm) due to lower reaction rates.", bullet),
        Spacer(1, 7),
        Paragraph("&bull; <b>Fundamental Law Demonstrated:</b> Thinner Reaction Layer &hArr; Higher Temperature Gradient &hArr; Faster Flame Speed.", bullet),
    ]
    t8 = Table([[img8, notes_8]], colWidths=[385, 265])
    t8.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t8)
    story.append(PageBreak())

    # =========================================================================
    # Slide 9: Numerical Verification & Literature Validation
    # =========================================================================
    story.extend(make_header("Numerical Verification &amp; Literature Validation"))
    img9_path = BASE_DIR / "validation_table_slide9.png"
    if img9_path.exists():
        story.append(Image(str(img9_path), width=645, height=235))
    story.append(PageBreak())

    # =========================================================================
    # Slide 10: Conclusions
    # =========================================================================
    story.extend(make_header("Summary &amp; Conclusions"))
    concl_items = [
        Paragraph("1. <b>Successful 1D Flame Modeling:</b> Freely-propagating laminar methane-air flames were successfully solved across &phi; = 0.65 &ndash; 1.35 using detailed GRI-Mech 3.0 chemistry.", body),
        Spacer(1, 10),
        Paragraph("2. <b>Peak Phenomena Identified:</b> Global peak flame speed occurs at &phi; = 1.05 (38.76 cm/s) and maximum temperature reaches 2237.1 K, driven by radical pool enrichment (H, OH).", body),
        Spacer(1, 10),
        Paragraph("3. <b>Spatial Layering Quantified:</b> The chemical reaction zone was proven to be sub-millimeter thin (&delta;_rxn &approx; 352 &mu;m), preceded by a conductive preheat zone.", body),
        Spacer(1, 10),
        Paragraph("4. <b>High Numerical Integrity:</b> Adaptive mesh refinement (16 &rarr; 240 points) ensured zero artificial diffusion and exact agreement (&lt;0.2%) with standard combustion literature.", body),
    ]
    for it in concl_items:
        story.append(it)
    story.append(PageBreak())

    # =========================================================================
    # Slide 11: Thank You
    # =========================================================================
    story.append(Spacer(1, 95))
    story.append(Paragraph("Thank You", title_style))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Department of Mechanical Engineering", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("1D Premixed Methane-Air Combustion Simulation (Cantera &amp; GRI-Mech 3.0)", ParagraphStyle('EndSub', parent=body, fontSize=11, leading=14, textColor=GRAY, alignment=1)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Compiled Presentation PDF to: {PDF_FILE}")

if __name__ == "__main__":
    build_pdf()
