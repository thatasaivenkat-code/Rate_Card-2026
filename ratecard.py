import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Vayu Vega Dashboard",
    page_icon="🚚",
    layout="wide"
)

# ==========================================
# 2. MODERN DASHBOARD CSS
# ==========================================
st.markdown("""
<style>

body {
    background-color: #f5f7fb;
}

/* Header */
.header {
    text-align: center;
    padding: 10px;
}
.header h1 {
    color: #111;
    font-weight: 800;
}
.header p {
    color: #777;
}

/* Card */
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Price Card */
.price-card {
    background: linear-gradient(135deg, #000000, #2c2c2c);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
}

.price {
    font-size: 60px;
    font-weight: 900;
    color: #00e676;
}

/* Inputs */
label {
    font-weight: bold !important;
    color: black !important;
}

/* Button */
.stButton>button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    background: #00c853;
    color: white;
    font-size: 18px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    if not os.path.exists("rates.xlsx"):
        return None, None

    try:
        s_df = pd.read_excel("rates.xlsx", sheet_name="States")
        s_df.columns = s_df.columns.str.strip().str.upper()

        r_df = pd.read_excel("rates.xlsx", sheet_name="Rates", header=2)
        r_df.columns = r_df.columns.str.strip()

        return s_df, r_df
    except:
        return None, None

state_df, rate_df = load_data()

# ==========================================
# 4. HEADER
# ==========================================
st.markdown("""
<div class="header">
    <h1>🚚 Vayu Vega Dashboard</h1>
    <p>Fast • Smart • Transparent Pricing</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. MAIN GRID
# ==========================================
if state_df is not None and rate_df is not None:

    col1, col2 = st.columns([1,1])

    # -------- LEFT PANEL --------
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        service = st.selectbox("🚛 Select Network", ["DTDC", "ECOM"])
        pincode = st.number_input("📍 Enter Pincode", value=0)

        st.markdown("### 📐 Dimensions (cm)")
        l, w, h = st.columns(3)

        with l:
            length = st.number_input("Length", value=0)
        with w:
            width = st.number_input("Width", value=0)
        with h:
            height = st.number_input("Height", value=0)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------- RIGHT PANEL --------
    with col2:

        if pincode > 0:
            match = state_df[state_df['PINCODE'] == pincode]

            if not match.empty:
                zone = str(match.iloc[0]['ZONE']).upper()

                clean_rates = rate_df.dropna(subset=['Weight'])
                weights = sorted(clean_rates['Weight'].unique())

                selected_kg = st.selectbox("⚖️ Select Weight", weights)

                if st.button("💰 Calculate Price"):

                    col_name = f"{zone}-{service}"

                    if col_name in clean_rates.columns:
                        try:
                            price = clean_rates.loc[
                                clean_rates['Weight'] == selected_kg,
                                col_name
                            ].values[0]

                            st.markdown(f"""
                            <div class="price-card">
                                <p>Shipping Cost</p>
                                <div class="price">₹{price}</div>
                                <p>
                                Zone: {zone} <br>
                                Service: {service} <br>
                                Weight: {selected_kg} kg <br>
                                Size: {length} x {width} x {height}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                            st.success("Price Calculated Successfully ✅")
                            st.balloons()

                        except:
                            st.error("❌ Rate not found")

            else:
                st.error("❌ Invalid Pincode")

else:
    st.warning("⚠️ Please keep rates.xlsx file in folder")

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<hr>
<center style='color:gray'>
Vayu Vega Enterprises • Gudiwada
</center>
""", unsafe_allow_html=True)
