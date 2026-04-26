import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(page_title="Vayu Vega HD Pro", page_icon="🚚", layout="wide")

# Custom CSS for the "Card" look
st.markdown("""
    <style>
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }
    h3 {
        color: #1E3A8A;
        margin-top: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. INTERNAL DATA
# ==========================================
PINCODE_MASTER = {
    521301: "LOCAL", 521325: "LOCAL", 500001: "METRO",
    560001: "METRO", 110001: "NORTH", 600001: "SOUTH",
}

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
]

# ==========================================
# 3. PREPARATION
# ==========================================
df_rates = pd.DataFrame(RATES_DATA)
weight_slabs = sorted(df_rates["Weight"].unique().tolist())
pincode_list = sorted(PINCODE_MASTER.keys())

st.title("🚚 Vayu Vega Rate Calculator")

# ==========================================
# 4. MAIN UI
# ==========================================
c1, c2 = st.columns([1, 1.2], gap="large")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📦 Booking Details")

    service = st.selectbox("NETWORK:", ["DTDC", "ECOM"], index=0)
    pincode = st.selectbox("PINCODE:", pincode_list, format_func=lambda x: str(x), index=0)

    st.markdown("<hr>", unsafe_allow_html=True)

    selected_wt = st.selectbox(
        "Weight (KG):",
        weight_slabs,
        format_func=lambda x: f"{x} KG",
        index=0,
    )

    st.write("📐 **Dimensions (Optional)**")
    d1, d2, d3 = st.columns(3)
    l = d1.number_input("L (cm)", value=0.0, step=1.0, format="%.1f")
    w = d2.number_input("W (cm)", value=0.0, step=1.0, format="%.1f")
    h = d3.number_input("H (cm)", value=0.0, step=1.0, format="%.1f")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    if pincode:
        zone = PINCODE_MASTER[pincode]
        
        # Calculate Volumetric Weight
        vol_wt = (l * w * h) / 5000.0 if l and w and h else 0.0

        # Step 1: Compare actual weight with volumetric
        raw_wt = max(selected_wt, vol_wt)

        # Step 2: Find the next available weight slab
        try:
            final_slab = min([x for x in weight_slabs if x >= raw_wt])
        except ValueError:
            final_slab = max(weight_slabs) # Fallback to max if over limit

        # Step 3: Dynamic Price Lookup
        column_name = f"{zone}-{service}"
        
        # Check if the column exists in your data
        if column_name in df_rates.columns:
            price = df_rates.loc[df_rates["Weight"] == final_slab, column_name].values[0]
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(f"📍 Zone: **{zone}** | Network: **{service}**")
            st.write(f"📊 Volumetric Weight: **{round(vol_wt, 3)} KG**")
            
            # FIXED SYNTAX ERROR HERE:
            st.markdown(f"<h3>Chargeable Weight: {final_slab} KG</h3>", unsafe_allow_html=True)
            
            st.success(f"💰 Final Rate: ₹{price}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(f"Rate for {column_name} not found in the database.")
