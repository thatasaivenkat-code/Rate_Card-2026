import streamlit as st
import pandas as pd
import urllib.parse

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(page_title="Vayu Vega HD Pro", page_icon="🚚", layout="wide")

# ==========================================
# 2. INTERNAL DATA
# ==========================================
PINCODE_MASTER = {
    521301: "LOCAL", 521325: "LOCAL", 500001: "METRO",
    560001: "METRO", 110001: "NORTH", 600001: "SOUTH"
    # మీ అన్ని పిన్‌కోడ్లు యాడ్ చెయ్...
}

# RATES_DATA: మీ “400 లైన్ల” డేటా ఇక్కడ వరుసగా ఉండాలి (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5...)
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
    # ఇలా మీ మిగిలిన 400 లైన్ల డేటా వరుసగా ఫిల్ చెయ్...
]

# ==========================================
# 3. SECURITY & CSS (మీ స్టైల్ కి మార్పు లేదు)
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

st.markdown("""<style>
# 4. MAIN CALCULATOR (ఇక్కడ మాత్రం logic మార్చాను)
# ==========================================
df_rates = pd.DataFrame(RATES_DATA)
weight_slabs = sorted(df_rates['Weight'].unique().tolist()) # ex: [0.5, 1.0, 1.5, 2.0, 2.5, ...]
pincode_list = sorted(list(PINCODE_MASTER.keys()))

c1, c2 = st.columns([1, 1.2], gap="large")

with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📦 Booking Details")

    service = st.selectbox("NETWORK:", ["DTDC", "ECOM"], index=0)
    pincode = st.selectbox("PINCODE:", pincode_list, index=0)

    st.markdown("<hr>", unsafe_allow_html=True)

    selected_wt = st.selectbox("Weight (KG):", weight_slabs, index=0)

    st.write("📐 **Dimensions (Optional)**")
    d1, d2, d3 = st.columns(3)
    l = d1.number_input("L (cm)", value=0.0, step=1.0, format="%.1f")
    w = d2.number_input("W (cm)", value=0.0, step=1.0, format="%.1f")
    h = d3.number_input("H (cm)", value=0.0, step=1.0, format="%.1f")

    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    if pincode:
        zone = PINCODE_MASTER[pincode]
        vol_wt = (l * w * h) / 5000.0 if l and w and h else 0.0

        # Step 1: raw chargeable weight = max(selected slab, volumetric weight)
        raw_wt = max(selected_wt, vol_wt)

        # Step 2: ఇక్కడ మీ logic రూల్స్ అమలు
        # - మీ రేట్ స్లాబ్ లిస్ట్ లో ఉన్న తర్వాత స్లాబ్ కనుక్కోండి
        # - ఉదా: 6.1 → 6.5; 6.6 → 7.0; 6.75 → 7.0
        # అంటే: మీ ముందుగా ఉన్న slab కంటే ఎక్కువ / సమానం అయ్యే మొదటి slab తీసుకోండి
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
