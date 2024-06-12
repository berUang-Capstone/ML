from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import tensorflow as tf
import json
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_files'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text(image_path):
    image = Image.open(image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    #formatted_text = add_newlines(text, line_length=80)
    return text

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

## Best Work
def extract_products_from_receipt(text):
    # Pola regex untuk mencocokkan nama produk, jumlah, harga satuan, dan total harga
    # product_pattern = re.compile(r'([A-Z\s/]+)\s+(\d+)\s+(\d+)\s+(\d{1,3},\d{3})')
    # product_pattern = re.compile(r'([A-Z\s&/.()0-9]+) (\d+) (\d{4,5}) (\d{1,3}(?:,\d{3})*)') # not bad
    product_pattern = re.compile(r'([A-Z\s&/.()0-9]+) (\d+) (\d{4,5}) (\d{1,3},\d{3})') # not bad
    # product_pattern = re.compile(r"([A-Z\/\s]+)\d+\s+([\d,]+)\s+([\d,]+)")
    
    # Normalize newline characters and split the text into lines
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    
    # Find matches in each line
    products = []
    for line in lines:
        match = product_pattern.search(line)
        if match:
            product_name = match.group(1).strip()
            quantity = int(match.group(2))
            unit_price = int(match.group(3))
            total_price = int(match.group(4).replace(',', ''))
            products.append({
                "name": product_name,
                "amount": total_price
            })
    
    # Convert the list of dictionaries to JSON
    products_json = json.dumps(products, indent=2)
    return products_json

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        text = extract_text(filepath)
        products = extract_products_from_receipt(text)
        return products
        #return jsonify({'message': f'File {filename} uploaded successfully'}), 200
    else:
        return jsonify({'error': 'File extension not allowed'}), 400
    


if __name__ == '__main__':
    app.run(debug=True)