from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:/MSIB/Text_recog/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Load the pre-trained BERT model and tokenizer
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2) # Adjust num_labels as needed
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text(image_path):
    image = Image.open(image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

def classify_text(text):
    inputs = tokenizer(text, return_tensors="tf", truncation=True, padding=True)
    outputs = model(inputs)
    predictions = tf.nn.softmax(outputs.logits, axis=-1)
    return predictions

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = extract_text(filepath)
            predictions = classify_text(text)
            return render_template('result.html', text=text, predictions=predictions)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)