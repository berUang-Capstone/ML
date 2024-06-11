import spacy
import re

# Load model bahasa Inggris
nlp = spacy.load("en_core_web_sm")

def extract_items(text):
    # Pola regex untuk menangkap nama barang, jumlah, dan harga
    pattern = r'(\d+)\s+(.*?)\s+(\d+)\s+(.*?)\s+(\d+)\s+(\d+,\d+)'

    # Temukan semua kemunculan pola yang cocok dalam teks
    matches = re.findall(pattern, text)

    items = []
    for match in matches:
        quantity = int(match[0])
        name = match[1]
        price_per_unit = int(match[2].replace(',', ''))
        unit = match[3]
        total_price = int(match[4])
        subtotal = int(match[5].replace(',', ''))
        
        items.append({
            "name": name,
            "quantity": quantity,
            "unit": unit,
            "price_per_unit": price_per_unit,
            "total_price": total_price,
            "subtotal": subtotal
        })

    return items

# Contoh teks nota
text = """
NOTA

TOKO MAKMUR

No Nota :
Kepada Yth : Ibu Rita (Warung Berkah)

Tanggal Nota : 28/02/2022

NO Nama Barang Jumlah Beli Harga Sub Total
1 Telur Ayam/kg 5 kg 20.000 100.000
2 Gula Pasir /kg 5 kg 12.500 62.500
3 Kecap Manis 60 ml / dus 1 dus 120.000 120.000
4 Minyak Goreng 1L 10L 14.000 140.000
5 Sampo Renceng 10 9.800 98.000
6 Mie Instan Soto / dus 1 dus 96.000 96.000
7 Mie Instan Goreng / dus 1 dus 102.000 102.000
8 Garam / bungkus 10 bungkus 2.500 25.000
9 Makanan Bayi Renceng 1 77.000 77.000
Jumlah 820.500
NB:
Barang yang sudah dibeli Hormat Kami,
Tidak dapat ditukar kembali

(Rudi)
"""

# Ekstraksi item dari teks nota
items = extract_items(text)

# Cetak hasil
for item in items:
    print(item)
