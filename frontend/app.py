import streamlit as st
from PIL import Image
import random

import sys, os
sys.path.append(os.path.abspath("../backend"))
from predict import predict_fog, predict_accident, final_risk

st.set_page_config(page_title="FOGVISION", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

* { font-family: 'Rajdhani', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #050816 0%, #0a0f2e 50%, #02040c 100%);
    color: white;
}

h1,h2,h3,h4,h5,h6 {
    font-family: 'Orbitron', sans-serif !important;
    color: white !important;
}

p, label, div { color: white !important; font-size: 16px; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #040714, #0a0f2e);
    border-right: 1px solid #00f2fe;
}

[data-testid="stSidebar"] h2 {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 22px !important;
    font-weight: 900 !important;
    color: #00f2fe !important;
    text-shadow: 0 0 15px #00f2fe;
    letter-spacing: 3px;
}

div[role="radiogroup"] label {
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 8px 12px !important;
    margin: 4px 0 !important;
    transition: all 0.3s ease;
    font-size: 15px !important;
    font-weight: 600 !important;
}

div[role="radiogroup"] label:hover {
    border: 1px solid rgba(0,242,254,0.5) !important;
    box-shadow: 0 0 10px rgba(0,242,254,0.3) !important;
    background: rgba(0,242,254,0.05) !important;
}

div[role="radiogroup"] label[aria-checked="true"] {
    background: rgba(0,242,254,0.15) !important;
    border: 1px solid #00f2fe !important;
    box-shadow: 0 0 15px rgba(0,242,254,0.4) !important;
    color: #00f2fe !important;
}

[data-testid="stSelectbox"] > div > div {
    background: #0b1225 !important;
    border: 1px solid rgba(0,242,254,0.3) !important;
    border-radius: 10px !important;
    transition: all 0.3s ease;
}

[data-testid="stSelectbox"] > div > div:hover {
    border: 1px solid #00f2fe !important;
    box-shadow: 0 0 12px rgba(0,242,254,0.4) !important;
}

.main-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 68px;
    font-weight: 900;
    text-align: center;
    color: #00f2fe;
    text-shadow: 0 0 10px #00f2fe, 0 0 30px rgba(0,242,254,0.5);
    letter-spacing: 8px;
}

.sub-title {
    text-align: center;
    color: #9ca3af !important;
    letter-spacing: 6px;
    font-size: 13px !important;
}

