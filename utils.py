
def generate_part_number(r, t, s, d, c, n, o, p):
    return f"W{r}{t}{s}{d}{c}{n}{o}{p}"

def calculate_output(capacity, deck_count, bottle_size):
    deck_count = int(deck_count)
    placements = int(capacity) * deck_count
    surface_area_lookup = {
        "110 x 240 mm": 550,
        "110 x 285 mm": 700,
        "110 x 355 mm": 940,
        "110 x 480 mm": 1320,
        "110 x 535 mm": 1555
    }
    bottles_per_pos = 2 if bottle_size == "110 x 240 mm" else 1
    bottles = placements * bottles_per_pos
    surface_area = surface_area_lookup[bottle_size] * bottles
    output_cells = surface_area * 1.5e5
    return bottles, surface_area, output_cells

from fpdf import FPDF
def generate_pdf(part_number, *args):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Roller Rack Configuration Summary", ln=True, align='C')
    labels = ["Control System", "Location", "Spacing", "Deck Type", "Capacity", "Decks", "Options", "Plug", "Bottle Size", "Bottle Count", "Surface Area", "Cell Output"]
    for label, value in zip(labels, args):
        pdf.cell(200, 10, txt=f"{label}: {value}", ln=True)
    return pdf.output(dest='S').encode('latin-1')
