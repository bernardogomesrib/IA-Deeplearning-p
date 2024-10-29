import os
import shutil
import streamlit as st
from PIL import Image
import uuid

# Função para listar todas as imagens nas subpastas
def list_images(base_dir):
    image_paths = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_paths.append(os.path.join(root, file))
    return image_paths

# Função para copiar e renomear a imagem com base na classificação
def classify_and_copy(image_path, target_dir, new_label):
    # Criar a pasta de destino para a nova classificação
    target_label_dir = os.path.join(target_dir, new_label)
    os.makedirs(target_label_dir, exist_ok=True)

    # Gerar um novo nome para a imagem usando um UUID
    new_name = f"{uuid.uuid4()}.jpg"
    new_path = os.path.join(target_label_dir, new_name)

    # Copiar a imagem para o novo diretório
    shutil.copy(image_path, new_path)
    return new_path

# Interface do Streamlit
st.title('Classificação de Imagens com Streamlit')

# Caminho da pasta base e da pasta de destino
base_dir = st.text_input('Caminho da pasta base com as imagens', '/path/to/your/images')
target_dir = st.text_input('Caminho da pasta de destino para as imagens classificadas', '/path/to/target/directory')

# Opções de classificação
class_labels = st.text_input('Digite as classificações disponíveis (separadas por vírgula)', 'categoria1, categoria2, categoria3')
class_labels = [label.strip() for label in class_labels.split(',')]

if base_dir and target_dir and class_labels:
    # Listar as imagens
    images = list_images(base_dir)
    
    if images:
        # Selecionar uma imagem para classificação
        current_image_path = images[0]
        image = Image.open(current_image_path)
        st.image(image, caption='Imagem para Classificação', use_column_width=True)

        # Selecionar a classificação
        selected_label = st.selectbox('Escolha a classificação para esta imagem:', class_labels)

        # Botão para classificar a imagem
        if st.button('Classificar Imagem'):
            # Classificar e copiar a imagem
            new_image_path = classify_and_copy(current_image_path, target_dir, selected_label)
            
            # Renomear a imagem original para evitar reclassificação
            original_renamed_path = current_image_path + '.classified'
            os.rename(current_image_path, original_renamed_path)

            st.success(f'Imagem classificada e copiada para: {new_image_path}')
            st.info(f'A imagem original foi renomeada para: {original_renamed_path}')
    else:
        st.warning('Nenhuma imagem encontrada na pasta especificada.')
else:
    st.warning('Por favor, preencha todos os campos.')

