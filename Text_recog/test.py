from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import json
import re

def extract_text(image_path):
    image = Image.open(image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

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
                "nama_produk": product_name,
                "jumlah": quantity,
                "harga_satuan": unit_price,
                "total_harga": total_price
            })
    
    # Convert the list of dictionaries to JSON
    products_json = json.dumps(products, indent=4)
    return products_json

text = extract_text('Text_recog/uploads/WhatsApp_Image_2024-05-16_at_16.17.02.jpeg')
products = extract_products_from_receipt(text)

print(products)