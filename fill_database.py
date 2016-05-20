from sqlalchemy.exc import IntegrityError
from app.models import Product
from app import db
from lxml import etree

import gzip
import argparse
import sqlite3


def unzip(filename):
    # file_name = 'ec_xml_feed.xml.gz'
    uz_filename = '.'.join(file_name.split('.')[:-1])
    with gzip.open(file_name, 'r') as zipped:
        with open(uz_filename, 'w') as new:
            for line in zipped:
                new.write(line)
    return uz_filename

def fill_database(file_name, is_zip=False):

    if is_zip:
        file_name = unzip(file_name)
    
    context = etree.iterparse(file_name, events=('end',), tag='product')
    id = len(Product.query.all()) + 1
    for event, product in context:
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
        if (id % 100) == 0:
            db.session.commit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Path to file', required=True)
    parser.add_argument('-z', '--zip', help='Is xml zipped')
    args = parser.parse_args()

    is_zip = args.zip
    file_name = args.path
    if file_name:
        fill_database(args.path, args.zip)
    else:
        print 'Please, enter path to file'
