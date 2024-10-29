import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Função para carregar o modelo
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('modelo.keras')  # Substitua pelo caminho do seu modelo
    return model

# Função para fazer a previsão
def predict(image, model):
    # Pré-processamento da imagem
    image = image.resize((224, 224))  # Ajuste para o tamanho de entrada do seu modelo
    image = np.array(image) / 255.0  # Normalizar os valores dos pixels para [0, 1]
    image = np.expand_dims(image, axis=0)  # Adicionar uma dimensão para batch
    # Fazer a previsão
    prediction = model.predict(image)
    return prediction

# Interface do Streamlit
st.title('Previsão de Imagens com IA')
st.write('Envie uma imagem e o modelo fará a previsão com base no que foi treinado.')

# Upload de imagem
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Carregar a imagem
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagem Carregada', use_column_width=True)
    st.write("Carregando...")

    # Carregar o modelo
    model = load_model()

    # Fazer a previsão
    prediction = predict(image, model)

    # Mostrar o resultado
    st.write("Resultado da Previsão:", prediction)
