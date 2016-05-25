# coding: utf-8
from __future__ import unicode_literals

from app import app, db
from app.models import Product

from PIL import ImageFont, Image, ImageOps, ImageDraw
import requests
import xml.etree.ElementTree as ET
import io
import random  
import time

from flask import Flask, send_file
from StringIO import StringIO


def cut_title(title, font, max_pixel):
    dots_pixels = font.getsize('...')[0]
    positions = []
    curr = 0
    for n, c in enumerate(title):
        curr += font.getsize(c)[0]
        if curr > max_pixel - dots_pixels:
            return title[:n]+'...'
    return title

def strike(text):
    result = ''
    for c in text:
        result += c + '\u0336'
    result += ' '
    return result

def load_image(url):
    fd = requests.get('https://www.google.ru/images/nav_logo242.png')
    image_file = io.BytesIO(fd.content)
    return Image.open(image_file, 'r')

def resize_image(img, output_size):
    img.thumbnail(output_size, Image.ANTIALIAS)

def generate_action_item():
    action_img = Image.new('RGBA', (120, 30), (255, 255, 255, 255))
    img_w, img_h = action_img.size
    small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    action_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    text_offset = (5, 5)
    draw = ImageDraw.Draw(action_img)
    draw.text(text_offset, 'COMPRA YA >', 'black', small_font)
    action_with_border = ImageOps.expand(action_img, border=2, fill='black')
    return action_with_border
   
def generate_image(image_url, price, product_title, free_shipping, loyality_programm, pricespecial=0, output_size=(340,340)):
    
    price_to_print = '{}$'.format(price)
    new_price_to_print = '{}$'.format(pricespecial)
    
    img = load_image(image_url)
    resize_image(img, output_size)
    img_w, img_h = img.size
    
    background = Image.new('RGBA', (int(1.2*img_w), int(1.6*img_h)), (255, 255, 255, 255))
    bg_w, bg_h = background.size
    offset = (int(0.1*bg_w), int(0.05*bg_h))
    
    background.paste(img, offset)

    draw = ImageDraw.Draw(background)
    small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    large_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
    plus_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)

    title_offset = (int(0.1*img_w), int(1.2*img_h))
    previous_price_offset = (title_offset[0], title_offset[1] + 20)
    new_price_offset = (title_offset[0], previous_price_offset[1] + 20)
    
    new_title = cut_title(product_title, small_font, output_size[0])
    draw.text(title_offset, new_title, 'black', font=small_font)

    if pricespecial > 0:
        previous_price_offset = (title_offset[0], title_offset[1] + 20)
        new_price_offset = (title_offset[0], previous_price_offset[1] + 20)
        draw.text(previous_price_offset, strike(str(price_to_print)), 'grey', font=small_font)
        draw.text(new_price_offset, str(new_price_to_print), 'red', font=large_font)
    else:
        new_price_offset = (title_offset[0], title_offset[1] + 20)
        draw.text(new_price_offset, str(price_to_print), 'red', font=large_font)

    free_shipping_offset = (title_offset[0] + img_w - 120, title_offset[1] + 50)
    loyality_offset = (title_offset[0] + img_w - 35, title_offset[1] + 20)
    mix_offset = (free_shipping_offset[0], loyality_offset[1])

    if loyality_programm and free_shipping:
        draw.text(free_shipping_offset, 'Envío gratis', 'green', font=large_font)
        draw.text(loyality_offset, 'plus', 'orange', font=large_font)
    elif loyality_programm:
        draw.text(loyality_offset, 'plus', 'orange', font=large_font)
    elif free_shipping:
        draw.text(mix_offset, 'Envío gratis', 'green', font=large_font)
    action_item = generate_action_item()
    background.paste(action_item, (title_offset[0], new_price_offset[1] + 40))
    return background

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
