import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import av

# Configurações de página para esconder menus do Streamlit
st.set_page_config(page_title="Camera iOS", layout="wide", initial_sidebar_state="collapsed")

# CSS para Clonar a Interface do iPhone
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #000; }
    
    /* Container do Visor da Câmera */
    .video-view {
        position: fixed; top: 10%; width: 100%; height: 65%;
        z-index: 1; display: flex; justify-content: center;
    }

    /* Interface Superior (Flash, Live, HDR) */
    .top-ui {
        position: fixed; top: 0; width: 100%; height: 80px;
        display: flex; justify-content: space-around; align-items: center;
        color: white; z-index: 10; font-family: sans-serif;
    }

    /* Seletor de Zoom (0.6, 1x, 2) */
    .zoom-ui {
        position: fixed; bottom: 26%; width: 100%;
        display: flex; justify-content: center; gap: 15px; z-index: 10;
    }
    .zoom-circle {
        background: rgba(0,0,0,0.5); border-radius: 50%; width: 35px; height: 35px;
        display: flex; align-items: center; justify-content: center;
        font-size: 11px; color: white; border: 1px solid rgba(255,255,255,0.2);
    }

    /* Modos de Câmera (FOTO em amarelo) */
    .modes-ui {
        position: fixed; bottom: 18%; width: 100%;
        display: flex; justify-content: center; gap: 20px;
        font-size: 13px; font-weight: bold; z-index: 10;
    }

    /* Botão de Disparo (Círculo Duplo) */
    div.stButton > button {
        border-radius: 50% !important;
        width: 80px !important; height: 80px !important;
        border: 4px solid white !important;
        background-color: transparent !important;
        position: fixed !important; bottom: 40px !important;
        left: 50% !important; transform: translateX(-50%) !important;
        z-index: 20 !important;
    }
    
    /* Ajuste para o componente de vídeo aparecer no meio */
    iframe { border-radius: 0px !important; }
    </style>
    
    <div class="top-ui">
        <span>⚡</span> <span style="color:#FFCC00">🟡 LIVE</span> <span>HDR</span>
    </div>
    
    <div class="zoom-ui">
        <div class="zoom-circle">0.6</div>
        <div class="zoom-circle" style="color:#FFCC00; border-color:#FFCC00">1x</div>
        <div class="zoom-circle">2</div>
    </div>

    <div class="modes-ui">
        <span style="opacity:0.5">VÍDEO</span>
        <span style="color:#FFCC00">FOTO</span>
        <span style="opacity:0.5">RETRATO</span>
    </div>
    """, unsafe_allow_html=True)

# Lógica de Filtros (Dramático Frio + Nitidez)
def engine_iphone(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # Filtro Dramático Frio (iOS Style)
    img = cv2.convertScaleAbs(img, alpha=1.2, beta=-10)
    img[:, :, 0] = cv2.add(img[:, :, 0], 25) # Realce Azul
    
    # Nitidez Pro
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)
    
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Componente de Câmera (O "START" que você viu vira o visor aqui)
webrtc_streamer(
    key="iphone-pro",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=engine_iphone,
    media_stream_constraints={"video": {"facingMode": "environment"}, "audio": False},
    async_processing=True,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Botão de Disparo (O botão invisível do Streamlit que ativa o design CSS)
if st.button(" "):
    st.toast("📸 Foto capturada!")
