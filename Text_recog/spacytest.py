import spacy
import re

# Load model bahasa Inggris
nlp = spacy.load("en_core_web_sm")

def extract_items(text):
    doc = nlp(text)
    
    items = []
    current_item = {}
    for token in doc:
        # Jika token adalah angka, mungkin itu adalah jumlah atau harga
        if token.like_num:
            if 'quantity' not in current_item:
                current_item['quantity'] = int(token.text)
            elif 'price' not in current_item:
                current_item['price'] = int(token.text.replace(',', ''))
                items.append(current_item)
                current_item = {}
        # Jika token adalah kata, itu mungkin adalah nama item
        elif token.is_alpha:
            if 'quantity' not in current_item and 'name' not in current_item:
                current_item['name'] = token.text
    return items

# Contoh teks
text = """
ABC ORANGE 525ML 1 13500
BISC.WNDRLND 300 1 20909
LEXUS SANDW COKL 190 1 26800
LUWAK WHT ORGL 20X20 1 25400
OREO CHO & VAN 2X137 1 19800
TONG TJI JASM T/A.25 1 9300
KOPIKO 78C 240ML 2 5500
FRSTEA TEH MADU 350 1 3950
SOVIA M/GORENG 21 1 26950
"""

# Ekstraksi item dari teks
items = extract_items(text)

# Cetak hasil
for item in items:
    print(item)
