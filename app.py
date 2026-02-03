import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import av
import time

# 1. CONFIGURAÇÃO DE TELA E PERMISSÕES
st.set_page_config(page_title="Souza Cam", layout="wide", initial_sidebar_state="collapsed")

# CSS para Interface iPhone com Filtros embaixo
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #000; }
    
    /* Visor da Câmera */
    .video-container {
        position: fixed; top: 80px; width: 100%; height: 60vh;
        z-index: 1; border-radius: 20px; overflow: hidden;
    }

    /* Interface Superior */
    .ios-header {
        position: fixed; top: 0; width: 100%; height: 80px;
        background: #000; display: flex; justify-content: space-around;
        align-items: center; color: white; z-index: 10;
    }

    /* Interface Inferior (Fundo Preto) */
    .ios-bottom {
        position: fixed; bottom: 0; width: 100%; height: 280px;
        background: #000; z-index: 10; display: flex; flex-direction: column;
        align-items: center;
    }

    /* Botão de Disparo */
    .shutter-btn {
        width: 75px; height: 75px; border-radius: 50%;
        border: 5px solid white; background: transparent;
        display: flex; align-items: center; justify-content: center;
        margin-top: 20px;
    }
    .shutter-inner { width: 60px; height: 60px; background: white; border-radius: 50%; }

    /* Indicador de Live Photo */
    .live-icon { color: #FFCC00; font-weight: bold; font-size: 12px; }
    </style>
    
    <div class="ios-header">
        <span>⚡</span> <span class="live-icon">🟡 LIVE</span> <span>HDR</span>
    </div>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE FILTROS (BOTÕES QUE SIMULAM O SWIPE)
if 'filtro_atual' not in st.session_state:
    st.session_state.filtro_atual = "PADRÃO"

# Barra de Modos/Filtros (Em cima do botão de disparo)
cols = st.columns([1,1,1,1])
with st.container():
    st.markdown('<div style="height: 150px;"></div>', unsafe_allow_html=True) # Espaçador
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("VÍVIDO"): st.session_state.filtro_atual = "VÍVIDO"
    if c2.button("DRAMÁTICO"): st.session_state.filtro_atual = "DRAMÁTICO"
    if c3.button("FRIO"): st.session_state.filtro_atual = "FRIO"
    if c4.button("P&B"): st.session_state.filtro_atual = "P&B"

# 3. MOTOR DE IMAGEM COM FILTROS IPHONE
def callback(frame):
    img = frame.to_ndarray(format="bgr24")
    f = st.session_state.filtro_atual
    
    # Efeito de Nitidez (Base)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)

    if f == "VÍVIDO":
        img = cv2.convertScaleAbs(img, alpha=1.2, beta=10)
    elif f == "DRAMÁTICO":
        img = cv2.convertScaleAbs(img, alpha=1.4, beta=-20)
    elif f == "FRIO":
        img[:, :, 0] = cv2.add(img[:, :, 0], 30)
    elif f == "P&B":
        img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
        
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# 4. O VISOR (Aqui resolve a permissão)
webrtc_streamer(
    key="souza-pro-final",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=callback,
    media_stream_constraints={
        "video": {"facingMode": "environment"}, # Força câmera traseira
        "audio": False
    },
    async_processing=True,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# 5. BOTÃO DE DISPARO (LIVE PHOTO)
if st.button("CAPTAR"):
    st.balloons()
    st.toast("🟡 LIVE PHOTO CAPTURADA!")
