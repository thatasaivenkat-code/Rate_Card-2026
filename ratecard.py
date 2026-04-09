import streamlit as st
import pandas as pd
import urllib.parse

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(page_title="Vayu Vega HD Pro", page_icon="🚚", layout="wide")

# ==========================================
# 2. INTERNAL DATA (ఇక్కడే నీ 400 లైన్ల డేటా ఉండాలి)
# ==========================================
# PINCODES & ZONES
PINCODE_MASTER = {
    521301: "LOCAL", 521325: "LOCAL", 500001: "METRO",
    560001: "METRO", 110001: "NORTH", 600001: "SOUTH"
    # నీ దగ్గర ఉన్న మిగిలిన పిన్‌కోడ్లు ఇక్కడ యాడ్ చెయ్...
}

# RATE CHART (Slabs)
# ఇక్కడ నువ్వు నీ ఎక్సెల్ లో ఉన్న రేట్లన్నీ వరుసగా పెట్టుకోవచ్చు
RATES_DATA = [
    {"Weight": 0.5, "LOCAL-DTDC": 40, "LOCAL-ECOM": 35, "METRO-DTDC": 60, "METRO-ECOM": 55},
    {"Weight": 1.0, "LOCAL-DTDC": 70, "LOCAL-ECOM": 65, "METRO-DTDC": 100, "METRO-ECOM": 90},
    {"Weight": 1.5, "LOCAL-DTDC": 100, "LOCAL-ECOM": 90, "METRO-DTDC": 140, "METRO-ECOM": 130},
    {"Weight": 2.0, "LOCAL-DTDC": 130, "LOCAL-ECOM": 120, "METRO-DTDC": 180, "METRO-ECOM": 170},
    {"Weight": 2.5, "LOCAL-DTDC": 160, "LOCAL-ECOM": 150, "METRO-DTDC": 220, "METRO-ECOM": 210},
    {"Weight": 3.0, "LOCAL-DTDC": 190, "LOCAL-ECOM": 180, "METRO-DTDC": 260, "METRO-ECOM": 250},
    # ఇలా నీ 400 లైన్ల డేటాని ఇక్కడ ఫిల్ చెయ్...
]

# ==========================================
# 3. SECURITY & CSS
# ==========================================
APP_PASSWORD = "vayu@123"
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Vayu Vega Login")
        pwd = st.text_input("Password", type="password")
        if st.button("Unlock"):
            if pwd == APP_PASSWORD:
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Wrong Password!")
    st.stop()

# CSS + Animation
st.markdown("""<style>
    .animation-wrap {
        width: 100%; height: 70px; position: relative;
        overflow: hidden; margin-bottom: 10px;
    }
    .moving-van {
        position: absolute; white-space: nowrap;
        animation: drive 10s linear infinite;
    }
    @keyframes drive { 0% { left: -250px; } 100% { left: 100%; } }
    .van-text {
        font-size: 26px; font-weight: 900; color: #075E54;
    }
# Weight slab list (your predefined slabs: 0.5, 1.0, 1.5, 2.0, 2.5, ...)
weight_slabs = sorted(df_rates['Weight'].unique().tolist())

# Pincode list (dropdown)
pincode_list = sorted(list(PINCODE_MASTER.keys()))

# Layout
c1, c2 = st.columns([1, 1.2], gap="large")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📦 Booking Details")

    # Dropdown for network
    service = st.selectbox("NETWORK:", ["DTDC", "ECOM"], index=0)

    # Dropdown for PINCODE
    pincode = st.selectbox("PINCODE:", pincode_list, index=0)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Dropdown for WEIGHT (only predefined slabs)
    selected_wt = st.selectbox("Weight (KG):", weight_slabs, index=0)

    st.write("📐 **Dimensions (Optional)**")
    d1, d2, d3 = st.columns(3)
    l = d1.number_input("L (cm)", value=0, step=1.0, format="%.1f")
    w = d2.number_input("W (cm)", value=0, step=1.0, format="%.1f")
    h = d3.number_input("H (cm)", value=0, step=1.0, format="%.1f")

    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    if pincode:
        zone = PINCODE_MASTER[pincode]
        vol_wt = (l * w * h) / 5000.0 if l and w and h else 0.0

        # Final weight = max(Actual slab, volumetric slab) → then map to next slab
        raw_wt = max(selected_wt, vol_wt)

        # Map raw_wt to the next slab in your weight_slabs list
        # Find the smallest slab that is >= raw_wt
        final_slab = min([x for x in weight_slabs if x >= raw_wt], default=max(weight_slabs))

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"📍 Zone: **{zone}** | Network: **{service}**")
        st.write(f"📊 Volumetric: **{round(vol_wt, 2)} KG**")
        st.markdown(f"<h3>Chargeable: {final_slab} KG</h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        target_col = f"{zone}-{service}"

        if target_col in df_rates.columns:
            price = df_rates.loc[df_rates['Weight'] == final_slab, target_col].values[0]

            st.markdown(f"""<div class="price-card">
                <p style="opacity:0.7;">SHIPPING PRICE</p>
                <div class="price">₹{price}</div>
                <p>Weight Slab: {final_slab} KG</p>
            </div>""", unsafe_allow_html=True)

            # WhatsApp button
            wa_msg = urllib.parse.quote(
                f"Vayu Vega Booking:
Pin: {pincode}
Weight: {final_slab}kg
Price: ₹{price}"
            )
            st.markdown(f"""<a href="https://wa.me/918885999794?text={wa_msg}" target="_blank">
                <button style="width:100%; background:#25D366; color:white; padding:15px; border:none; border-radius:12px; font-weight:bold; margin-top:15px; cursor:pointer;">
                    📲 Share on WhatsApp
                </button>
            </a>""", unsafe_allow_html=True)

            st.balloons()

st.markdown(
    "<p style='text-align:center; color:grey; font-size:12px; margin-top:50px;'>© Vayu Vega Logistics</p>",
    unsafe_allow_html=True
)
