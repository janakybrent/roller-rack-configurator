
import streamlit as st
from utils import generate_part_number, calculate_output, generate_pdf

st.set_page_config(page_title="WHEATON Roller Apparatus Configurator", layout="wide")

st.markdown("""
    <style>
    .step-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .step-subtext {
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .part-summary {
        border: 1px solid #CCC;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #F8F9FA;
    }
    .config-box {
        border: 1px solid #EEE;
        padding: 1.2rem;
        border-radius: 0.5rem;
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("WHEATON® Roller Apparatus Configurator")
st.write("Configure your roller apparatus by following the steps below")

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("config_form"):
        st.markdown('<div class="step-header">Step 1: Select Control System Type</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-subtext">Choose between the advanced R2P™ 2.0 with touchscreen or the standard LED display.</div>', unsafe_allow_html=True)
        ctrl_system = st.radio("", ["R (R2P™ 2.0)", "S (STANDARD)"])

        ctrl_location = st.radio("Step 2: Select Control System Location", ["T (Top Mounted)", "B (Bottom Mounted)"])
        deck_spacing = st.radio("Step 3: Select Deck Spacing", ["P (Production - 6\")", "M (Modular - 7.125\")"])
        deck_type = st.radio("Step 4: Select Deck Type", ["F (Fixed)", "R (Removable)"])
        capacity = st.radio("Step 5: Select Capacity", ["5", "8"])
        deck_options = [f"{i:02}" for i in range(1, 12 if capacity == "5" else 10)]
        deck_number = st.selectbox("Step 6: Select Number of Decks", deck_options)
        options = st.radio("Step 7: Select Options", ["0 (No options)", "1 (Includes alarm + battery backup)"])
        plug_style = st.selectbox("Step 8: Select Plug Style", ["-A (120V)", "-B (100V)", "-C (230V EU)", "-D (230V UK)", "-F (230V AU)", "-G (230V IT)", "-J (230V IN)"])
        bottle_size = st.selectbox("Select Roller Bottle Size", ["110 x 240 mm", "110 x 285 mm", "110 x 355 mm", "110 x 480 mm", "110 x 535 mm"])
        submitted = st.form_submit_button("Generate Configuration")

if submitted:
    r = ctrl_system.split()[0]
    t = ctrl_location.split()[0]
    s = deck_spacing.split()[0]
    d = deck_type.split()[0]
    c = capacity
    n = deck_number
    o = options.split()[0]
    p = plug_style.split()[0]

    part_number = generate_part_number(r, t, s, d, c, n, o, p)
    bottles, surface_area, output_cells = calculate_output(c, n, bottle_size)

    with col2:
        st.markdown("### Configuration Summary")
        st.markdown('<div class="part-summary">', unsafe_allow_html=True)
        st.write(f"**Part Number:** `{part_number}`")
        st.write(f"**Bottle Size:** {bottle_size}")
        st.write(f"**Bottle Count per Rack:** {bottles}")
        st.write(f"**Surface Area:** {surface_area:,} cm²")
        st.write(f"**Estimated Cell Output:** {output_cells:.2e} cells")
        st.markdown('</div>', unsafe_allow_html=True)

        pdf_bytes = generate_pdf(part_number, r, t, s, d, c, n, o, p, bottle_size, bottles, surface_area, output_cells)
        st.download_button("📄 Download Summary PDF", data=pdf_bytes, file_name=f"{part_number}_summary.pdf")
