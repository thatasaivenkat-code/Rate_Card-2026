import streamlit as st
import pandas as pd
import os
import math

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Vayu Vega Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f4f7fb 0%, #eef3f9 100%);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.2rem;
    max-width: 1250px;
}

.main-title {
    padding: 20px 24px;
    border-radius: 24px;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.18);
    margin-bottom: 18px;
}

.main-title h1 {
    margin: 0;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.main-title p {
    margin: 8px 0 0;
    color: #cbd5e1;
    font-size: 15px;
}

.glass-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(226,232,240,0.9);
    backdrop-filter: blur(10px);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 10px 30px rgba(15,23,42,0.08);
    margin-bottom: 18px;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 14px;
}

.small-muted {
    color: #64748b;
    font-size: 13px;
    margin-top: -6px;
    margin-bottom: 10px;
}

.metric-box {
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 16px;
    text-align: center;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
}

.metric-label {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 6px;
    font-weight: 600;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #0f172a;
}

.result-card {
    background: linear-gradient(135deg, #052e16, #166534);
    border-radius: 24px;
    padding: 28px;
    color: white;
    box-shadow: 0 14px 36px rgba(22,101,52,0.28);
}

.result-card h2 {
    margin: 0 0 8px;
    font-size: 20px;
    font-weight: 700;
    color: #dcfce7;
}

.result-price {
    font-size: 56px;
    font-weight: 900;
    line-height: 1;
    margin: 10px 0 18px;
    color: #86efac;
}

.result-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 10px;
}

.result-item {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 12px;
}

.result-item span {
    display: block;
    color: #bbf7d0;
    font-size: 12px;
    margin-bottom: 4px;
}

.result-item strong {
    font-size: 15px;
    color: white;
}

.footer-box {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 8px;
    padding-bottom: 10px;
}

/* Streamlit widget polish */
.stSelectbox label, .stNumberInput label {
    font-weight: 700 !important;
    color: #0f172a !important;
}

.stSelectbox > div > div,
.stNumberInput > div > div > input {
    border-radius: 14px !important;
}

div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    min-height: 48px !important;
    border: 1px solid #dbe2ea !important;
    background: white !important;
}

.stNumberInput input {
    border-radius: 14px !important;
    min-height: 48px !important;
}

.stButton > button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 14px;
    background: linear-gradient(135deg, #16a34a, #15803d);
    color: white;
    font-size: 17px;
    font-weight: 800;
    box-shadow: 0 10px 24px rgba(22,163,74,0.22);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #15803d, #166534);
    color: white;
}

