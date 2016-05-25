# coding: utf-8
from __future__ import unicode_literals

from PIL import ImageFont, Image, ImageOps, ImageDraw
import requests
import io


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

def get_font(size, bold=False):
    if bold:
        font_path = './static/DejaVuSans-Bold.ttf'
    else:
        font_path = './static/DejaVuSans.ttf'
    return ImageFont.truetype(font_path, size)

def load_image(url):
    fd = requests.get(url)
    image_file = io.BytesIO(fd.content)
    return Image.open(image_file, 'r')

def resize_image(img, output_size):
    img.thumbnail(output_size, Image.ANTIALIAS)

def generate_action_item():
    action_img = Image.new('RGBA', (120, 30), (255, 255, 255, 255))
    img_w, img_h = action_img.size
    small_font = get_font(16)
    action_font = get_font(16)
    text_offset = (5, 5)
    draw = ImageDraw.Draw(action_img)
    draw.text(text_offset, 'COMPRA YA >', 'black', small_font)
    action_with_border = ImageOps.expand(action_img, border=2, fill='black')
    return action_with_border
   
def generate_image(image_url, price, product_title, free_shipping, loyality_programm, output_size, pricespecial=0):
    print output_size
    if not output_size:
        output_size = (340, 340)

    price_to_print = '{}$'.format(price)
    new_price_to_print = '{}$'.format(pricespecial)
    
    img = load_image(image_url)
    image_size = (int(0.6*output_size[0]), int(0.6*output_size[0]))
    resize_image(img, image_size)
    img_w, img_h = img.size
    
    background = Image.new('RGBA', output_size, (255, 255, 255, 255))
    bg_w, bg_h = output_size
    offset = (int((bg_w-img_w)/2), int(0.05*bg_h))
    
    background.paste(img, offset)

    draw = ImageDraw.Draw(background)
    small_font = get_font(16)
    large_font = get_font(22)
    plus_font = get_font(22, bold=True)

    title_offset = (int(0.1*bg_w), int(1.2*img_h))
    previous_price_offset = (title_offset[0], title_offset[1] + 20)
    new_price_offset = (title_offset[0], previous_price_offset[1] + 30)
    
    new_title = cut_title(product_title, small_font, int(0.85*output_size[0]))
    draw.text(title_offset, new_title, 'black', font=small_font)

    if pricespecial > 0:
        draw.text(previous_price_offset, strike(str(price_to_print)), 'grey', font=small_font)
        draw.text(new_price_offset, str(new_price_to_print), 'red', font=large_font)
    else:
        draw.text(new_price_offset, str(price_to_print), 'red', font=large_font)

    free_shipping_offset = (0.9*bg_w-large_font.getsize('Envío gratis')[0], new_price_offset[1])
    loyality_offset = (0.9*bg_w-large_font.getsize('plus')[0], free_shipping_offset[1]-30)

    if loyality_programm and free_shipping:
        draw.text(free_shipping_offset, 'Envío gratis', 'green', font=large_font)
        draw.text(loyality_offset, 'plus', 'orange', font=large_font)
    elif loyality_programm:
        draw.text(loyality_offset, 'plus', 'orange', font=large_font)
    elif free_shipping:
        draw.text(free_shipping_offset, 'Envío gratis', 'green', font=large_font)
    action_item = generate_action_item()
    background.paste(action_item, (title_offset[0], new_price_offset[1] + 40))
    return background
