import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('checkpoint_best.keras')
    return model

def predict(image, model):
    image = image.resize((225, 150))  # Certifique-se de redimensionar para (225, 150)
    image = np.array(image) / 255.0  
    image = np.expand_dims(image, axis=0)  
    prediction = model.predict(image)
    
    #class_names = ['Healthy', 'Multiple deseases', 'Powdery', 'Rust', 'Scab']
    predicted_class = prediction # class_names[np.argmax(prediction)]
    
    return predicted_class

def plot_confusion_matrix(cm, class_names):
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    st.pyplot(plt)

st.title('Previsão de Imagens com IA')
st.write('Envie uma imagem e o modelo fará a previsão com base no que foi treinado.')

uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagem Carregada', use_container_width=True)
    st.write("Carregando...")

    model = load_model()
    prediction = predict(image, model)
    st.write("Resultado da Previsão:", prediction)

    # Mostrar a matriz de confusão
    if st.button('Mostrar Matriz de Confusão'):
        # Carregar dados de validação
        VALID_DIR = 'fusionValidate2/'
        validation_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
        validation_generator = validation_datagen.flow_from_directory(VALID_DIR, target_size=(225, 150), class_mode='categorical', shuffle=False)

        # Obter previsões e rótulos verdadeiros
        y_pred = model.predict(validation_generator)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true = validation_generator.classes

        # Calcular a matriz de confusão
        cm = confusion_matrix(y_true, y_pred_classes)
        class_names = list(validation_generator.class_indices.keys())
        plot_confusion_matrix(cm, class_names)