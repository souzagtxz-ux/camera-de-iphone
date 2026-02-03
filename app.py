import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import av
import time
import io
from PIL import Image

# Configuração de App Nativo Fullscreen
st.set_page_config(page_title="Souza Cam Pro", layout="wide", initial_sidebar_state="collapsed")

# 1. CSS PARA OS MODOS NO RODAPÉ
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #000; color: white; }
    
    /* Container dos Modos (Carrossel) */
    .mode-selector {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 80px;
        font-family: sans-serif;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    /* Botão de Disparo */
    div.stButton > button {
        border-radius: 50% !important;
        width: 80px !important; height: 80px !important;
        border: 5px solid white !important;
        position: fixed !important; bottom: 30px !important;
        left: 50% !important; transform: translateX(-50%) !important;
        z-index: 9999 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SELEÇÃO DE MODO ESTILO IPHONE
st.markdown('<div class="mode-selector">', unsafe_allow_html=True)
modo = st.radio("", ["VÍDEO", "FOTO", "LIVE", "NOITE"], horizontal=True, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# 3. FILTROS IOS (Aparecem na lateral para não poluir)
filtro = st.sidebar.selectbox("ESTILO", ["PADRÃO", "VÍVIDO", "DRAMÁTICO", "P&B"])

def engine_ultra(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # --- MODO NOITE (LONG EXPOSURE SIMULATION) ---
    if modo == "NOITE":
        # Aumenta ganho de luz e reduz ruído
        img = cv2.convertScaleAbs(img, alpha=1.5, beta=30)
        img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    # --- NITIDEZ (SHARPENING) ---
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    img = cv2.filter2D(img, -1, kernel)

    # --- FILTROS ---
    if filtro == "VÍVIDO":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = cv2.convertScaleAbs(hsv[:,:,1], alpha=1.4)
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    elif filtro == "DRAMÁTICO":
        img = cv2.convertScaleAbs(img, alpha=1.3, beta=-20)
    elif filtro == "P&B":
        img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# 4. CÂMERA
ctx = webrtc_streamer(
    key="souza-ultra",
    video_frame_callback=engine_ultra,
    media_stream_constraints={
        "video": {"facingMode": "environment"},
        "audio": (modo == "VÍDEO")
    },
    async_processing=True
)

# 5. LÓGICA DO BOTÃO DE DISPARO
if modo == "VÍDEO":
    st.markdown("<style>div.stButton > button { background: red !important; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>div.stButton > button { background: white !important; }</style>", unsafe_allow_html=True)

if st.button(" "):
    if modo == "LIVE":
        st.toast("🟡 LIVE")
        time.sleep(1.5)
        st.success("Momento Live capturado!")
    elif modo == "FOTO" or modo == "NOITE":
        st.toast("📸 Capturando...")
        if ctx.video_receiver:
            frame = ctx.video_receiver.get_frame(timeout=1)
            img = frame.to_ndarray(format="bgr24")
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            buf = io.BytesIO()
            Image.fromarray(img_rgb).save(buf, format="JPEG")
            st.download_button("SALVAR NA GALERIA", buf.getvalue(), "foto.jpg", "image/jpeg")
