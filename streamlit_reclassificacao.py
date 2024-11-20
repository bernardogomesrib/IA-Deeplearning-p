import streamlit as st
import os
from PIL import Image
import shutil

# Diretório onde as imagens estão armazenadas
IMAGE_DIR = 'fusion2'
TARGET_DIR = 'target'

# Variável de contagem para renomear as imagens reclassificadas
count = 0

# Função para carregar imagens do diretório
def load_images(image_dir):
    images = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith(('jpg', 'jpeg', 'png')):
                images.append(os.path.join(root, file))
    return images

# Função para carregar pastas do diretório
def load_labels(image_dir):
    labels = []
    for root, dirs, files in os.walk(image_dir):
        for dir in dirs:
            labels.append(dir)
        break  # Apenas o primeiro nível de diretórios
    return labels

# Função para salvar a imagem reclassificada
def save_reclassified_image(image_path, label):
    global count
    count += 1
    target_path = os.path.join(TARGET_DIR, label)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    new_image_name = f"reclassified-{count}.jpg"
    new_image_path = os.path.join(target_path, new_image_name)
    shutil.copy(image_path, new_image_path)
    return new_image_path

# Carregar imagens
images = load_images(IMAGE_DIR)

# Carregar labels
labels = load_labels(IMAGE_DIR)

# Interface do Streamlit
st.title('Reclassificação de Imagens')

if images:
    # Selecionar uma imagem
    image_path = st.selectbox('Selecione uma imagem para reclassificar', images)
    image = Image.open(image_path)
    st.image(image, caption=os.path.basename(image_path), use_container_width=True)

    # Botões para nova classificação
    st.write('Selecione a nova classificação para a imagem:')
    for label in labels:
        if st.button(label):
            new_image_path = save_reclassified_image(image_path, label)
            st.write(f'Imagem reclassificada e salva em: {new_image_path}')
else:
    st.write('Nenhuma imagem encontrada no diretório especificado.')