from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import json
import re

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
    formatted_text = add_newlines(text, line_length=80)
    return text

def classify_text(text):
    inputs = tokenizer(text, return_tensors="tf", truncation=True, padding=True)
    outputs = model(inputs)
    predictions = tf.nn.softmax(outputs.logits, axis=-1)
    return predictions

# def parse_receipt(receipt_text):
#     # Ekstraksi produk dan harga menggunakan regular expression
#     pattern = re.compile(r'([A-Z/\s]+)\s+\d+\s+(\d+,\d+)')
#     matches = pattern.findall(receipt_text)

#     # Format hasil ekstraksi ke dalam JSON
#     products = []
#     for match in matches:
#         product_name = match[0].strip()
#         price = match[1].replace(',', '')
#         products.append({"product_name": product_name, "price": int(price)})

#     # Convert to JSON
#     products_json = json.dumps(products, indent=4)

#     return products_json

def add_newlines(text, line_length=80):
    lines = []
    while len(text) > line_length:
        space_index = text.rfind(' ', 0, line_length)
        if space_index == -1:
            space_index = line_length
        lines.append(text[:space_index])
        text = text[space_index:].strip()
    lines.append(text)
    return '\n'.join(lines)

def extract_products_from_receipt(text):
    # Pola regex untuk mencocokkan nama produk, jumlah, harga satuan, dan total harga
    product_pattern = re.compile(r'([A-Z\s/]+)\s+(\d+)\s+(\d+)\s+(\d{1,3},\d{3})')
    
    # Mencari semua kecocokan
    matches = product_pattern.findall(text)
    
    # Membuat list untuk menyimpan produk dan harga
    products = []
    for match in matches:
        product_name = match[0].strip()
        jumlah = int(match[1])
        harga_satuan = int(match[2])
        total_harga = int(match[3].replace(',', ''))
        products.append({
            "nama_produk": product_name,
            "jumlah": jumlah,
            "harga_satuan": harga_satuan,
            "total_harga": total_harga
        })
    
    return products

# def extract_products_from_receipt(receipt_text):
#     # Pola regex untuk mencocokkan produk dan harganya
#     # pattern = r"([A-Z0-9/\s]+) (\d+) (\d+),?(\d*) (\d+),?(\d*)"
#     pattern = r"([A-Z\s/]+)\s+(\d+)\s+(\d+)\s+(\d{1,3},\d{3})"

#     # Menemukan semua kecocokan dalam teks struk
#     matches = re.findall(pattern, receipt_text)

#     # Menampung produk dan harganya
#     products = []

#     for match in matches:
#         nama_produk = match[0].strip()
#         jumlah = int(match[1])
#         harga_satuan = int(match[2] + match[3])
#         total_harga = int(match[4] + match[5])
#         products.append({
#             "nama_produk": nama_produk,
#             "jumlah": jumlah,
#             "harga_satuan": harga_satuan,
#             "total_harga": total_harga
#         })
#     return products

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
            products = extract_products_from_receipt(text)
            predictions = classify_text(text)
            return render_template('result.html', text=text, predictions=predictions, products=products)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)