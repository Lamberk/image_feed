import sqlite3
from sqlalchemy.exc import IntegrityError
from app.models import Product
from app import db
import xml.etree.ElementTree as ET

id = 1

file_name = 'ec_xml_feed.xml'
tree = ET.parse(file_name)
root = tree.getroot()
for product in root:
    if product.find('freeshipping').text == 'False':
        free_shipping = False
    elif product.find('freeshipping').text == 'True':
        free_shipping = True
    if product.find('pricespecial').text:
        pricespecial = float(product.find('pricespecial').text)
    else:
        pricespecial = None
    new_product = Product(
        id = id,
        sku = product.find('sku').text,
        loyality_programm = bool(int(product.find('linio_plus_enabled').text)),
        free_shipping = free_shipping,
        image_url = product.find('imagelarge').text,
        product_title = product.find('name').text,
        price = float(product.find('price').text),
        pricespecial = pricespecial,
    )
    db.session.add(new_product)
    id += 1
db.session.commit()
