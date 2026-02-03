import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import av
import io
from PIL import Image

st.set_page_config(page_title="Camera", layout="wide", initial_sidebar_state="collapsed")

# CSS para criar as molduras pretas (Top e Bottom bars)
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #000; }
    
    /* Moldura superior preta */
    .ios-header {
        height: 80px; background: #000;
        display: flex; justify-content: space-around; align-items: center;
        position: fixed; top: 0; width: 100%; z-index: 1000;
        color: white; font-size: 18px;
    }

    /* Ajuste do visor da câmera para não ocupar a tela toda */
    video {
        object-fit: cover;
        margin-top: 80px; /* Desce a imagem para baixo da barra preta */
        height: calc(100vh - 300px) !important; /* Corta para caber a barra de baixo */
        width: 100% !important;
    }

    /* Moldura inferior preta (onde ficam os botões) */
    .ios-footer {
        height: 220px; background: #000;
        position: fixed; bottom: 0; width: 100%; z-index: 1000;
    }

    /* Seletores de Zoom dentro da imagem */
    .zoom-float {
        position: fixed; bottom: 240px; width: 100%;
        display: flex; justify-content: center; gap: 10px; z-index: 1001;
    }
    .z-btn {
        background: rgba(0,0,0,0.5); border-radius: 50%; width: 32px; height: 32px;
        color: white; font-size: 10px; display: flex; align-items: center; justify-content: center;
    }

    /* Modos e Botão no fundo preto */
    .mode-list {
        position: fixed; bottom: 130px; width: 100%;
        display: flex; justify-content: center; gap: 20px;
        color: white; font-weight: bold; font-size: 13px; z-index: 1001;
    }
    .mode-yellow { color: #FFCC00; }

    div.stButton > button {
        border-radius: 50% !important;
        width: 75px !important; height: 75px !important;
        border: 4px solid white !important;
        background: transparent !important;
        position: fixed !important; bottom: 35px !important;
        left: 50% !important; transform: translateX(-50%) !important;
        z-index: 1002;
    }
    div.stButton > button::after {
        content: ""; display: block; width: 60px; height: 60px;
        background: white; border-radius: 50%; margin: auto;
    }
    </style>
    
    <div class="ios-header">
        <span>⚡</span> <span>H̅D̅R̅</span> <span>🟡</span> <span><i class="fa fa-chevron-up"></i></span>
    </div>

    <div class="zoom-float">
        <div class="z-btn">0.5</div> <div class="z-btn" style="border:1px solid #FFCC00">1x</div> <div class="z-btn">2</div>
    </div>

    <div class="ios-footer">
        <div class="mode-list">
            <span style="opacity:0.6">VÍDEO</span>
            <span class="mode-yellow">FOTO</span>
            <span style="opacity:0.6">RETRATO</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def engine_iphone_style(frame):
    img = frame.to_ndarray(format="bgr24")
    # Aplica o Dramático Frio
    img = cv2.convertScaleAbs(img, alpha=1.2, beta=-10)
    img[:, :, 0] = cv2.add(img[:, :, 0], 20)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="iphone-layout",
    video_frame_callback=engine_iphone_style,
    media_stream_constraints={"video": {"facingMode": "environment"}},
    async_processing=True
)

if st.button(" "):
    st.toast("📸 Foto Salva!")
