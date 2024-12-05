import os
import numpy as np
import streamlit as st
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model

# Load the VGG16 model
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    features = model.predict(img_array)
    features = features.flatten()

    return features

def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img_path)
    return images

# Streamlit app
st.title("Image Similarity Checker")

# Folder path input
folder_path = st.text_input("/content/downloaded_images")

if folder_path:
    # Load images
    image_paths = load_images_from_folder(folder_path)

    if len(image_paths) > 10:
        # Extract features for the first 10 images
        features_list = []
        for img_path in image_paths[:10]:
            features = extract_features(img_path)
            features_list.append(features)

        # Extract features for the 11th image
        new_image_path = image_paths[10]
        new_image_features = extract_features(new_image_path)

        # Calculate cosine similarity between the 11th image and each of the first 10 images
        similarities = []
        for i, features in enumerate(features_list):
            similarity = cosine_similarity([new_image_features], [features])
            similarities.append((i+1, similarity[0][0]))

        # Sort similarities in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Display the similarities
        st.write("Similarities with the 11th image:")
        for i, similarity in similarities:
            st.write(f"Similarity with image {i}: {similarity}")
    else:
        st.write("Please ensure the folder contains at least 11 images.")
