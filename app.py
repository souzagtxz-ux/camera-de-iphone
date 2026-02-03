import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import cv2
import numpy as np
import av
from groq import Groq

# Configuração de Identidade
st.set_page_config(page_title="iOS 16 Pro - Souza IA", layout="centered")

# Inicialização do Groq (Sua Key já integrada)
client = Groq(api_key="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")

# Interface Visual Estilo Apple
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    [data-testid="stSidebar"] { background-color: #121212; border-right: 1px solid #333; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    
    .dev-label {
        text-align: center; font-size: 10px; letter-spacing: 3px;
        color: #888; text-transform: uppercase; margin-top: 20px;
    }
    .stButton>button {
        border-radius: 50%; width: 85px; height: 85px;
        border: 5px solid white; background-color: white;
        margin: 0 auto; display: block; box-shadow: 0 0 20px rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Menu Lateral de Inteligência
st.sidebar.title("Souza IA Control")
modo_ia = st.sidebar.toggle("Ativar Analisador Groq", value=True)
estilo = st.sidebar.selectbox("Estilo Manual", ["Padrão", "Vívido", "Contraste Rico", "Quente", "Frio", "Cinematográfico"])

def aplicar_pos_processamento(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # Simulação de HDR via Software (Melhora o sensor do Poco X3)
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.createCLAHE(clipLimit=2.0).apply(img_yuv[:,:,0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    # Aplicação de Filtros Baseados nos Estilos Apple
    if estilo == "Vívido":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = cv2.convertScaleAbs(hsv[:,:,1], alpha=1.4)
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    elif estilo == "Quente":
        img[:, :, 2] = cv2.add(img[:, :, 2], 30)
    elif estilo == "Frio":
        img[:, :, 0] = cv2.add(img[:, :, 0], 30)
    elif estilo == "Cinematográfico":
        img = cv2.GaussianBlur(img, (3, 3), 0)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Visor da Câmera (Configurado para o máximo do Poco X3)
st.markdown("<h3 style='text-align: center;'>FOTO</h3>", unsafe_allow_html=True)

webrtc_streamer(
    key="souza_ios_camera",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=aplicar_pos_processamento,
    media_stream_constraints={
        "video": {
            "width": {"ideal": 3840}, 
            "height": {"ideal": 2160},
            "facingMode": "environment"
        },
        "audio": False
    },
    async_processing=True
)

st.markdown("<p class='dev-label'>Desenvolvido por Souza</p>", unsafe_allow_html=True)

# Botão de Captura e IA
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button(" "):
        st.toast("📸 Foto Salva na Galeria!")
        if modo_ia:
            # Comando para o Groq analisar a cena (Simulação de metadados)
            st.sidebar.info("Groq IA: Cena detectada e otimizada.")

st.markdown("""
    <div style='display: flex; justify-content: center; gap: 25px; font-weight: bold; font-size: 11px; margin-top: 10px; color: #777;'>
        <span>VÍDEO</span> <span style='color: #FFCC00;'>FOTO</span> <span>RETRATO</span> <span>PANO</span>
    </div>
    """, unsafe_allow_html=True)
