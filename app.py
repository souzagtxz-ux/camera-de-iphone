import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import av

# Configuração de Estilo iOS
st.set_page_config(page_title="Camera iOS 16 Pro - Souza", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    [data-testid="stSidebar"] { background-color: #121212; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Assinatura do Desenvolvedor Souza */
    .dev-signature {
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 10px;
        letter-spacing: 2px;
        color: #888888;
        margin-top: 10px;
        text-transform: uppercase;
    }

    /* Botão de obturador estilo iPhone */
    .stButton>button {
        border-radius: 50%; width: 80px; height: 80px;
        border: 4px solid #ffffff; background-color: #ffffff;
        box-shadow: 0 0 15px rgba(255,255,255,0.3);
        margin: 0 auto; display: block; transition: 0.2s;
    }
    .stButton>button:active { transform: scale(0.9); background-color: #dddddd; }
    </style>
    """, unsafe_allow_html=True)

# Barra Lateral - Estilos Fotográficos
st.sidebar.title("Ajustes Pro")
estilo = st.sidebar.radio("Estilo de Cor", ["Padrão", "Vívido", "Contraste Rico", "Quente", "Frio", "Cinematográfico"])

# Créditos no Sidebar também
st.sidebar.markdown("---")
st.sidebar.write("👤 **Dev:** Souza")

def process_frame(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # Lógica de Filtros (Ajuste A18 Pro Simulation)
    if estilo == "Vívido":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = cv2.convertScaleAbs(hsv[:,:,1], alpha=1.4)
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    elif estilo == "Contraste Rico":
        img = cv2.convertScaleAbs(img, alpha=1.3, beta=-20)
    elif estilo == "Quente":
        img[:, :, 2] = cv2.add(img[:, :, 2], 35)
    elif estilo == "Frio":
        img[:, :, 0] = cv2.add(img[:, :, 0], 40)
    elif estilo == "Cinematográfico":
        img = cv2.GaussianBlur(img, (3, 3), 0)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Título e Visor
st.markdown("<h3 style='text-align: center;'>FOTO</h3>", unsafe_allow_html=True)

webrtc_streamer(
    key="ios_camera",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=process_frame,
    media_stream_constraints={
        "video": {
            "width": {"ideal": 3840}, 
            "height": {"ideal": 2160},
            "facingMode": "environment"
        },
        "audio": False
    },
    async_processing=True,
)

# Assinatura Souza abaixo do visor
st.markdown("<p class='dev-signature'>Desenvolvedor: SOUZA</p>", unsafe_allow_html=True)

# Interface de Modos
st.markdown("""
    <div style='display: flex; justify-content: center; gap: 20px; font-weight: bold; font-size: 11px; margin: 15px 0;'>
        <span style='color: #555;'>VÍDEO</span>
        <span style='color: #FFCC00;'>FOTO</span>
        <span style='color: #555;'>RETRATO</span>
    </div>
    """, unsafe_allow_html=True)

# Botão Disparador
if st.button(" "):
    st.toast("Capturado com sucesso!")
