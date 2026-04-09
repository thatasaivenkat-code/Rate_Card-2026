import streamlit as st
import pandas as pd
import os
import urllib.parse

# ==========================================
# 1. PAGE CONFIG & THEME
# ==========================================
st.set_page_config(
    page_title="Vayu Vega HD Pro",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. SECURITY (PASSWORD)
# ==========================================
APP_PASSWORD = "vayu@123"

# Custom CSS for Login Page
st.markdown("""
<style>
    .stTextInput label { color: black !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/726/726455.png", width=100)
        st.title("🔐 Access Portal")
        pwd = st.text_input("Enter Access Password", type="password")
        if st.button("Unlock Dashboard"):
            if pwd == APP_PASSWORD:
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("❌ Incorrect Password")
    st.stop()

# ==========================================
# 3. PREMIUM CSS & ANIMATION
# ==========================================
st.markdown("""
<style>
    /* Hide GitHub Icon */
    a[href*="github"] { display: none !important; }
    
    .main { background-color: #f8f9fa; }
    
    /* Animation Container */
    .animation-wrap {
        width: 100%; height: 80px; position: relative;
        overflow: hidden; background: transparent; margin-bottom: 10px;
    }
    .moving-van {
        position: absolute; white-space: nowrap;
        animation: drive 12s linear infinite;
    }
    @keyframes drive {
        0% { left: -250px; }
        100% { left: 100%; }
    }
    .van-text { font-size: 28px; font-weight: 900; color: #075E54; font-family: sans-serif; }

    /* Cards Styling */
    .card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.06); margin-bottom: 20px; border: 1px solid #eee; }
    label { color: black !important; font-weight: bold !important; font-size: 16px !important; }
    
    /* Result Styling */
    .price-card { background: #111; color: white; padding: 30px; border-radius: 20px; text-align: center; border-bottom: 6px solid #25D366; }
    .price { font-size: 60px; color: #25D366; font-weight: 900; margin: 10px 0; }
    
    /* Alert & Notes */
    .alert-box { background: #fff3cd; padding: 15px; border-radius: 12px; color: #856404; border-left: 6px solid #ffc107; margin-top: 15px; }
    .support-box { background: #e3f2fd; padding: 15px; border-radius: 12px; color: #0d47a1; border-left: 6px solid #2196f3; margin-top: 15px; }
</style>

<div class="animation-wrap">
    <div class="moving-van">
        <span style="font-size:40px;">🚚</span>
        <span class="van-text">VAYU VEGA HD PRO</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. LOAD DATA (EXCEL)
# ==========================================
@st.cache_data
def load_all_data():
    if not os.path.exists("rates.xlsx"):
        return None, None
    try:
        s = pd.read_excel("rates.xlsx", sheet_name="States")
        s.columns = s.columns.str.strip().str.upper()

        r = pd.read_excel("rates.xlsx", sheet_name="Rates", header=2)
        r.columns = r.columns.str.strip()
        return s, r
    except Exception as e:
        st.error(f"Error loading Excel: {e}")
        return None, None

state_df, rate_df = load_all_data()

# ==========================================
# 5. MAIN INTERFACE
# ==========================================
st.markdown("<h2 style='text-align: center; color: #111;'>Smart Rate Calculator</h2>", unsafe_allow_html=True)

if state_df is not None and rate_df is not None:

    col1, col2 = st.columns([1, 1.2], gap="large")

    # --- LEFT: INPUTS ---
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📍 Booking Details")
        
        service = st.selectbox("Select Courier Network", ["DTDC", "ECOM"])
        pincode = st.number_input("Enter Destination Pincode", value=0, step=1)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("⚖️ Weight & Size")
        dead_weight = st.number_input("Actual Weight (KG)", value=0.5, step=0.1)
        
        st.write("📐 **Dimensions (cm)**")
        d1, d2, d3 = st.columns(3)
        with d1: l = st.number_input("Length", value=0, min_value=0)
        with d2: w = st.number_input("Width", value=0, min_value=0)
        with d3: h = st.number_input("Height", value=0, min_value=0)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- RIGHT: CALCULATIONS & RESULTS ---
    with col2:
        if pincode > 0:
            match = state_df[state_df['PINCODE'] == pincode]

            if not match.empty:
                zone = str(match.iloc[0]['ZONE']).upper()

                # Volumetric Calculation (Formula: L*W*H / 5000)
                vol_weight = (l * w * h) / 5000 if l and w and h else 0
                # Final Weight (Max of Actual or Volumetric)
                charge_weight = max(dead_weight, vol_weight)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("📋 Weight Analysis")
                st.write(f"🔹 Actual Weight: **{dead_weight} KG**")
                st.write(f"🔹 Volumetric Weight: **{round(vol_weight, 2)} KG**")
                st.markdown(f"<h3 style='color:#075E54;'>✅ Chargeable Weight: {round(charge_weight, 2)} KG</h3>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Rate Retrieval
                clean_rates = rate_df.dropna(subset=['Weight'])
                weights_list = sorted(clean_rates['Weight'].unique())

                # Finding the closest matching weight in Excel
                # If charge_weight is 1.2, it finds 1.5 or 2 based on your Excel rows
                selected_row_weight = min([x for x in weights_list if x >= charge_weight], default=max(weights_list))
                
                target_col = f"{zone}-{service}"

                if target_col in clean_rates.columns:
                    try:
                        price = clean_rates.loc[clean_rates['Weight'] == selected_row_weight, target_col].values[0]

                        # --- PRICE CARD DISPLAY ---
                        st.markdown(f"""
                        <div class="price-card">
                            <p style="margin:0; opacity:0.7;">TOTAL SHIPPING FEE</p>
                            <div class="price">₹{price}</div>
                            <p style="margin:0;">Applied Weight: {selected_row_weight} KG</p>
                            <p style="font-size:12px; opacity:0.5;">Zone: {zone} | Network: {service}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Volumetric Warning
                        if vol_weight > dead_weight:
                            st.markdown(f"""
                            <div class="alert-box">
                                ⚠️ <b>Volumetric Alert:</b><br>
                                పార్సెల్ సైజు ఎక్కువగా ఉంది ({round(vol_weight,2)} KG). కాబట్టి Weight కంటే Size కి చార్జ్ పడుతుంది.
                            </div>
                            """, unsafe_allow_html=True)

                        # Support Box
                        st.markdown("""
                        <div class="support-box">
                            <b>📞 Customer Support:</b><br>
                            Sai: <b>8885999794</b><br>
                            ఏవైనా సందేహాలు ఉంటే కాల్ చేయండి.
                        </div>
                        """, unsafe_allow_html=True)

                        # --- WHATSAPP BUTTON ---
                        wa_phone = "918885999794"
                        wa_msg = f"""Hello Sai Garu,
I checked shipping in Vayu Vega App.

📍 Pincode: {pincode}
🚚 Service: {service}
⚖️ Weight: {charge_weight} KG (Applied: {selected_row_weight} KG)
📐 Dimensions: {l}x{w}x{h} cm
💰 Price: ₹{price}

Please assist with the booking."""
                        
                        encoded_msg = urllib.parse.quote(wa_msg)
                        wa_url = f"https://wa.me/{wa_phone}?text={encoded_msg}"

                        st.markdown(f"""
                        <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                            <button style="width:100%; background:#25D366; color:white; padding:18px; border:none; border-radius:15px; font-size:20px; font-weight:bold; cursor:pointer; margin-top:15px; box-shadow: 0 4px 15px rgba(37,211,102,0.3);">
                                📲 Share on WhatsApp
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
                        st.success("Calculation Successful ✅")
                        st.balloons()

                    except Exception:
                        st.error("❌ ఈ బరువుకు రేట్ కార్డులో ధర లేదు.")
                else:
                    st.error(f"❌ Column '{target_col}' not found in Excel.")
            else:
                st.error("❌ Invalid Pincode / Service Not Available")
        else:
            st.info("💡 వివరాలు ఎంటర్ చేస్తే ఇక్కడ రేట్ కనిపిస్తుంది.")

else:
    st.warning("⚠️ **rates.xlsx** ఫైల్ దొరకలేదు. దయచేసి అదే ఫోల్డర్ లో ఉంచండి.")

st.markdown("<br><hr><p style='text-align: center; font-size: 12px; color: #999;'>Vayu Vega Enterprises | Gudiwada Automation</p>", unsafe_allow_html=True)
