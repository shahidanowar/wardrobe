import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

# Categories for clothing classification
CATEGORIES = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
]

# Load pre-trained model (this is a placeholder - you'll need to implement the actual model loading)
def load_model():
    # This is a placeholder for the actual model loading code
    # You would typically load a pre-trained model here
    model_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/4"
    model = tf.keras.Sequential([
        hub.KerasLayer(model_url)
    ])
    return model

def preprocess_image(image_path):
    """Preprocess image for model input."""
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

def classify_image(image_path):
    """Classify an image using the pre-trained model."""
    try:
        model = load_model()
        processed_image = preprocess_image(image_path)
        predictions = model.predict(processed_image)
        predicted_class = CATEGORIES[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))
        return predicted_class, confidence
    except Exception as e:
        print(f"Error in image classification: {str(e)}")
        return "Unknown", 0.0

def generate_outfit_recommendation(items, occasion):
    """Generate outfit recommendations based on available items and occasion."""
    # This is a simple rule-based recommendation system
    # In a production environment, you would want to use a more sophisticated approach
    
    occasion_rules = {
        'formal': {
            'top': ['Shirt', 'Coat'],
            'bottom': ['Trouser'],
            'shoes': ['Ankle boot']
        },
        'casual': {
            'top': ['T-shirt/top', 'Pullover'],
            'bottom': ['Trouser'],
            'shoes': ['Sneaker', 'Sandal']
        },
        'party': {
            'top': ['Shirt', 'T-shirt/top'],
            'bottom': ['Trouser'],
            'shoes': ['Sneaker', 'Ankle boot']
        }
    }
    
    if occasion not in occasion_rules:
        occasion = 'casual'
    
    outfit = []
    rules = occasion_rules[occasion]
    
    # Select one item for each category based on the rules
    for category, allowed_types in rules.items():
        suitable_items = [
            item for item in items
            if item.category.lower() == category.lower() and
            item.predicted_category in allowed_types
        ]
        if suitable_items:
            outfit.append(np.random.choice(suitable_items))
    
    return outfit