hr {
    margin-top: 24px !important;
    margin-bottom: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPERS
# ==========================================
@st.cache_data
def load_data():
    if not os.path.exists("rates.xlsx"):
        return None, None

    try:
        state_df = pd.read_excel("rates.xlsx", sheet_name="States")
        state_df.columns = state_df.columns.str.strip().str.upper()

        rate_df = pd.read_excel("rates.xlsx", sheet_name="Rates", header=2)
        rate_df.columns = rate_df.columns.str.strip()

        # clean state data
        if "PINCODE" in state_df.columns:
            state_df["PINCODE"] = pd.to_numeric(state_df["PINCODE"], errors="coerce")
            state_df = state_df.dropna(subset=["PINCODE"])
            state_df["PINCODE"] = state_df["PINCODE"].astype(int)

        if "ZONE" in state_df.columns:
            state_df["ZONE"] = state_df["ZONE"].astype(str).str.strip().str.upper()

        # clean rate data
        if "Weight" in rate_df.columns:
            rate_df["Weight"] = pd.to_numeric(rate_df["Weight"], errors="coerce")
            rate_df = rate_df.dropna(subset=["Weight"])
            rate_df["Weight"] = rate_df["Weight"].astype(float)

        return state_df, rate_df

    except Exception:
        return None, None


def get_available_services(rate_df):
    services = set()
    for col in rate_df.columns:
        if "-" in str(col):
            parts = str(col).split("-")
            if len(parts) >= 2:
                services.add(parts[-1].strip().upper())
    preferred = ["DTDC", "ECOM"]
    ordered = [x for x in preferred if x in services] + sorted([x for x in services if x not in preferred])
    return ordered if ordered else ["DTDC", "ECOM"]


def get_chargeable_weight(actual_weight, length, width, height, divisor=5000):
    volumetric_weight = (length * width * height) / divisor if all(v > 0 for v in [length, width, height]) else 0
    chargeable_weight = max(actual_weight, volumetric_weight)
    return round(volumetric_weight, 3), round(chargeable_weight, 3)


def find_rate_by_slab(rate_df, col_name, chargeable_weight):
    temp = rate_df[["Weight", col_name]].dropna().copy()
    temp = temp.sort_values("Weight")

    exact = temp[temp["Weight"] == chargeable_weight]
    if not exact.empty:
        return float(exact.iloc[0][col_name]), float(exact.iloc[0]["Weight"])

    higher = temp[temp["Weight"] >= chargeable_weight]
    if not higher.empty:
        return float(higher.iloc[0][col_name]), float(higher.iloc[0]["Weight"])

    # if chargeable weight is above max slab, use last available slab
    return float(temp.iloc[-1][col_name]), float(temp.iloc[-1]["Weight"])


def format_weight(x):
    try:
        x = float(x)
        if x.is_integer():
            return f"{int(x)} Kg"
        return f"{x:.3f} Kg"
    except:
        return str(x)


# ==========================================
# LOAD DATA
# ==========================================
state_df, rate_df = load_data()

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div class="main-title">
    <h1>🚚 Vayu Vega Pricing Dashboard</h1>
    <p>Fast • Smart • Transparent Courier Costing</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MAIN APP
# ==========================================
if state_df is None or rate_df is None:
    st.warning("⚠️ Please keep rates.xlsx file in the same folder.")
    st.stop()

required_state_cols = {"PINCODE", "ZONE"}
if not required_state_cols.issubset(set(state_df.columns)):
    st.error("States sheet must contain PINCODE and ZONE columns.")
    st.stop()

if "Weight" not in rate_df.columns:
    st.error("Rates sheet must contain Weight column.")
    st.stop()

services = get_available_services(rate_df)
pincode_list = sorted(state_df["PINCODE"].dropna().unique().tolist())
weight_list = sorted(rate_df["Weight"].dropna().unique().tolist())

left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Shipment Details</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">Select service, pincode, dimensions and actual weight.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        service = st.selectbox("🚛 Select Network", services)
    with c2:
        selected_pincode = st.selectbox(
            "📍 Select Pincode",
            options=pincode_list,
            format_func=lambda x: str(x)
        )

    match = state_df[state_df["PINCODE"] == selected_pincode]
    zone = str(match.iloc[0]["ZONE"]).upper() if not match.empty else ""

    c3, c4 = st.columns(2)
    with c3:
        actual_weight = st.selectbox(
            "⚖️ Actual Weight",
            options=weight_list,
            format_func=format_weight
        )
    with c4:
        divisor = st.selectbox(
            "📦 Volumetric Divisor",
            options=[5000, 6000],
            index=0,
            help="Most couriers use 5000 or 6000 based on tariff rules."
        )

    st.markdown("#### 📐 Package Dimensions (cm)")
    d1, d2, d3 = st.columns(3)
    with d1:
        length = st.number_input("Length", min_value=0.0, value=0.0, step=0.5)
    with d2:
        width = st.number_input("Width", min_value=0.0, value=0.0, step=0.5)
    with d3:
        height = st.number_input("Height", min_value=0.0, value=0.0, step=0.5)

    volumetric_weight, chargeable_weight = get_chargeable_weight(
        actual_weight, length, width, height, divisor=divisor
    )

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Zone</div>
            <div class="metric-value">{zone if zone else "-"}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Volumetric Wt</div>
            <div class="metric-value">{volumetric_weight:.3f}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Chargeable Wt</div>
            <div class="metric-value">{chargeable_weight:.3f}</div>
        </div>
        """, unsafe_allow_html=True)

    calculate = st.button("💰 Calculate Shipping Price")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Price Output</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">Final price is based on higher of actual weight or volumetric weight.</div>', unsafe_allow_html=True)

    if calculate:
        if not zone:
            st.error("❌ Selected pincode not mapped to any zone.")
        else:
            col_name = f"{zone}-{service}"

            if col_name not in rate_df.columns:
                st.error(f"❌ Rate column not found: {col_name}")
            else:
                try:
                    price, slab_used = find_rate_by_slab(rate_df, col_name, chargeable_weight)

                    basis = "Volumetric Weight" if volumetric_weight > actual_weight else "Actual Weight"

                    st.markdown(f"""
                    <div class="result-card">
                        <h2>Shipping Cost</h2>
                        <div class="result-price">₹{price:,.2f}</div>

                        <div class="result-grid">
                            <div class="result-item">
                                <span>Zone</span>
                                <strong>{zone}</strong>
                            </div>
                            <div class="result-item">
                                <span>Service</span>
                                <strong>{service}</strong>
                            </div>
                            <div class="result-item">
                                <span>Actual Weight</span>
                                <strong>{actual_weight} Kg</strong>
                            </div>
                            <div class="result-item">
                                <span>Volumetric Weight</span>
                                <strong>{volumetric_weight:.3f} Kg</strong>
                            </div>
                            <div class="result-item">
                                <span>Chargeable Weight</span>
                                <strong>{chargeable_weight:.3f} Kg</strong>
                            </div>
                            <div class="result-item">
                                <span>Rate Slab Used</span>
                                <strong>{slab_used} Kg</strong>
                            </div>
                            <div class="result-item">
                                <span>Calculation Basis</span>
                                <strong>{basis}</strong>
                            </div>
                            <div class="result-item">
                                <span>Dimensions</span>
                                <strong>{length} × {width} × {height} cm</strong>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.success("Price calculated successfully ✅")
                    st.balloons()

                except Exception as e:
                    st.error(f"❌ Error while calculating rate: {e}")
    else:
        st.info("Enter shipment details and click Calculate Shipping Price.")

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# OPTIONAL PREVIEW TABLES
# ==========================================
with st.expander("🔎 View Pincode Mapping"):
    preview_cols = [c for c in ["PINCODE", "ZONE"] if c in state_df.columns]
    st.dataframe(state_df[preview_cols].drop_duplicates().sort_values("PINCODE"), use_container_width=True)

with st.expander("📊 View Available Rate Slabs"):
    st.dataframe(rate_df, use_container_width=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="footer-box">
    Vayu Vega Enterprises • Gudivada
</div>
""", unsafe_allow_html=True)
