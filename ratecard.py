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
# SETTINGS
# ==========================================
WHATSAPP_NUMBER = "918885999794"   # <-- Mee WhatsApp number international format lo ivvandi
WHATSAPP_MESSAGE = "Hello Vayu Vega, I need support regarding courier price quotation."

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f4f7fb 0%, #eef3f9 100%);
}

.block-container {
    max-width: 1250px;
    padding-top: 1.2rem;
    padding-bottom: 1.5rem;
}

.main-title {
    padding: 22px 24px;
    border-radius: 24px;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.18);
    margin-bottom: 20px;
}

.main-title h1 {
    margin: 0;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.4px;
}

.main-title p {
    margin: 7px 0 0;
    color: #cbd5e1;
    font-size: 14px;
}

.glass-card {
    background: rgba(255,255,255,0.86);
    border: 1px solid rgba(226,232,240,0.95);
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
    margin-bottom: 8px;
}

.small-muted {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 14px;
}

.metric-box {
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 14px 12px;
    text-align: center;
    min-height: 92px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.metric-label {
    font-size: 12px;
    color: #64748b;
    margin-bottom: 6px;
    font-weight: 700;
}

.metric-value {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
}

.result-shell {
    background: linear-gradient(135deg, #052e16, #166534);
    border-radius: 24px;
    padding: 24px;
    color: white;
    box-shadow: 0 14px 36px rgba(22,101,52,0.28);
    margin-top: 10px;
}

.result-shell h2 {
    margin: 0 0 8px 0;
    color: #dcfce7;
    font-size: 20px;
    font-weight: 800;
}

.result-price {
    font-size: 56px;
    font-weight: 900;
    line-height: 1;
    color: #86efac;
    margin-bottom: 16px;
}

.info-tile {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 12px 14px;
    min-height: 82px;
}

.info-tile .label {
    color: #bbf7d0;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 6px;
}

.info-tile .value {
    color: white;
    font-size: 15px;
    font-weight: 800;
    line-height: 1.35;
    word-break: break-word;
}

.notify-box {
    margin-top: 18px;
    padding: 16px 18px;
    border-radius: 18px;
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    border: 1px solid #a7f3d0;
    box-shadow: 0 8px 20px rgba(16,185,129,0.12);
}

.notify-title {
    font-size: 15px;
    font-weight: 800;
    color: #065f46;
    margin-bottom: 6px;
}

.notify-text {
    font-size: 13px;
    color: #065f46;
    margin-bottom: 10px;
}

.whatsapp-link a {
    display: inline-block;
    text-decoration: none;
    background: #16a34a;
    color: white !important;
    padding: 10px 16px;
    border-radius: 12px;
    font-weight: 800;
    box-shadow: 0 8px 18px rgba(22,163,74,0.24);
}

.whatsapp-link a:hover {
    background: #15803d;
}

.footer-box {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 8px;
    padding-bottom: 10px;
}

/* Widget styling */
.stSelectbox label, .stNumberInput label {
    font-weight: 700 !important;
    color: #0f172a !important;
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

div[data-testid="stExpander"] {
    border-radius: 18px !important;
    border: 1px solid #e2e8f0 !important;
    overflow: hidden;
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

        if "PINCODE" in state_df.columns:
            state_df["PINCODE"] = pd.to_numeric(state_df["PINCODE"], errors="coerce")
            state_df = state_df.dropna(subset=["PINCODE"])
            state_df["PINCODE"] = state_df["PINCODE"].astype(int)

        if "ZONE" in state_df.columns:
            state_df["ZONE"] = state_df["ZONE"].astype(str).str.strip().str.upper()

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
    if all(v > 0 for v in [length, width, height]):
        volumetric_weight = (length * width * height) / divisor
    else:
        volumetric_weight = 0

    chargeable_weight = max(actual_weight, volumetric_weight)
    return round(volumetric_weight, 3), round(chargeable_weight, 3)


def find_rate_by_slab(rate_df, col_name, chargeable_weight):
    temp = rate_df[["Weight", col_name]].dropna().copy()
    temp = temp.sort_values("Weight").reset_index(drop=True)

    exact = temp[temp["Weight"] == chargeable_weight]
    if not exact.empty:
        return float(exact.iloc[0][col_name]), float(exact.iloc[0]["Weight"])

    higher = temp[temp["Weight"] >= chargeable_weight]
    if not higher.empty:
        return float(higher.iloc[0][col_name]), float(higher.iloc[0]["Weight"])

    return float(temp.iloc[-1][col_name]), float(temp.iloc[-1]["Weight"])


def format_weight(x):
    x = float(x)
    if x.is_integer():
        return f"{int(x)} Kg"
    return f"{x:.3f} Kg"


def build_whatsapp_link(number, message):
    clean_number = "".join(ch for ch in str(number) if ch.isdigit())
    encoded_message = message.replace(" ", "%20")
    return f"https://wa.me/{clean_number}?text={encoded_message}"


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

left, right = st.columns([1.08, 0.92], gap="large")

# ==========================================
# LEFT PANEL
# ==========================================
with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Shipment Details</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">Select service, pincode, actual weight and package dimensions.</div>', unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    with a1:
        service = st.selectbox("🚛 Select Network", services)
    with a2:
        selected_pincode = st.selectbox(
            "📍 Select Pincode",
            options=pincode_list,
            format_func=lambda x: str(x)
        )

    selected_row = state_df[state_df["PINCODE"] == selected_pincode]
    zone = str(selected_row.iloc[0]["ZONE"]).upper() if not selected_row.empty else ""

    a3, a4 = st.columns(2)
    with a3:
        actual_weight = st.selectbox(
            "⚖️ Select Actual Weight",
            options=weight_list,
            format_func=format_weight
        )
    with a4:
        divisor = st.selectbox(
            "📦 Volumetric Divisor",
            options=[5000, 6000],
            index=0,
            help="Courier rule batti divisor change avvachu."
        )

    st.markdown("#### 📐 Dimensions (cm)")
    d1, d2, d3 = st.columns(3)
    with d1:
        length = st.number_input("Length", min_value=0.0, value=0.0, step=0.5)
    with d2:
        width = st.number_input("Width", min_value=0.0, value=0.0, step=0.5)
    with d3:
        height = st.number_input("Height", min_value=0.0, value=0.0, step=0.5)

    volumetric_weight, chargeable_weight = get_chargeable_weight(
        actual_weight, length, width, height, divisor
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

# ==========================================
# RIGHT PANEL
# ==========================================
with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Price Output</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">Final price is based on the higher of actual or volumetric weight.</div>', unsafe_allow_html=True)

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
                    wa_link = build_whatsapp_link(
                        WHATSAPP_NUMBER,
                        f"{WHATSAPP_MESSAGE} Zone: {zone}, Service: {service}, Chargeable Weight: {chargeable_weight} Kg, Price: ₹{price:,.2f}"
                    )

                    st.markdown(f"""
                    <div class="result-shell">
                        <h2>Shipping Cost</h2>
                        <div class="result-price">₹{price:,.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    r1, r2 = st.columns(2)
                    with r1:
                        st.markdown(f"""
                        <div class="info-tile">
                            <div class="label">Zone</div>
                            <div class="value">{zone}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="info-tile">
                            <div class="label">Actual Weight</div>
                            <div class="value">{actual_weight} Kg</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="info-tile">
                            <div class="label">Chargeable Weight</div>
                            <div class="value">{chargeable_weight:.3f} Kg</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="info-tile">
                            <div class="label">Calculation Basis</div>
                            <div class="value">{basis}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with r2:
                        st.markdown(f"""
                        <div class="info-tile">
                            <div class="label">Service</div>
                            <div class="value">{service}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="info-tile">
                            <div class="label">Volumetric Weight</div>
                            <div class="value">{volumetric_weight:.3f} Kg</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="info-tile">
                            <div class="label">Rate Slab Used</div>
                            <div class="value">{slab_used} Kg</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="info-tile">
                            <div class="label">Dimensions</div>
                            <div class="value">{length} × {width} × {height} cm</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="notify-box">
                        <div class="notify-title">📲 Need instant confirmation?</div>
                        <div class="notify-text">
                            For booking/support, click the WhatsApp number below and continue directly in WhatsApp.
                        </div>
                        <div class="whatsapp-link">
                            <a href="{wa_link}" target="_blank" rel="noopener noreferrer">
                                WhatsApp: {WHATSAPP_NUMBER}
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.success("Price calculated successfully ✅")

                except Exception as e:
                    st.error(f"❌ Error while calculating rate: {e}")
    else:
        st.info("Enter shipment details and click Calculate Shipping Price.")

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# EXTRA TABLES
# ==========================================
with st.expander("🔎 View Pincode Mapping"):
    preview_cols = [c for c in ["PINCODE", "ZONE"] if c in state_df.columns]
    st.dataframe(
        state_df[preview_cols].drop_duplicates().sort_values("PINCODE"),
        use_container_width=True
    )

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
