import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# 1. Fix: Point to the actual subfolder and filename shown in your sidebar
# We use absolute path logic to ensure it works regardless of where you run it from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "cat_dog_model.h5")

# Load model once
model = load_model(MODEL_PATH)

class_names = ["cat", "dog"]  # must match training order

def predict_image(img_path):
    # 2. Fix: Changed from 150 to 224 to match your MobileNetV2 training config
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Preprocess input (MobileNetV2 expects -1 to 1 or 0 to 1 depending on version)
    # Using 1./255 to match your train_model.py ImageDataGenerator
    img_array = img_array / 255.0

    prediction = model.predict(img_array)

    # Since you used categorical_crossentropy with 2 units:
    predicted_index = np.argmax(prediction)
    label = class_names[predicted_index]
    confidence = float(np.max(prediction))

    return label, confidence