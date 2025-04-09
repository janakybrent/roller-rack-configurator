
import streamlit as st
from utils import generate_part_number, calculate_output, generate_pdf

st.set_page_config(page_title="WHEATON Roller Rack Configurator")

st.title("🧪 WHEATON® Roller Rack Configurator")

with st.form("config_form"):
    st.header("Step-by-step Configuration")

    ctrl_system = st.selectbox("Control System Type", ["R", "S"])
    ctrl_location = st.selectbox("Control System Location", ["T", "B"])
    deck_spacing = st.selectbox("Deck Spacing", ["P", "M"])
    deck_type = st.selectbox("Deck Type", ["F", "R"])
    capacity = st.selectbox("Capacity", ["5", "8"])
    deck_number = st.selectbox("Number of Decks", [f"{i:02}" for i in range(1, 12 if capacity == "5" else 10)])
    options = st.selectbox("Options", ["0", "1"])
    plug_style = st.selectbox("Plug Style", ["-A", "-B", "-C", "-D", "-F", "-G", "-J"])

    bottle_size = st.selectbox("Bottle Size", ["110 x 240 mm", "110 x 285 mm", "110 x 355 mm", "110 x 480 mm", "110 x 535 mm"])
    submit = st.form_submit_button("Generate Configuration")

if submit:
    part_number = generate_part_number(ctrl_system, ctrl_location, deck_spacing, deck_type, capacity, deck_number, options, plug_style)
    bottles, surface_area, output_cells = calculate_output(capacity, deck_number, bottle_size)

    st.subheader("🔧 Generated Part Number")
    st.code(part_number, language="text")

    st.subheader("📊 Output Estimate")
    st.write(f"Bottles per Rack: {bottles}")
    st.write(f"Total Surface Area: {surface_area:,} cm²")
    st.write(f"Estimated Cell Output: {output_cells:.2e} cells")

    if st.button("Download Summary PDF"):
        pdf_bytes = generate_pdf(part_number, ctrl_system, ctrl_location, deck_spacing, deck_type, capacity,
                                 deck_number, options, plug_style, bottle_size, bottles, surface_area, output_cells)
        st.download_button("📄 Download PDF", data=pdf_bytes, file_name=f"{part_number}_summary.pdf")
