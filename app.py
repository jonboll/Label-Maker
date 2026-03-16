import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import os

def create_label(order_num, item_count, material, design_name):
    dpi = 300
    width = 1200  # 4 inches
    height = 300  # 1 inch
    
    # 1. GENERATE QR CODE
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2, # Slightly smaller border to allow for larger QR/Text
    )
    qr.add_data(order_num)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('L')
    
    # Resize QR to fill most of the height
    qr_side = 260 
    qr_img = qr_img.resize((qr_side, qr_side), resample=Image.NEAREST)
    
    # 2. CREATE CANVAS
    background = Image.new('L', (width, height), color=255)
    background.paste(qr_img, (20, 20))
    
    draw = ImageDraw.Draw(background)
    
    # 3. LOAD FONT (Falls back to default if font file is missing)
    font_path = "arialbd.ttf" # Ensure this file is in your GitHub repo!
    if os.path.exists(font_path):
        font_main = ImageFont.truetype(font_path, 55)   # Large for Order #
        font_sub = ImageFont.truetype(font_path, 42)    # Medium for details
    else:
        st.warning("Font file 'arialbd.ttf' not found. Using default tiny font.")
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 4. DRAW TEXT WITH TIGHT SPACING
    text_x = 320
    # Vertical positions adjusted to maximize the 300px height
    draw.text((text_x, 30), f"ORDER #: {order_num}", fill=0, font=font_main)
    draw.text((text_x, 100), f"ITEM: {item_count}", fill=0, font=font_sub)
    draw.text((text_x, 160), f"MAT: {material}", fill=0, font=font_sub)
    draw.text((text_x, 220), f"DESIGN: {design_name}", fill=0, font=font_sub)
    
    return background.convert('RGB')

# --- STREAMLIT UI ---
