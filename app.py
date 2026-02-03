import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import av
from groq import Groq
import PIL.Image as Image
import io

# Configuração de App Nativo
st.set_page_config(page_title="Souza Cam", layout="wide", initial_sidebar_state="collapsed")

# 1. CSS DE ELITE (Interface iPhone 16)
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #000; }
    
    /* Botão de Disparo Branco Circular */
    div.stButton > button {
        border-radius: 50% !important;
        width: 80px !important; height: 80px !important;
        border: 5px solid white !important;
        background: radial-gradient(circle, #fff 40%, transparent 50%) !important;
        position: fixed !important; bottom: 30px !important;
        left: 50% !important; transform: translateX(-50%) !important;
        z-index: 9999 !important;
    }

    /* Seletor de Filtros Central */
    .stSelectbox div[data-baseweb="select"] {
        background-color: transparent !important;
        border: none !important;
        color: #FFCC00 !important;
        font-weight: bold !important;
        text-align: center !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. IA E FILTROS
client = Groq(api_key="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")
filtros_iphone = ["PADRÃO", "VÍVIDO", "VÍVIDO QUENTE", "VÍVIDO FRIO", "DRAMÁTICO", "DRAMÁTICO FRIO", "P&B"]
filtro_selecionado = st.selectbox("", filtros_iphone, index=0, label_visibility="collapsed")

# Função que aplica a "mágica" nos frames
def engine_iphone(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # Smart Sharpening
    kernel = np.array([[-0.5,-0.5,-0.5], [-0.5,5,-0.5], [-0.5,-0.5,-0.5]])
    img = cv2.filter2D(img, -1, kernel)

    # Lógica de Cores Apple
    if "VÍVIDO" in filtro_selecionado:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = cv2.convertScaleAbs(hsv[:,:,1], alpha=1.3)
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    if "DRAMÁTICO" in filtro_selecionado:
        img = cv2.convertScaleAbs(img, alpha=1.25, beta=-15)
        if "FRIO" in filtro_selecionado:
            img[:, :, 0] = cv2.add(img[:, :, 0], 25)

    if filtro_selecionado == "P&B":
        img = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# 3. WEBRTC (O Visor)
ctx = webrtc_streamer(
    key="souza-final",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=engine_iphone,
    media_stream_constraints={"video": {"facingMode": "environment"}, "audio": False},
    async_processing=True
)

# 4. CAPTURA E DOWNLOAD
if st.button(" "):
    if ctx.video_receiver:
        try:
            # Pega o último frame processado
            frame = ctx.video_receiver.get_frame(timeout=1)
            img_save = frame.to_ndarray(format="bgr24")
            img_save = cv2.cvtColor(img_save, cv2.COLOR_BGR2RGB)
            
            # Converte para baixar
            final_img = Image.fromarray(img_save)
            buf = io.BytesIO()
            final_img.save(buf, format="JPEG", quality=95)
            byte_im = buf.getvalue()
            
            st.toast("📸 Foto capturada!")
            st.download_button(label="SALVAR NA GALERIA", data=byte_im, file_name="souza_cam.jpg", mime="image/jpeg")
            
            # IA do Groq analisa o cenário
            st.info("IA Souza: Analisando iluminação...")
        except:
            st.warning("Aguarde a câmera iniciar...")
