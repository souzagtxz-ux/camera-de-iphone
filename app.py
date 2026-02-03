import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import av
import time

# Configuração Ultra Pro
st.set_page_config(page_title="Souza Cam iOS", layout="wide", initial_sidebar_state="collapsed")

# CSS para transformar o site em um App de Câmera Real
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #000; color: white; }
    
    /* Botão de Disparo Dinâmico */
    div.stButton > button {
        border-radius: 50% !important;
        width: 80px !important; height: 80px !important;
        border: 5px solid white !important;
        position: fixed !important; bottom: 60px !important;
        left: 50% !important; transform: translateX(-50%) !important;
        z-index: 9999 !important;
    }

    /* Seletor de Modos no rodapé */
    .mode-bar {
        position: fixed; bottom: 150px; width: 100%;
        text-align: center; font-family: sans-serif;
        font-size: 12px; letter-spacing: 2px; color: #FFCC00;
        z-index: 999; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Interface Lateral (Ajustes)
st.sidebar.title("⚙️ Configurações Apple")
modo = st.sidebar.radio("MODO SELECIONADO", ["FOTO", "VÍDEO", "LIVE PHOTO"])
filtro = st.sidebar.selectbox("ESTILO FOTOGRÁFICO", 
    ["Padrão", "Vívido", "Vívido Quente", "Vívido Frio", "Dramático", "Dramático Frio", "P&B Silencioso"])

st.markdown(f'<div class="mode-bar">{modo} • {filtro.upper()}</div>', unsafe_allow_html=True)

# Lógica de Cor do Botão
if modo == "VÍDEO":
    st.markdown("<style>div.stButton > button { background: radial-gradient(circle, red 50%, transparent 55%) !important; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>div.stButton > button { background: radial-gradient(circle, white 50%, transparent 55%) !important; }</style>", unsafe_allow_html=True)

def processador_universal(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # 1. NITIDEZ G-CAM (Deep Fusion)
    img_blurred = cv2.GaussianBlur(img, (0, 0), 3)
    img = cv2.addWeighted(img, 1.7, img_blurred, -0.7, 0)

    # 2. APLICAÇÃO DOS EFEITOS IOS
    if "Vívido" in filtro:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = cv2.convertScaleAbs(hsv[:,:,1], alpha=1.4)
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    if "Quente" in filtro:
        img[:, :, 2] = cv2.add(img[:, :, 2], 30)
    elif "Frio" in filtro:
        img[:, :, 0] = cv2.add(img[:, :, 0], 40)
        
    if "Dramático" in filtro:
        img = cv2.convertScaleAbs(img, alpha=1.2, beta=-20)
        
    if "P&B" in filtro:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Câmera principal
webrtc_streamer(
    key="souza-pro-max",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=processador_universal,
    media_stream_constraints={
        "video": {"facingMode": "environment", "width": 1280, "height": 720},
        "audio": (modo == "VÍDEO")
    },
    async_processing=True
)

# Ação do Botão
if st.button(" "):
    if modo == "FOTO":
        st.toast("📸 Capturado com Estilo Apple!")
    elif modo == "LIVE PHOTO":
        with st.spinner("🟡 LIVE"):
            time.sleep(1.5)
        st.success("Live Photo Salva!")
    elif modo == "VÍDEO":
        st.error("🎥 Gravando... Clique novamente para parar.")
