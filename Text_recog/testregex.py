import re
import json

def extract_products_and_prices(receipt_text):
    # Define a regex pattern to match product lines
    product_pattern = re.compile(r'([A-Z\s&/.()0-9]+)\s+(\d+)\s+(\d{4,5})\s+(\d{1,3}(?:,\d{3})*)')
    
    # Normalize newline characters and split the text into lines
    lines = receipt_text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    
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

# Example receipt text
receipt_text = """
SLANCOL 1/-10,ANCOL —_, |
BARAT Jakart UTa i,
NPWP Ot S37 04 B-082 O00 | ey |
BESI JANGKANG KM. 1.5/004 0274445494
JL.BESI JANGKANG KM. 1.5 RT 01 RW 13 MINDI
» SUKOHARJO, NGAGLIK, SLEMAN, SLEMAN, 5558
16.06.18-17:08 — 2,1,27 301135/RATIH/01
ABC ORANGE 525ML 1 13500 13,500
I/F BISC.WNDRLND 300 1 20909 20,900
LEXUS SANDW COKL 190 1 26800 26,800
LUWAK WHT ORGL 20X20 1 25400 25,400
OREO CHO & VAN 2X137 = 1—«*19800 19, 800
TONG TJI JASM T/A.25 1 9300 9,300
KOPIKO 78C 240ML 2 5500 11,000
FRSTEA TEH MADU 350 1 3950 3,950
SOVIA M/GORENG 21 1 26950 26,950
CANCEL : — (1)(26950) (26,950)
HARGA JUAL : 130,650
VOUCHER ABC SQUASH ORANGE ; (3,600)
VOUCHER INDOFOOD WONDERLAND : (10,000)
TONG TJI TEA INDONESTA : (S0n\
"""

# Extract products and prices from the receipt text
products_json = extract_products_and_prices(receipt_text)

# Print the resulting JSON
print(products_json)
