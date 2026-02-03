import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import av

# 1. SETUP E TELA SEMPRE LIGADA (JavaScript)
st.set_page_config(page_title="Souza Cam Pro", layout="wide", initial_sidebar_state="collapsed")

# Script para manter a tela do celular ligada (Wake Lock API)
st.components.v1.html("""
    <script>
    async function keepScreenOn() {
        try {
            const wakeLock = await navigator.wakeLock.request('screen');
            console.log('Tela Bloqueada: Sempre Ligada');
        } catch (err) {
            console.log('Erro no WakeLock: ' + err.message);
        }
    }
    keepScreenOn();
    </script>
""", height=0)

# 2. CSS DA INTERFACE IPHONE (Igual ao que você pediu)
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #000; }
    
    .ios-header {
        position: fixed; top: 0; width: 100%; height: 60px;
        display: flex; justify-content: space-around; align-items: center;
        color: white; z-index: 100; background: black;
    }

    video {
        width: 100% !important;
        height: 65vh !important;
        object-fit: cover !important;
        margin-top: 60px;
    }

    .ios-footer {
        position: fixed; bottom: 0; width: 100%; height: 240px;
        background: black; z-index: 90;
    }

    .zoom-bar {
        position: fixed; bottom: 190px; width: 100%;
        display: flex; justify-content: center; gap: 10px; z-index: 100;
    }
    .z-unit {
        background: rgba(30,30,30,0.9); border-radius: 50%; width: 35px; height: 35px;
        display: flex; align-items: center; justify-content: center;
        font-size: 11px; color: white; border: 1px solid #333;
    }
    .z-active { border: 1px solid #FFCC00; color: #FFCC00; }

    div.stButton > button {
        border-radius: 50% !important;
        width: 80px !important; height: 80px !important;
        border: 5px solid white !important;
        background: transparent !important;
        position: fixed !important; bottom: 35px !important;
        left: 50% !important; transform: translateX(-50%) !important;
        z-index: 100 !important;
    }
    div.stButton > button::after {
        content: ""; display: block; width: 62px; height: 62px;
        background: white; border-radius: 50%; margin: auto;
    }
    </style>
    
    <div class="ios-header">
        <span>⚡</span> <span style="color:#FFCC00">🟡 LIVE</span> <span>HDR</span>
    </div>

    <div class="zoom-bar">
        <div class="z-unit">0.6</div>
        <div class="z-unit z-active">1x</div>
        <div class="z-unit">2</div>
    </div>

    <div class="ios-footer">
        <div style="display:flex; justify-content:center; gap:20px; margin-top:15px; color:white; font-weight:bold; font-size:13px;">
            <span style="opacity:0.5">VÍDEO</span> <span style="color:#FFCC00">FOTO</span> <span style="opacity:0.5">RETRATO</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 3. FILTRO IPHONE (Dramático Frio + Nitidez)
def engine_pro(frame):
    img = frame.to_ndarray(format="bgr24")
    # Sharpening
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)
    # Filtro Frio
    img = cv2.convertScaleAbs(img, alpha=1.2, beta=-5)
    img[:, :, 0] = cv2.add(img[:, :, 0], 20)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# 4. VISOR (Configuração para abrir direto)
webrtc_streamer(
    key="iphone-screen-on",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=engine_pro,
    media_stream_constraints={
        "video": {"facingMode": "environment"},
        "audio": False
    },
    async_processing=True,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

if st.button(" "):
    st.toast("📸 Capturado!")
