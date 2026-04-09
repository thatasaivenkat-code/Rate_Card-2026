import streamlit as st
import pandas as pd
import os
import urllib.parse

# ==========================================
# 1. PAGE CONFIGURATION
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

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("""
        <style>
        .login-box {
            background-color: white; padding: 40px; border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/726/726455.png", width=80)
        st.header("🔐 Vayu Vega Access")
        pwd = st.text_input("Please Enter Password", type="password")
        if st.button("Unlock Dashboard"):
            if pwd == APP_PASSWORD:
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("❌ Invalid Password!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# 3. PREMIUM CSS & VAN ANIMATION
# ==========================================
st.markdown("""
<style>
    /* Hide Streamlit Header Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    a[href*="github"] { display: none !important; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: #075E54; border-radius: 10px; }

    /* Moving Van Animation */
    .animation-container {
        width: 100%; height: 90px; position: relative;
        overflow: hidden; background: transparent; border-bottom: 2px solid #eee;
    }
    .moving-group {
        position: absolute; white-space: nowrap;
        animation: driveVan 12s linear infinite;
        display: flex; align-items: center;
    }
    @keyframes driveVan {
        0% { left: -300px; }
        100% { left: 100%; }
    }
    .van-icon { font-size: 45px; margin-right: 15px; }
    .van-label { 
        font-size: 30px; font-weight: 900; color: #075E54; 
        font-family: 'Arial Black', sans-serif; letter-spacing: 2px;
    }

    /* Professional UI Cards */
    .card { 
        background: white; padding: 25px; border-radius: 20px; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.06); margin-bottom: 20px; 
        border: 1px solid #f0f0f0; 
    }
    
    /* Global Label Styling - Pure Black */
    label, .stSelectbox p, .stNumberInput p { 
        color: #000000 !important; font-weight: 800 !important; font-size: 16px !important; 
    }

    /* Result Price Card */
    .price-card { 
        background: #000000; color: #ffffff; padding: 35px; 
        border-radius: 25px; text-align: center; 
        border-bottom: 8px solid #25D366; box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    .price-value { font-size: 65px; font-weight: 900; color: #25D366; margin: 10px 0; }
    
    /* Support & Info Boxes */
    .info-box { 
        background: #e3f2fd; padding: 15px; border-radius: 12px; 
        color: #0d47a1; border-left: 6px solid #2196f3; font-size: 14px;
    }
</style>

<div class="animation-container">
    <div class="moving-group">
        <span class="van-icon">🚚</span>
        <span class="van-label">VAYU VEGA HD PRO</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. DATA ENGINE (OPTIMIZED FOR 400+ ROWS)
# ==========================================
@st.cache_data
def load_excel_data():
    file = "rates.xlsx"
    if not os.path.exists(file):
        return None, None
    try:
        # Load States Sheet
        s_df = pd.read_excel(file, sheet_name="States")
        s_df.columns = s_df.columns.str.strip().str.upper()
        
        # Load Rates Sheet (Header at A3)
        r_df = pd.read_excel(file, sheet_name="Rates", header=2)
        r_df.columns = r_df.columns.str.strip()
        return s_df, r_df
    except Exception as e:
        st.error(f"Excel Error: {e}")
        return None, None

state_df, rate_df = load_excel_data()

# ==========================================
# 5. MAIN APP INTERFACE
# ==========================================
if state_df is not None and rate_df is not None:
    
    # Cleaning Rate Data
    clean_rates = rate_df.dropna(subset=['Weight'])
    
    # Dashboard Columns
    col_in, col_out = st.columns([1, 1.2], gap="large")

    # --- LEFT SIDE: INPUTS ---
    with col_in:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📍 Booking Details")
        
        # Network Dropdown
        service = st.selectbox("Courier Network ఎంచుకోండి", ["DTDC", "ECOM"])
        
        # Pincode Dropdown (Unique & Sorted)
        pincodes = sorted(state_df['PINCODE'].unique().tolist())
        selected_pin = st.selectbox("Destination Pincode ఎంచుకోండి", pincodes)

        st.markdown("<hr style='opacity:0.3;'>", unsafe_allow_html=True)
        st.subheader("⚖️ Weight Parameters")
        
        # Weight Dropdown from Excel
        excel_weights = sorted(clean_rates['Weight'].unique().tolist())
        base_weight = st.selectbox("బరువు (Select Weight KG)", excel_weights)

        st.markdown("📐 **Dimensions (cm) - Optional**")
        d1, d2, d3 = st.columns(3)
        with d1: l = st.number_input("Length", min_value=0, value=0)
        with d2: w = st.number_input("Width", min_value=0, value=0)
        with d3: h = st.number_input("Height", min_value=0, value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- RIGHT SIDE: RESULTS ---
    with col_out:
        if selected_pin:
            # Get Zone
            match = state_df[state_df['PINCODE'] == selected_pin]
            zone = str(match.iloc[0]['ZONE']).upper()

            # 1. Volumetric Weight Calculation
            vol_wt = (l * w * h) / 5000 if l and w and h else 0
            
            # 2. Chargeable Weight (Max of Selected vs Volumetric)
            final_wt = max(base_weight, vol_wt)
            
            # 3. Finding the next available slab in Excel for the final weight
            # If final_wt is 1.2, it will find 1.5 or 2.0 from your list
            applied_slab = min([x for x in excel_weights if x >= final_wt], default=max(excel_weights))

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(f"🏷️ Network: **{service}** | Zone: **{zone}**")
            st.write(f"⚖️ Base Weight: **{base_weight} KG**")
            if vol_wt > 0:
                st.write(f"📏 Volumetric Weight: **{round(vol_wt, 2)} KG**")
            st.markdown(f"<h3 style='color:#075E54; margin-top:10px;'>✅ Final Applied Weight: {applied_slab} KG</h3>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # 4. Price Retrieval
            target_col = f"{zone}-{service}"
            if target_col in clean_rates.columns:
                try:
                    final_price = clean_rates.loc[clean_rates['Weight'] == applied_slab, target_col].values[0]

                    # --- PRICE DISPLAY ---
                    st.markdown(f"""
                    <div class="price-card">
                        <p style="margin:0; opacity:0.8; letter-spacing:1px;">ESTIMATED SHIPPING COST</p>
                        <div class="price-value">₹{final_price}</div>
                        <p style="margin:0; font-size:14px; opacity:0.6;">Weight Slab: {applied_slab} KG</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Volumetric Warning
                    if vol_wt > base_weight:
                        st.warning(f"⚠️ గమనిక: పార్సెల్ సైజు (Volumetric) ఎక్కువగా ఉండటం వల్ల {applied_slab} KG రేటు వర్తిస్తుంది.")

                    # --- SUPPORT & WHATSAPP ---
                    st.markdown("""
                        <div class="info-box" style="margin-top:15px;">
                            📞 <b>Customer Support:</b> Sai (8885999794)<br>
                            ఏవైనా డౌట్స్ ఉంటే పైన ఉన్న నంబర్ కి సంప్రదించండి.
                        </div>
                    """, unsafe_allow_html=True)

                    # WhatsApp Link
                    wa_phone = "918885999794"
                    wa_text = f"Hello Sai Garu,\nI checked shipping in Vayu Vega App.\n\n📍 Pincode: {selected_pin}\n🚚 Network: {service}\n⚖️ Weight: {applied_slab} KG\n💰 Price: ₹{final_price}\n\nPlease confirm."
                    encoded_wa = urllib.parse.quote(wa_text)
                    
                    st.markdown(f"""
                    <a href="https://wa.me/{wa_phone}?text={encoded_wa}" target="_blank" style="text-decoration:none;">
                        <button style="width:100%; background:#25D366; color:white; padding:18px; border:none; border-radius:15px; font-size:18px; font-weight:bold; cursor:pointer; margin-top:15px; transition:0.3s;">
                            📲 Share Booking on WhatsApp
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                except:
                    st.error("Rate Chart లో ఈ వెయిట్ స్లాబ్ కి ధర లేదు.")
            else:
                st.error(f"Excel Error: '{target_col}' కాలమ్ దొరకలేదు.")
else:
    st.warning("⚠️ 'rates.xlsx' ఫైల్ లోడ్ అవ్వలేదు. దయచేసి ఫైల్ నేమ్ సరిచూసుకోండి.")

st.markdown("<br><p style='text-align:center; font-size:12px; color:#999;'>© 2026 Vayu Vega Logistics Automation | Gudiwada</p>", unsafe_allow_html=True)
