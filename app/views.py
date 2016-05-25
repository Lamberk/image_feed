# coding: utf-8
from __future__ import unicode_literals

from app import app, db
from app.models import Product
from app.helpers import generate_image

import random  

from flask import Flask, send_file
from StringIO import StringIO


def serve_image(img):
    img_io = StringIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/api/get_image/random/', methods=['GET'])
def get_rand_image():
    rand = random.randrange(0, db.session.query(Product).count())   
    sku = db.session.query(Product)[rand].sku
    return get_image(sku)

@app.route('/api/get_image/<string:sku>/', methods=['GET'])
def get_image(sku):
    product = Product.query.filter_by(sku=sku).first()
    img = generate_image(
        loyality_programm = product.loyality_programm,
        free_shipping = product.free_shipping,
        image_url = product.image_url,
        product_title = product.product_title,
        price = product.price,
        pricespecial = product.pricespecial,
    )
    return serve_image(img)
