import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def draw_bold_text(draw, position, text, font, fill=0):
    """Draws text multiple times slightly offset to simulate a heavy bold effect."""
    x, y = position
    # Draw the text 3 times with 1-pixel offsets for a 'thick' look
    for adj in range(3):
        draw.text((x + adj, y), text, fill=fill, font=font)
        draw.text((x, y + adj), text, fill=fill, font=font)

def create_label(order_num, item_count, material, design_name):
    # 300 DPI: 1 inch = 300px height. 4.5 inches = 1350px width.
    width, height = 1350, 300  
    
    # 1. QR CODE
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(order_num)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('L')
    qr_side = 280 
    qr_img = qr_img.resize((qr_side, qr_side), resample=Image.NEAREST)
    
    # 2. CANVAS
    background = Image.new('L', (width, height), color=255)
    background.paste(qr_img, (10, 10))
    draw = ImageDraw.Draw(background)
    
    # 3. FONT SIZING
    # We use a very large default size. 
    # Even if the 'path' fails, the default font will now be scaled up.
    try:
        # Standard Linux path for a bold font
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        font_main = ImageFont.truetype(font_path, 70) # Massive Order #
        font_sub = ImageFont.truetype(font_path, 48)  # Large Details
    except:
        font_main = ImageFont.load_default(size=60)
        font_sub = ImageFont.load_default(size=40)

    # 4. DRAW TEXT (Using the Bold trick)
    text_x = 340
    
    # Drawing each line with our 'Bold' helper function
    draw_bold_text(draw, (text_x, 30), f"ORDER #: {order_num}", font_main)
    draw_bold_text(draw, (text_x, 110), f"ITEM: {item_count}", font_sub)
    draw_bold_text(draw, (text_x, 175), f"MAT: {material}", font_sub)
    draw_bold_text(draw, (text_x, 235), f"DESIGN: {design_name}", font_sub)
    
    return background.convert('RGB')

# --- STREAMLIT UI ---
st.set_page_config(page_title="Ultra Bold Label Maker")
st.title("🏷️ Ultra-Bold 1-Inch Labels")

order_id = st.text_input("Order Number", "211720")
items = st.text_input("Item Count", "1 of 1")
mat = st.text_input("Material", "Linen Cotton Canvas")
design = st.text_input("Design Name", "Sweetgrass Final PNG")

if st.button("Generate Bold Label"):
    img = create_label(order_id, items, mat, design)
    st.image(img, caption="Preview: 1 inch tall at 300 DPI", use_container_width=True)
    
    buf = io.BytesIO()
    img.save(buf, format="PNG", dpi=(300, 300))
    st.download_button("Download High-Res Label", buf.getvalue(), f"Label_{order_id}.png", "image/png")
