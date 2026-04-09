import streamlit as st
import pandas as pd
import os
import urllib.parse

# ==========================================
# 🔒 SECURITY (PASSWORD)
# ==========================================
APP_PASSWORD = "vayu@123"

pwd = st.text_input("🔐 Enter Access Password", type="password")

if pwd != APP_PASSWORD:
    st.warning("🔒 Unauthorized Access")
    st.stop()

# ==========================================
# 🔒 HIDE GITHUB ICON
# ==========================================
st.markdown("""
<style>
a[href*="github"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(page_title="Vayu Vega Pro", layout="wide")

# ==========================================
# CSS
# ==========================================
st.markdown("""
<style>
.card {background:white;padding:20px;border-radius:15px;box-shadow:0 6px 15px rgba(0,0,0,0.08);margin-bottom:20px;}
.price-card {background:black;color:white;padding:25px;border-radius:15px;text-align:center;}
.price {font-size:50px;color:#00e676;font-weight:900;}
.alert {background:#fff3cd;padding:15px;border-radius:10px;color:#856404;margin-top:15px;border:1px solid #ffeeba;}
.note {background:#e3f2fd;padding:15px;border-radius:10px;color:#0d47a1;margin-top:15px;border:1px solid #90caf9;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    if not os.path.exists("rates.xlsx"):
        return None, None
    try:
        s = pd.read_excel("rates.xlsx", sheet_name="States")
        s.columns = s.columns.str.strip().str.upper()

        r = pd.read_excel("rates.xlsx", sheet_name="Rates", header=2)
        r.columns = r.columns.str.strip()
        return s, r
    except:
        return None, None

state_df, rate_df = load_data()

# ==========================================
# HEADER
# ==========================================
st.title("🚚 Vayu Vega Smart Calculator")

# ==========================================
# MAIN
# ==========================================
if state_df is not None and rate_df is not None:

    c1, c2 = st.columns(2)

    # -------- INPUT --------
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        service = st.selectbox("Courier", ["DTDC", "ECOM"])
        pincode = st.number_input("Pincode", value=0)

        st.subheader("📦 Weight")
        dead_weight = st.number_input("Dead Weight (KG)", value=0.5)

        st.subheader("📐 Dimensions (cm)")
        l = st.number_input("Length", value=0)
        w = st.number_input("Width", value=0)
        h = st.number_input("Height", value=0)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------- CALCULATION --------
    with c2:
        if pincode > 0:

            match = state_df[state_df['PINCODE'] == pincode]

            if not match.empty:
                zone = str(match.iloc[0]['ZONE']).upper()

                # VOLUMETRIC
                volumetric_weight = (l * w * h) / 5000 if l and w and h else 0

                # FINAL WEIGHT
                charge_weight = max(dead_weight, volumetric_weight)

                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.write(f"📊 Dead Weight: {dead_weight} KG")
                st.write(f"📊 Volumetric Weight: {round(volumetric_weight,2)} KG")
                st.write(f"✅ Chargeable Weight: {round(charge_weight,2)} KG")

                st.markdown('</div>', unsafe_allow_html=True)

                # RATE CALC
                clean = rate_df.dropna(subset=['Weight'])
                weights = sorted(clean['Weight'].unique())

                selected = min(weights, key=lambda x: abs(x - charge_weight))
                col = f"{zone}-{service}"

                if col in clean.columns:

                    price = clean.loc[
                        clean['Weight'] == selected,
                        col
                    ].values[0]

                    # PRICE DISPLAY
                    st.markdown(f"""
                    <div class="price-card">
                        <p>Final Charge</p>
                        <div class="price">₹{price}</div>
                        <p>Weight Used: {selected} KG</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # ⚠️ ALERT
                    if volumetric_weight > dead_weight:
                        st.markdown(f"""
                        <div class="alert">
                        ⚠️ Volumetric Weight ({round(volumetric_weight,2)} KG) ఎక్కువగా ఉంది.<br>
                        Charges volumetric weight ప్రకారం తీసుకుంటారు.
                        </div>
                        """, unsafe_allow_html=True)

                    # 📢 NOTICE
                    st.markdown("""
                    <div class="note">
                    📢 <b>Customer Support:</b><br><br>
                    📞 Sai: 8885999794<br>
                    👉 Courier related queries కోసం సంప్రదించండి
                    </div>
                    """, unsafe_allow_html=True)

                    # 📲 WHATSAPP BUTTON
                    phone_number = "918885999794"

                    message = f"""
Hello Sai Garu,

I checked shipping in Vayu Vega App.

Pincode: {pincode}
Service: {service}
Weight: {selected} KG
Price: ₹{price}

Please assist.
"""

                    encoded = urllib.parse.quote(message)
                    url = f"https://wa.me/{phone_number}?text={encoded}"

                    st.markdown(f"""
                    <a href="{url}" target="_blank">
                        <button style="
                            width:100%;
                            background:#25D366;
                            color:white;
                            padding:15px;
                            border:none;
                            border-radius:10px;
                            font-size:18px;
                            font-weight:bold;
                            margin-top:15px;">
                            📲 Chat on WhatsApp
                        </button>
                    </a>
                    """, unsafe_allow_html=True)

                    st.success("Calculated ✅")

            else:
                st.error("Invalid Pincode")

else:
    st.warning("⚠️ rates.xlsx file folder lo undali")
