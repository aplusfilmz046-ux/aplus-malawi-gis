import streamlit as st
import sqlite3
import math
import folium
from streamlit_folium import st_folium
from transaction_logger import log_system_event

# 🎨 SECTION 1: GLOBAL BRAND CONFIGURATION & MOBILE APPS STYLING
st.set_page_config(
    page_title="A+Malawi GIS Addressing Platform", 
    page_icon="🇲🇼", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# We define the complete layout CSS as a single flat string variable right here
mobile_css = """<style>
[data-testid="stAppViewContainer"] .main .block-container { padding: 0rem !important; max-width: 100% !important; }
[data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
h1, h2, h3, h4, p, div { font-family: 'Inter', sans-serif !important; }
.m-nav { background-color: #111111; padding: 1.1rem 1.5rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #ce1126; position: sticky; top: 0; z-index: 9999; }
.m-logo-group { display: flex; align-items: center; gap: 0.6rem; }
.m-logo-sphere { background: radial-gradient(circle, #ce1126 0%, #111111 100%); width: 36px; height: 36px; border-radius: 50%; border: 2px solid #008751; }
.m-logo-text { color: white; font-size: 1.3rem; font-weight: 800; margin: 0; }
.m-logo-text span { color: #ce1126; }
.m-nav-action-btn { background-color: #008751; color: white !important; padding: 0.45rem 1.2rem; border-radius: 20px; font-weight: 600; text-decoration: none !important; font-size: 0.75rem; }
.m-hero-container { background: linear-gradient(160deg, #070f0b 0%, #131c17 100%); padding: 3.5rem 1.5rem; text-align: center; color: white; border-bottom: 6px solid #008751; }
.m-tagline-pill { background-color: rgba(206, 17, 38, 0.15); color: #ff4d5a; padding: 0.35rem 1.1rem; border-radius: 30px; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; display: inline-block; margin-bottom: 1.25rem; }
.m-hero-container h2 { font-size: 2.6rem !important; font-weight: 900 !important; line-height: 1.15 !important; margin: 0 0 1rem 0 !important; color: white !important; }
.m-hero-container p { font-size: 0.95rem; color: #cccccc; line-height: 1.5; margin-bottom: 2.5rem; }
.embedded-graphic-card { background-color: #1a1a1a; padding: 0.5rem; border-radius: 16px; box-shadow: 0 12px 35px rgba(0,0,0,0.4); margin-bottom: 2rem; border: 1px solid #2d2d2d; }
.embedded-graphic-card img { border-radius: 12px; width: 100%; height: auto; display: block; }
.m-sectors-wrapper { padding: 3.5rem 1.5rem; background-color: white; text-align: center; }
.m-sectors-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem; }
.m-sector-card { background-color: #ffffff; padding: 1.75rem 0.75rem; border-radius: 14px; border: 1px solid #eaeaea; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
.m-sector-icon-sphere { font-size: 1.6rem; width: 48px; height: 45px; background-color: #f1f8e9; color: #008751; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 0.85rem auto; }
.m-sector-card h4 { font-size: 1rem !important; font-weight: 700 !important; color: #111111 !important; margin: 0 0 0.35rem 0 !important; }
.m-sector-card p { font-size: 0.75rem !important; color: #666666 !important; margin: 0 !important; line-height: 1.3 !important; }
.m-marketing-promo { padding: 3rem 1.5rem; background-color: #ffffff; }
.m-marketing-promo h3 { font-size: 1.75rem !important; font-weight: 800 !important; color: #111111 !important; margin-bottom: 0.85rem !important; }
.m-marketing-promo p { font-size: 0.95rem; color: #555555; line-height: 1.55; }
.m-pipeline-wrapper { padding: 3.5rem 1.5rem; background-color: #f9fbf9; border-top: 1px solid #eaeaea; border-bottom: 1px solid #eaeaea; }
.m-pipeline-wrapper h3 { font-size: 1.75rem !important; font-weight: 800 !important; text-align: center; margin-bottom: 2rem !important; }
.m-pipeline-flow-step { background-color: #ffffff; padding: 1.35rem; border-radius: 14px; border: 1px solid #eef2ee; margin-bottom: 1rem; display: flex; gap: 1rem; align-items: flex-start; box-shadow: 0 3px 10px rgba(0,135,81,0.01); }
.m-pipeline-badge { background-color: #008751; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: 700; flex-shrink: 0; font-size: 0.85rem; }
.m-pipeline-flow-step h4 { font-size: 1.1rem !important; font-weight: 700 !important; color: #111111 !important; margin: 0 0 0.25rem 0 !important; }
.m-pipeline-flow-step p { font-size: 0.85rem !important; color: #555555 !important; line-height: 1.4 !important; margin: 0 !important; }
.m-workspace { padding: 3.5rem 1.5rem; background-color: #f4f7f5; }
.m-w-title { font-size: 1.5rem !important; font-weight: 800 !important; text-align: center; margin-bottom: 1.75rem !important; }
div.stButton > button { background: #ce1126 !important; color: white !important; border: none !important; width: 100% !important; padding: 0.8rem !important; font-weight: 700 !important; border-radius: 25px !important; box-shadow: 0 4px 10px rgba(206,17,38,0.15) !important; }
.m-footer { background-color: #111111; padding: 3.5rem 1.5rem; color: #aaaaaa; text-align: center; border-top: 4px solid #ce1126; }
.m-footer h4 { color: white !important; font-size: 1.3rem !important; font-weight: 800 !important; margin-bottom: 0.6rem !important; }
.m-footer p { font-size: 0.85rem; line-height: 1.45; }
.m-footer-bottom-bar { border-top: 1px solid #222222; margin-top: 2rem; padding-top: 1.25rem; font-size: 0.7rem; }
</style>"""
st.markdown(mobile_css, unsafe_allow_html=True)

# --- SECTION 2: RENDER BRAND PHONE NAVIGATION HEADER ---
st.markdown('<div class="m-nav"><div class="m-logo-group"><div class="m-logo-sphere"></div><div class="m-logo-text">A+<span>Malawi</span></div></div><a class="m-nav-action-btn" href="#register-section">Register Now</a></div>', unsafe_allow_html=True)

# --- SECTION 3: RENDER THE HERO BLOCK AND VECTOR LAYOUT GRAPHICS ---
st.markdown('<div class="m-hero-container"><div class="m-tagline-pill">🇲🇼 MALAWI\'S DIGITAL ADDRESS SYSTEM</div><h2>Your Place.<br/><span style="color: #ce1126;">Your Address.</span><br/><span style="color: #008751;">Your Identity.</span></h2><p>A+Malawi GIS Addressing Platform helps you register your home, business, farm or institution on a map — so you can be found, served and connected, anywhere in Malawi.</p>', unsafe_allow_html=True)

# Injecting the embedded digital image graphics natively via compact text variables
flag_map_svg = '<div class="embedded-graphic-card"><img src="data:image/svg+xml;utf8,<svg xmlns=\'http://w3.org\' width=\'340\' height=\'240\' viewBox=\'0 0 340 240\' style=\'background:%230c140f;\'><path d=\'M130 30 L160 50 L180 90 L160 140 L190 190 L150 220 L130 180 L140 130 L110 90 Z\' fill=\'%23ce1126\' stroke=\'%23008751\' stroke-width=\'3\'/><rect x=\'20\' y=\'80\' width=\'80\' height=\'15\' fill=\'black\'/><rect x=\'20\' y=\'95\' width=\'80\' height=\'15\' fill=\'%23ce1126\'/><rect x=\'20\' y=\'110\' width=\'80\' height=\'15\' fill=\'%23008751\'/><text x=\'200\' y=\'100\' font-family=\'sans-serif\' font-size=\'16\' font-weight=\'900\' fill=\'white\'>One Map</text><text x=\'200\' y=\'125\' font-family=\'sans-serif\' font-size=\'16\' font-weight=\'900\' fill=\'%23ce1126\'>One Malawi</text><text x=\'200\' y=\'150\' font-family=\'sans-serif\' font-size=\'16\' font-weight=\'900\' fill=\'%23008751\'>One Address</text></svg>"/></div>'
hero_phone_svg = '<div class="embedded-graphic-card"><img src="data:image/svg+xml;utf8,<svg xmlns=\'http://w3.org\' width=\'340\' height=\'440\' viewBox=\'0 0 340 480\' style=\'background:%23111;\'><rect x=\'30\' y=\'20\' width=\'280\' height=\'440\' rx=\'32\' fill=\'%23222\' stroke=\'%23333\' stroke-width=\'4\'/><rect x=\'45\' y=\'35\' width=\'250\' height=\'410\' rx=\'20\' fill=\'%23e3f2fd\'/><circle cx=\'170\' cy=\'200\' r=\'12\' fill=\'%23ce1126\' stroke=\'white\' stroke-width=\'3\'/><path d=\'M170 200 L170 240\' stroke=\'%23ce1126\' stroke-width=\'4\'/><rect x=\'60\' y=\'320\' width=\'220\' height=\'90\' rx=\'12\' fill=\'white\' style=\'filter:drop-shadow(0 4px 8px rgba(0,0,0,0.15));\'/><text x=\'75\' y=\'345\' font-family=\'sans-serif\' font-size=\'11\' font-weight=\'bold\' fill=\'%23666\' text-transform=\'uppercase\'>A+ MALAWI ADDRESS</text><text x=\'75\' y=\'370\' font-family=\'sans-serif\' font-size=\'16\' font-weight=\'900\' fill=\'%23111\'>Chilumba, Nkhata Bay</text><text x=\'75\' y=\'395\' font-family=\'sans-serif\' font-size=\'12\' font-weight=\'bold\' fill=\'%23008751\'>📍 -11.5833, 34.2833</text></svg>"/></div>'

st.markdown(flag_map_svg, unsafe_allow_html=True)
st.markdown(hero_phone_svg, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True) # Close hero container

# --- SECTION 4: RENDER THE RESPONSIVE SECTORS GRID ---
sectors_grid_html = '<div class="m-sectors-wrapper"><small style="color: #008751; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">Sectors We Serve</small><div class="m-sectors-grid"><div class="m-sector-card"><div class="m-sector-icon-sphere">🏠</div><h4>Homes</h4><p>Your family, safer, more connected</p></div><div class="m-sector-card"><div class="m-sector-icon-sphere">🏢</div><h4>Businesses</h4><p>Grow your business with a real address</p></div><div class="m-sector-card"><div class="m-sector-icon-sphere">🌾</div><h4>Farms</h4><p>Access support, markets & services</p></div><div class="m-sector-card"><div class="m-sector-icon-sphere">🎓</div><h4>Schools</h4><p>Better planning & service delivery</p></div><div class="m-sector-card"><div class="m-sector-icon-sphere">⛪</div><h4>Churches</h4><p>Reach your community more easily</p></div><div class="m-sector-card"><div class="m-sector-icon-sphere">🏥</div><h4>Clinics</h4><p>Faster help, better care</p></div></div></div>'
st.markdown(sectors_grid_html, unsafe_allow_html=True)

# --- SECTION 5: RENDER USER ENGAGEMENT WOMAN GRAPHIC ---
