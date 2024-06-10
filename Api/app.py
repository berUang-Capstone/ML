from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the model
model = load_model('Api\model.h5')
with open('Api/tokenizer.joblib', 'rb') as f:
    tokenizer = joblib.load(f)
with open('Api/label_encoder.joblib', 'rb') as f:
    label_encoder = joblib.load(f)
    

# Preprocess function to convert text input into a format the model expects
def preprocess_text(text):
    # Tokenize and pad the text as needed
    # This should match the preprocessing done during training
    # For demonstration, assuming the existence of a tokenizer and max_length
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=5 , padding='post')
    return padded_sequences

@app.route('/')
def home():
    return "NLP Model Deployment API"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get the data from the request
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Preprocess the input text
    input_data = preprocess_text(text)
    
    # Make a prediction
    prediction = model.predict(input_data)
    
    treshold = 0.3

    # Memeriksa apakah probabilitas tertinggi kurang dari treshold
    if np.max(prediction) < treshold:
        predicted_class = "other"
    else:
        predicted_class_index = np.argmax(prediction, axis=1)
        predicted_class = label_encoder.inverse_transform(predicted_class_index)[0]

    # Output prediksi kelas
    print("Predicted Class:", predicted_class)

    probabilities_rounded = [float(round(prob, 4)) for prob in prediction[0]]
    # print("Predicted probabilities:", probabilities_rounded)
    
    # Return the prediction as a JSON response
    return jsonify({
                    'probabilities': probabilities_rounded,
                    'class_predicted': predicted_class, 
                    })

if __name__ == '__main__':
    app.run(debug=True)
