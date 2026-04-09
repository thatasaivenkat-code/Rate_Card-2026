import streamlit as st
import pandas as pd
import os
import urllib.parse

# ==========================================
# 🔒 PASSWORD
# ==========================================
APP_PASSWORD = "vayu@123"
pwd = st.text_input("🔐 Enter Access Password", type="password")
if pwd != APP_PASSWORD:
    st.stop()

# ==========================================
# 🔒 HIDE GITHUB
# ==========================================
st.markdown("""
<style>
a[href*="github"] {display:none !important;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="Vayu Vega Pro", layout="wide")

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    if not os.path.exists("rates.xlsx"):
        return None, None
    
    s = pd.read_excel("rates.xlsx", sheet_name="States")
    s.columns = s.columns.str.strip().str.upper()

    r = pd.read_excel("rates.xlsx", sheet_name="Rates", header=2)
    r.columns = r.columns.str.strip()

    return s, r

state_df, rate_df = load_data()

# ==========================================
# HEADER
# ==========================================
st.title("🚚 Vayu Vega Smart Calculator")

if state_df is not None and rate_df is not None:

    c1, c2 = st.columns(2)

    # -------- INPUT --------
    with c1:
        st.markdown("### 📦 Input Details")

        service = st.selectbox("Courier", ["DTDC", "ECOM"])

        # 🔥 FILTER WEIGHT BASED ON COURIER
        clean = rate_df.dropna(subset=['Weight'])
        service_columns = [col for col in clean.columns if service in col]

        if service_columns:
            weights = sorted(clean['Weight'].unique().tolist())
        else:
            weights = []

        dead_weight = st.selectbox("Select Weight (KG)", weights)

        # 🔥 FILTER PINCODES BASED ON COURIER (only valid zones)
        valid_zones = [col.split("-")[0] for col in service_columns]
        valid_states = state_df[state_df['ZONE'].isin(valid_zones)]

        pincodes = sorted(valid_states['PINCODE'].unique().tolist())
        pincode = st.selectbox("Select Pincode", pincodes)

        # Dimensions
        st.markdown("### 📐 Dimensions (cm)")
        l = st.number_input("Length", value=0)
        w = st.number_input("Width", value=0)
        h = st.number_input("Height", value=0)

    # -------- CALCULATION --------
    with c2:

        match = state_df[state_df['PINCODE'] == pincode]

        if not match.empty:
            zone = str(match.iloc[0]['ZONE']).upper()

            # VOLUMETRIC
            volumetric_weight = (l * w * h) / 5000 if l and w and h else 0
            charge_weight = max(dead_weight, volumetric_weight)

            st.markdown("### 📊 Weight Details")
            st.write(f"Dead Weight: {dead_weight} KG")
            st.write(f"Volumetric Weight: {round(volumetric_weight,2)} KG")
            st.write(f"Chargeable Weight: {round(charge_weight,2)} KG")

            # CLOSEST WEIGHT MATCH
            selected = min(weights, key=lambda x: abs(x - charge_weight))

            col = f"{zone}-{service}"

            if col in clean.columns:

                price = clean.loc[
                    clean['Weight'] == selected,
                    col
                ].values[0]

                st.markdown(f"## 💰 Final Price: ₹{price}")

                # ALERT
                if volumetric_weight > dead_weight:
                    st.warning(
                        f"⚠️ Volumetric ({round(volumetric_weight,2)} KG) > Dead Weight → Charges volumetric weight ప్రకారం ఉంటాయి"
                    )

                # NOTICE
                st.info("📞 Courier queries: Sai - 8885999794")

                # WHATSAPP
                msg = f"Pincode:{pincode}, Service:{service}, Weight:{selected}, Price:{price}"
                url = f"https://wa.me/918885999794?text={urllib.parse.quote(msg)}"

                st.markdown(f"""
                <a href="{url}" target="_blank">
                    <button style="width:100%;background:#25D366;color:white;padding:12px;border:none;border-radius:8px;">
                        📲 WhatsApp Chat
                    </button>
                </a>
                """, unsafe_allow_html=True)

        else:
            st.error("Invalid Pincode")

else:
    st.warning("rates.xlsx file required")
