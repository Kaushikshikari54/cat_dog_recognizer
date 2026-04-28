import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --------------------
# CONFIG
# --------------------
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 5

TRAIN_DIR = "dataset/train"
VAL_DIR = "dataset/validation"
MODEL_SAVE_PATH = "model/cat_dog_model.h5"

# --------------------
# DATA GENERATORS
# --------------------
train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

val_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_data = val_gen.flow_from_directory(
    VAL_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

# --------------------
# MODEL (TRANSFER LEARNING)
# --------------------
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
output = Dense(2, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# --------------------
# TRAIN
# --------------------
model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# --------------------
# SAVE MODEL
# --------------------
model.save(MODEL_SAVE_PATH)
print("✅ Model trained and saved successfully")