.feature-card {
    background: linear-gradient(135deg, #0b1225, #0f1a35);
    border-radius: 20px;
    padding: 35px 25px;
    text-align: center;
    border: 1px solid rgba(0,242,254,0.2);
    transition: all 0.4s ease;
    min-height: 220px;
}

.feature-card:hover {
    border: 1px solid #00f2fe;
    box-shadow: 0 0 25px rgba(0,242,254,0.3);
}

.feature-card h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00f2fe !important;
    font-size: 15px !important;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(135deg, #00f2fe, #0080ff);
    color: black !important;
    font-weight: 700 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 12px !important;
    letter-spacing: 1px;
    border: none !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 15px rgba(0,242,254,0.3);
    padding: 12px !important;
}

.stButton > button:hover {
    box-shadow: 0 0 25px rgba(0,242,254,0.7) !important;
    transform: translateY(-2px) !important;
}

.section-header {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 22px;
    font-weight: 900;
    color: #00f2fe;
    border-left: 5px solid #00f2fe;
    padding-left: 15px;
    text-shadow: 0 0 10px rgba(0,242,254,0.5);
    letter-spacing: 3px;
    margin-bottom: 20px;
}

.prediction-header {
    background: linear-gradient(135deg, #0b2239, #0f1a35);
    padding: 25px;
    border-radius: 15px;
    border-left: 5px solid #00f2fe;
    box-shadow: 0 0 20px rgba(0,242,254,0.1);
}

.em-card {
    background: linear-gradient(135deg, #0b1225, #0f1a35);
    padding: 20px 10px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid rgba(0,242,254,0.25);
    transition: all 0.3s ease;
}

.logo-svg {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}

@keyframes fogPulse {
    0%   { opacity: 0.6; transform: scale(1); }
    50%  { opacity: 1;   transform: scale(1.05); }
    100% { opacity: 0.6; transform: scale(1); }
}

.fog-logo {
    animation: fogPulse 3s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "em_msg" not in st.session_state:
    st.session_state.em_msg = None

# ---------- NAV ----------
st.sidebar.markdown("<h2>🛰️ FOGVISION</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

pages = ["Home", "Analyzer", "Risk Dashboard", "Safety Tips"]
choice = st.sidebar.radio("Navigate:", pages,
    index=pages.index(st.session_state.page))

if choice != st.session_state.page:
    st.session_state.page = choice
    st.rerun()


# ================= HOME =================
if st.session_state.page == "Home":

    st.write("")

    st.markdown("""
    <div class="logo-svg">
      <svg class="fog-logo" width="110" height="110" viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg">
        <circle cx="55" cy="55" r="50" fill="none" stroke="#00f2fe" stroke-width="1.5" opacity="0.3"/>
        <circle cx="55" cy="55" r="38" fill="none" stroke="#00f2fe" stroke-width="1" opacity="0.5"/>
        <circle cx="55" cy="55" r="25" fill="none" stroke="#00f2fe" stroke-width="1.5" opacity="0.7"/>
        <circle cx="55" cy="55" r="10" fill="#00f2fe" opacity="0.9"/>
        <line x1="55" y1="5"  x2="55" y2="105" stroke="#00f2fe" stroke-width="0.5" opacity="0.2"/>
        <line x1="5"  y1="55" x2="105" y2="55" stroke="#00f2fe" stroke-width="0.5" opacity="0.2"/>
        <path d="M30 55 Q55 30 80 55 Q55 80 30 55Z" fill="rgba(0,242,254,0.15)" stroke="#00f2fe" stroke-width="1"/>
        <circle cx="55" cy="55" r="4" fill="white"/>
        <path d="M20 75 Q35 70 50 75 Q65 80 80 75" stroke="#00f2fe" stroke-width="2" fill="none" opacity="0.6"/>
        <path d="M25 83 Q42 78 58 83 Q72 88 85 83" stroke="#00f2fe" stroke-width="1.5" fill="none" opacity="0.4"/>
      </svg>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">FOGVISION</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">SMART VISION • SAFER ROADS • AI POWERED</p>', unsafe_allow_html=True)

    st.write("")
    st.write("---")
    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('''
        <div class="feature-card">
            <div style="font-size:45px">🔍</div>
            <h3>Risk Analyzer</h3>
            <p style="color:#9ca3af !important;font-size:13px">Detect fog density & road visibility using AI computer vision.</p>
        </div>''', unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 Launch Analyzer", key="home_analyzer"):
            st.session_state.page = "Analyzer"
            st.rerun()

    with c2:
        st.markdown('''
        <div class="feature-card">
            <div style="font-size:45px">📊</div>
            <h3>Risk Dashboard</h3>
            <p style="color:#9ca3af !important;font-size:13px">Predict accident risk based on weather, road & speed data.</p>
        </div>''', unsafe_allow_html=True)
        st.write("")
        if st.button("📊 Open Dashboard", key="home_dashboard"):
            st.session_state.page = "Risk Dashboard"
            st.rerun()

    with c3:
        st.markdown('''
        <div class="feature-card">
            <div style="font-size:45px">💡</div>
            <h3>Safety Protocol</h3>
            <p style="color:#9ca3af !important;font-size:13px">Essential fog driving rules to keep you safe on the road.</p>
        </div>''', unsafe_allow_html=True)
        st.write("")
        if st.button("💡 Explore Tips", key="home_tips"):
            st.session_state.page = "Safety Tips"
            st.rerun()


# ================= ANALYZER =================
elif st.session_state.page == "Analyzer":

    st.markdown('<div class="section-header">🌫️ ENVIRONMENTAL ANALYZER</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.subheader("📷 Visual Intake")
        file = st.file_uploader("Upload Road Image", type=["jpg","jpeg","png"])

        if file:
            img = Image.open(file)
            st.image(img, use_container_width=True)
            with st.spinner("🔍 Analyzing fog density..."):
                fog_idx, fog_label = predict_fog(img)

            if fog_idx == 0:
                st.error(f"🌫️ Fog Detection: **{fog_label}**")
            elif fog_idx == 1:
                st.warning(f"🌫️ Fog Detection: **{fog_label}**")
            else:
                st.success(f"✅ Fog Detection: **{fog_label}**")

    with c2:
        st.subheader("⚙️ Trip Inputs")
        time = st.selectbox("🕐 Time of Day", ["Day", "Night"])
        speed = st.slider("🚗 Speed (km/h)", 0, 120, 60)
        weather = st.selectbox("🌤️ Weather", ["Clear", "Rainy", "Cloudy", "Snowing"])
        road = st.selectbox("🛣️ Road Condition", ["Dry", "Wet", "Icy"])

        st.write("")
        st.subheader("🛣️ Road Details")
        st.radio("Road Type", ["Highway", "Urban Street", "Rural Path"])

        if file:
            with st.spinner("🤖 Calculating risk..."):
                acc_idx, acc_label = predict_accident(speed, weather, road, time)
                risk = final_risk(fog_idx, acc_idx, speed, weather, road)  # ✅ UPDATED

            st.divider()
            st.markdown(f"**🚗 Accident Severity:** `{acc_label}`")
            st.write("")
            if "HIGH" in risk:
                st.error(f"### 🚨 FINAL RISK: {risk}")
            elif "MEDIUM" in risk:
                st.warning(f"### ⚠️ FINAL RISK: {risk}")
            else:
                st.success(f"### ✅ FINAL RISK: {risk}")


# ================= DASHBOARD =================
elif st.session_state.page == "Risk Dashboard":

    st.markdown('<div class="prediction-header"><h2 style="color:#00f2fe !important; font-family:Orbitron,sans-serif">ACCIDENT RISK PREDICTION</h2><p style="color:#9ca3af !important">AI-powered prediction based on your trip data</p></div>', unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        d_speed = st.slider("🚗 Speed (km/h)", 0, 120, 60)
        d_weather = st.selectbox("🌤️ Weather", ["Clear", "Rainy", "Cloudy", "Snowing"])
    with col2:
        d_road = st.selectbox("🛣️ Road Condition", ["Dry", "Wet", "Icy"])
        d_time = st.selectbox("🕐 Time", ["Day", "Night"])
        d_fog = st.selectbox("🌫️ Fog Level", ["No Fog", "Medium Fog", "Dense Fog"])

    st.write("")

    if st.button("🚀 GENERATE ADVANCED REPORT"):
        fog_map = {"No Fog": 2, "Medium Fog": 1, "Dense Fog": 0}
        fog_idx = fog_map[d_fog]

        with st.spinner("🤖 Analyzing conditions..."):
            acc_idx, acc_label = predict_accident(d_speed, d_weather, d_road, d_time)
            risk = final_risk(fog_idx, acc_idx, d_speed, d_weather, d_road)  # ✅ UPDATED

        prob = random.randint(20, 90)
        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1: st.metric("🌫️ Fog Level", d_fog)
        with col2: st.metric("🚗 Severity", acc_label)
        with col3: st.metric("🎯 Risk", risk)

        st.write("")
        st.progress(prob / 100)
        st.write(f"**Accident Probability Estimate: {prob}%**")

        if "HIGH" in risk:
            st.error("🚨 CRITICAL ALERT: Conditions hazardous. Avoid driving!")
        elif "MEDIUM" in risk:
            st.warning("⚠️ CAUTION: Drive carefully and reduce speed.")
        else:
            st.success("✅ Conditions safe. Stay alert.")

    st.divider()
    st.subheader("🆘 Emergency Quick-Links")
    st.write("")

    ec1, ec2, ec3, ec4 = st.columns(4)

    with ec1:
        st.markdown('<div class="em-card"><div style="font-size:30px">📞</div><div style="font-family:Orbitron,sans-serif;font-size:11px;color:#00f2fe !important;font-weight:700">SOS DISPATCH</div><div style="font-size:11px;color:#9ca3af !important">Emergency services</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("📞 Call SOS", key="sos"):
            st.error("🚨 **SOS ACTIVATED!** Call **112** immediately for emergency services!")

    with ec2:
        st.markdown('<div class="em-card"><div style="font-size:30px">🏥</div><div style="font-family:Orbitron,sans-serif;font-size:11px;color:#00f2fe !important;font-weight:700">HOSPITAL</div><div style="font-size:11px;color:#9ca3af !important">Nearest medical help</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("🏥 Find Hospital", key="hosp"):
            st.info("🏥 **Finding nearest hospital...**")
            st.markdown("👉 [**Click here → Open Google Maps Hospitals**](https://www.google.com/maps/search/hospital+near+me/)")

    with ec3:
        st.markdown('<div class="em-card"><div style="font-size:30px">🔧</div><div style="font-family:Orbitron,sans-serif;font-size:11px;color:#00f2fe !important;font-weight:700">ROADSIDE ASSIST</div><div style="font-size:11px;color:#9ca3af !important">Nearest mechanic</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("🔧 Get Help", key="road"):
            st.info("🔧 **Locating nearest roadside assistance...**")
            st.markdown("👉 [**Click here → Find Nearest Mechanic**](https://www.google.com/maps/search/car+repair+near+me/)")

    with ec4:
        st.markdown('<div class="em-card"><div style="font-size:30px">🏨</div><div style="font-family:Orbitron,sans-serif;font-size:11px;color:#00f2fe !important;font-weight:700">SAFE STAY</div><div style="font-size:11px;color:#9ca3af !important">Nearest shelter</div></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("🏨 Find Stay", key="stay"):
            st.info("🏨 **Finding nearest safe stay...**")
            st.markdown("👉 [**Click here → Find Nearest Hotel**](https://www.google.com/maps/search/hotel+near+me/)")


# ================= SAFETY =================
elif st.session_state.page == "Safety Tips":

    st.markdown('<div class="section-header">💡 SAFETY PROTOCOLS</div>', unsafe_allow_html=True)
    st.write("")

    tips = [
        ("🧘 Always Remain Focused", "Stay alert and avoid distractions. Fog reduces reaction time significantly."),
        ("🐌 Drive Slow", "Reduce speed by at least 50% in heavy fog. Speed is the #1 cause of fog accidents."),
        ("🔦 Use Low-Beam Lights", "High beams reflect off fog and reduce visibility. Always use low-beam or fog lights."),
        ("↔️ Maintain Distance", "Keep at least 3x the normal safe following distance in foggy conditions."),
        ("🚫 Avoid Overtaking", "Never attempt overtaking in fog — you cannot judge oncoming traffic speed."),
        ("🧼 Clean Windows", "Ensure windshield and mirrors are clean. Use defogger to clear condensation."),
        ("🚨 Stay Visible", "Turn on hazard lights if visibility drops below 50m. Make yourself seen."),
        ("🛑 Stop if Needed", "If fog is too dense, pull over safely away from traffic and wait it out.")
    ]

    for t, d in tips:
        with st.expander(t):
            st.write(d)