import streamlit as st
import pandas as pd
import urllib.parse

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(page_title="Vayu Vega HD Pro", page_icon="🚚", layout="wide")

# ==========================================
# 2. INTERNAL DATA (మీ ఎక్సెల్ లో ఉన్న వాటికి equal)
# ==========================================
# మీరు తర్వాత మీ ఎక్సెల్ నుంచి df PINCODE_MASTER గా రీడ్ చేయొచ్చు,
# ఇక్కడ మాత్రం simple dict గా ఉంది
PINCODE_MASTER = {
    521301: "LOCAL", 521325: "LOCAL", 500001: "METRO",
    560001: "METRO", 110001: "NORTH", 600001: "SOUTH",
    # … మీరు మీ ఎక్సెల్ లో ఉన్న అన్ని పిన్‌కోడ్లు యాడ్ చెయ్
}

# మీ ఎక్సెల్ లో ఉన్న Weight slabs యూనిక్‌గా ఇక్కడ ఉండాలి (0.5, 1.0, 1.5, 2.0, 2.5, ..., 8.5, 9.0, ...)
RATES_DATA = [
    {"Weight": 0.5, "LOCAL-DTDC": 40, "LOCAL-ECOM": 35, "METRO-DTDC": 60, "METRO-ECOM": 55},
    {"Weight": 1.0, "LOCAL-DTDC": 70, "LOCAL-ECOM": 65, "METRO-DTDC": 100, "METRO-ECOM": 90},
    {"Weight": 1.5, "LOCAL-DTDC": 100, "LOCAL-ECOM": 90, "METRO-DTDC": 140, "METRO-ECOM": 130},
    {"Weight": 2.0, "LOCAL-DTDC": 130, "LOCAL-ECOM": 120, "METRO-DTDC": 180, "METRO-ECOM": 170},
    {"Weight": 2.5, "LOCAL-DTDC": 160, "LOCAL-ECOM": 150, "METRO-DTDC": 220, "METRO-ECOM": 210},
    {"Weight": 3.0, "LOCAL-DTDC": 190, "LOCAL-ECOM": 180, "METRO-DTDC": 260, "METRO-ECOM": 250},
    {"Weight": 3.5, "LOCAL-DTDC": 220, "LOCAL-ECOM": 210, "METRO-DTDC": 290, "METRO-ECOM": 280},
    {"Weight": 4.0, "LOCAL-DTDC": 250, "LOCAL-ECOM": 240, "METRO-DTDC": 320, "METRO-ECOM": 310},
    {"Weight": 4.5, "LOCAL-DTDC": 280, "LOCAL-ECOM": 270, "METRO-DTDC": 350, "METRO-ECOM": 340},
    {"Weight": 5.0, "LOCAL-DTDC": 310, "LOCAL-ECOM": 300, "METRO-DTDC": 380, "METRO-ECOM": 370},
    {"Weight": 5.5, "LOCAL-DTDC": 340, "LOCAL-ECOM": 330, "METRO-DTDC": 410, "METRO-ECOM": 400},
    {"Weight": 6.0, "LOCAL-DTDC": 370, "LOCAL-ECOM": 360, "METRO-DTDC": 440, "METRO-ECOM": 430},
    {"Weight": 6.5, "LOCAL-DTDC": 400, "LOCAL-ECOM": 390, "METRO-DTDC": 470, "METRO-ECOM": 460},
    {"Weight": 7.0, "LOCAL-DTDC": 430, "LOCAL-ECOM": 420, "METRO-DTDC": 500, "METRO-ECOM": 490},
    {"Weight": 7.5, "LOCAL-DTDC": 460, "LOCAL-ECOM": 450, "METRO-DTDC": 530, "METRO-ECOM": 520},
    {"Weight": 8.0, "LOCAL-DTDC": 490, "LOCAL-ECOM": 480, "METRO-DTDC": 560, "METRO-ECOM": 550},
    {"Weight": 8.5, "LOCAL-DTDC": 520, "LOCAL-ECOM": 510, "METRO-DTDC": 590, "METRO-ECOM": 580},
    {"Weight": 9.0, "LOCAL-DTDC": 550, "LOCAL-ECOM": 540, "METRO-DTDC": 620, "METRO-ECOM": 610},
    # మీ “400 లైన్ల” డేటా మిగిలినదంతా వరుసగా ఇక్కడ ఫిల్ చెయ్
]

# ==========================================
# 3. SECURITY & CSS (మీ డిజైన్ కి మ్యాచ్ అయ్యే స్టైల్)
# 4. MAIN CALCULATOR (logic: 8.75 → 9.0, 8.1 → 8.5, etc.)
# ==========================================
df_rates = pd.DataFrame(RATES_DATA)
# మీ ఎక్సెల్ లో ఉన్న unique weights & pincodes నే fetch చేస్తున్నాం → డ్రాప్‌డౌన్‌లు అలాగే వస్తాయి
weight_slabs = sorted(df_rates["Weight"].unique().tolist()) # ex: [0.5, 1.0, 1.5, ... 8.5, 9.0]

# మీ ఎక్సెల్ నుంచి PINCODE_MASTER → list (ఉదా: మీరు తర్వాత ఎక్సెల్ నుంచి df రీడ్ చేసి PINCODES list లాగా తీసుకుంటాం)
pincode_list = sorted(PINCODE_MASTER.keys()) # dropdown options for PINCODE

c1, c2 = st.columns([1, 1.2], gap="large")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📦 Booking Details")

    service = st.selectbox("NETWORK:", ["DTDC", "ECOM"], index=0)
    pincode = st.selectbox("PINCODE:", pincode_list, format_func=lambda x: str(x), index=0)

    st.markdown("<hr>", unsafe_allow_html=True)

    # మీ ఎక్సెల్ లో ఉన్న Weight slabs నే dropdown లాగా select చేయొచ్చు
    selected_wt = st.selectbox(
        "Weight (KG):",
        weight_slabs,
        format_func=lambda x: f"{x} KG",
        index=0,
    )

    st.write("📐 **Dimensions (Optional)**")
    d1, d2, d3 = st.columns(3)
    l = d1.number_input("L (cm)", value=0.0, step=1.0, format="%.1f", key="l")
    w = d2.number_input("W (cm)", value=0.0, step=1.0, format="%.1f", key="w")
    h = d3.number_input("H (cm)", value=0.0, step=1.0, format="%.1f", key="h")

    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    if pincode:
        zone = PINCODE_MASTER[pincode]
        vol_wt = (l * w * h) / 5000.0 if l and w and h else 0.0

        # Step 1: raw chargeable weight (actual slab vs volumetric)
        raw_wt = max(selected_wt, vol_wt)

        # Step 2: ఇప్పుడు మీ రేట్‌లో ఉన్న తర్వాత స్లాబ్‌కే ఎగిరించు (మీ మీది logic ప్రకారం)
        # ఉదా: 8.1 → 8.5; 8.75 → 9.0; 6.1 → 6.5; 6.6 → 7.0 అంటే,
        # weight_slabs లో ఉన్న మొదటి slab తీసుకోవాలి ఇది raw_wt కంటే ఎక్కువ / సమానం
        final_slab = min([x for x in weight_slabs if x >= raw_wt], default=max(weight_slabs))

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"📍 Zone: **{zone}** | Network: **{service}**")
        st.write(f"📊 Volumetric: **{round(vol_wt, 3)} KG**")
        st.markdown(f"<h3>Chargeable:
