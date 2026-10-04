import streamlit as st
import sqlite3
import math
import folium
from streamlit_folium import st_folium
from transaction_logger import log_system_event

# Configure browser layout to support high-fidelity custom visual components
st.set_page_config(
    page_title="A+Malawi GIS Addressing Platform", 
    page_icon="🇲🇼", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 📋 PRODUCTION INTERFACE: STYLING & VIEWPORT STYLESHEETS ---
mobile_css = """<style>
[data-testid="stAppViewContainer"] .main .block-container { padding: 0rem !important; max-width: 100% !important; background-color: #f4f6f4; }
[data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
h1, h2, h3, h4, p, div, span { font-family: 'Inter', sans-serif !important; }

/* 📱 CORE NAVIGATION LAYER */
.m-nav-bar { background-color: #111111; padding: 1.1rem 1.5rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #ce1126; position: sticky; top: 0; z-index: 9999; }
.m-logo-group { display: flex; align-items: center; gap: 0.6rem; }
.m-logo-sphere { background: radial-gradient(circle, #ce1126 0%, #111111 100%); width: 36px; height: 36px; border-radius: 50%; border: 2px solid #008751; }
.m-logo-text { color: white; font-size: 1.3rem; font-weight: 800; margin: 0; }
.m-logo-text span { color: #ce1126; }
.m-action-badge { background-color: #008751; color: white !important; padding: 0.45rem 1.2rem; border-radius: 20px; font-weight: 600; text-decoration: none !important; font-size: 0.75rem; }

/* 🚀 PREMIUM HERO CANVASES */
.m-hero-stage { background: linear-gradient(160deg, #070f0b 0%, #131c17 100%); padding: 3.5rem 1.5rem; text-align: center; color: white; border-bottom: 6px solid #008751; }
.m-pill-tag { background-color: rgba(206, 17, 38, 0.15); color: #ff4d5a; padding: 0.35rem 1.1rem; border-radius: 30px; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; display: inline-block; margin-bottom: 1.25rem; border: 1px solid rgba(206, 17, 38, 0.3); }
.m-hero-stage h2 { font-size: 2.6rem !important; font-weight: 900 !important; line-height: 1.15 !important; margin: 0 0 1rem 0 !important; color: white !important; }
.m-hero-stage p { font-size: 0.95rem; color: #cccccc; line-height: 1.5; margin-bottom: 2.5rem; }

/* 🖼️ HIGH-FIDELITY VECTOR VECTOR CONTAINER CARDS */
.vector-card-wrapper { width: 100%; max-width: 420px; margin: 0 auto 1.5rem auto; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 1px solid rgba(0,0,0,0.05); background-color: #111; }
.vector-card-wrapper img { width: 100%; height: auto; display: block; }

/* 📱 SECTORS GRID LAYOUT MATRICES */
.m-sectors-grid-panel { padding: 3.5rem 1.5rem; background-color: white; text-align: center; }
.m-sectors-grid-panel h3 { font-size: 1.6rem !important; font-weight: 800 !important; margin-bottom: 1.5rem !important; color: #111111 !important; }

/* 📱 THREE STEPS FLOW PIPELINES */
.m-pipeline-panel { padding: 3.5rem 1.5rem; background-color: #ffffff; border-top: 1px solid #eaeaea; border-bottom: 1px solid #eaeaea; }
.m-pipeline-panel h3 { font-size: 1.75rem !important; font-weight: 800 !important; text-align: center; margin-bottom: 2rem !important; color: #111111 !important; }
.m-pipeline-card-step { background-color: #f9fbf9; padding: 1.35rem; border-radius: 14px; border: 1px solid #eef2ee; margin-bottom: 1rem; display: flex; gap: 1rem; align-items: flex-start; }
.m-pipeline-number-badge { background-color: #008751; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: 700; flex-shrink: 0; font-size: 0.85rem; }

/* 📱 GIS ENGINE FORM CORE WORKSPACE */
.m-workspace-wrapper { padding: 3.5rem 1.5rem; background-color: #f4f7f5; }
.m-workspace-title-header { font-size: 1.5rem !important; font-weight: 800 !important; text-align: center; margin-bottom: 1.75rem !important; color: #111111 !important; }
div.stButton > button { background: linear-gradient(to right, #ce1126, #b20e20) !important; color: white !important; border: none !important; width: 100% !important; padding: 0.85rem !important; font-weight: 700 !important; border-radius: 25px !important; box-shadow: 0 5px 15px rgba(206,17,38,0.3) !important; font-size: 1rem !important; }

/* 📱 BRAND REGIONAL FOOTER FOOTERS */
.m-app-footer { background-color: #111111; padding: 3.5rem 1.5rem; color: #aaaaaa; text-align: center; border-top: 4px solid #ce1126; }
</style>"""
st.markdown(mobile_css, unsafe_allow_html=True)

# ==========================================
# 📱 REFACTORED MODULE 1: COMPACT INTERACTIVE APP NAVBAR
# ==========================================
st.markdown('<div class="m-nav-bar"><div class="m-logo-group"><div class="m-logo-sphere"></div><div class="m-logo-text">A+<span>Malawi</span></div></div><a class="m-action-badge" href="#register-section">Register Address</a></div>', unsafe_allow_html=True)

# ==========================================
# 📱 REFACTORED MODULE 2: HERO STAGE BACKGROUND HEADER
# ==========================================
st.markdown('<div class="m-hero-stage"><div class="m-pill-tag">🇲🇼 MALAWI\'S DIGITAL ADDRESS SYSTEM</div><h2>Your Place.<br/><span style="color: #ce1126;">Your Address.</span><br/><span style="color: #008751;">Your Identity.</span></h2><p>A+Malawi GIS Addressing Platform helps you register your home, business, farm or institution on a map — so you can be found, served and connected, anywhere in Malawi.</p>', unsafe_allow_html=True)

# ==========================================
# 📱 REFACTORED MODULE 3: EXACT PREPACKAGED STRUCTURAL DESIGN GRAPHICS
# ==========================================
# Graphic Node A: "One Map, One Malawi" Flag Silhouette Overlay Map
flag_map_svg = '<div class="vector-card-wrapper"><img src="data:image/svg+xml;utf8,<svg xmlns=\'http://w3.org\' width=\'340\' height=\'240\' viewBox=\'0 0 340 240\' style=\'background:%230c140f;\'><path d=\'M130 30 L160 50 L180 90 L160 140 L190 190 L150 220 L130 180 L140 130 L110 90 Z\' fill=\'%23ce1126\' stroke=\'%23008751\' stroke-width=\'3\'/><rect x=\'20\' y=\'80\' width=\'80\' height=\'15\' fill=\'black\'/><rect x=\'20\' y=\'95\' width=\'80\' height=\'15\' fill=\'%23ce1126\'/><rect x=\'20\' y=\'110\' width=\'80\' height=\'15\' fill=\'%23008751\'/><text x=\'200\' y=\'100\' font-family=\'sans-serif\' font-size=\'16\' font-weight=\'900\' fill=\'white\'>One Map</text><text x=\'200\' y=\'125\' font-family=\'sans-serif\' font-size=\'16\' font-weight=\'900\' fill=\'%23ce1126\'>One Malawi</text><text x=\'200\' y=\'150\' font-family=\'sans-serif\' font-size=\'16\' font-weight=\'900\' fill=\'%23008751\'>One Address</text></svg>"/></div>'
st.markdown(flag_map_svg, unsafe_allow_html=True)

# Graphic Node B: Hand Holding Mockup Smartphone displaying the Live Active Address Pin
hero_phone_svg = '<div class="vector-card-wrapper"><img src="data:image/svg+xml;utf8,<svg xmlns=\'http://w3.org\' width=\'340\' height=\'440\' viewBox=\'0 0 340 480\' style=\'background:%23111;\'><rect x=\'30\' y=\'20\' width=\'280\' height=\'440\' rx=\'32\' fill=\'%23222\' stroke=\'%23333\' stroke-width=\'4\'/><rect x=\'45\' y=\'35\' width=\'250\' height=\'410\' rx=\'20\' fill=\'%23e3f2fd\'/><circle cx=\'170\' cy=\'200\' r=\'12\' fill=\'%23ce1126\' stroke=\'white\' stroke-width=\'3\'/><path d=\'M170 200 L170 240\' stroke=\'%23ce1126\' stroke-width=\'4\'/><rect x=\'60\' y=\'320\' width=\'220\' height=\'90\' rx=\'12\' fill=\'white\'/><text x=\'75\' y=\'345\' font-family=\'sans-serif\' font-size=\'11\' font-weight=\'bold\' fill=\'%23666\'>A+ MALAWI ADDRESS</text><text x=\'75\' y=\'370\' font-family=\'sans-serif\' font-size=\'16\' font-weight=\'900\' fill=\'%23111\'>Chilumba, Nkhata Bay</text><text x=\'75\' y=\'395\' font-family=\'sans-serif\' font-size=\'12\' font-weight=\'bold\' fill=\'%23008751\'>📍 -11.5833, 34.2833</text></svg>"/></div>'
st.markdown(hero_phone_svg, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True) # Close hero block canvas block safely

# ==========================================
# 📱 REFACTORED MODULE 4: SIX PURPOSE LAYOUT CARDS SECTORS (NATIVE PHONE SCALING)
# ==========================================
st.markdown('<div class="m-sectors-grid-panel"><h3>Addressed for Every Purpose</h3></div>', unsafe_allow_html=True)

sectors = [
    {"icon": "🏠", "title": "Homes", "desc": "Your family, safer, more connected"},
    {"icon": "🏢", "title": "Businesses", "desc": "Grow your business with a real address"},
    {"icon": "🌾", "title": "Farms", "desc": "Access support, markets & services"},
    {"icon": "🎓", "title": "Schools", "desc": "Better planning & service delivery"},
    {"icon": "⛪", "title": "Churches", "desc": "Reach your community more easily"},
    {"icon": "🏥", "title": "Clinics", "desc": "Faster help, better care"}
]

# Renders cleanly in stacked dual-card grids matching your blueprint parameters
for i in range(0, len(sectors), 2):
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown(f"<div style='font-size: 1.6rem; width: 46px; height: 46px; background-color: #f1f8e9; color: #008751; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 0.5rem auto;'>{sectors[i]['icon']}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align:center; font-weight:700;'>{sectors[i]['title']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; font-size:0.8rem; color:#666;'>{sectors[i]['desc']}</p>", unsafe_allow_html=True)
    with col2:
        with st.container(border=True):
            st.markdown(f"<div style='font-size: 1.6rem; width: 46px; height: 46px; background-color: #f1f8e9; color: #008751; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 0.5rem auto;'>{sectors[i+1]['icon']}</div>", unsafe_allow_html=True)
