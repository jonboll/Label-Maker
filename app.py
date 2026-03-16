import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def create_label(order_num, item_count, material, design_name):
    # 300 DPI: 1 inch = 300px height
    width, height = 1200, 300  
    
    # 1. QR CODE GENERATION
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
    
    # 3. SMART FONT LOADER
    # These are standard Bold fonts found on Linux (Streamlit) servers
    linux_fonts = [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]
    
    font_main = None
    for path in linux_fonts:
        try:
            font_main = ImageFont.truetype(path, 60)
            font_sub = ImageFont.truetype(path, 42)
            break
        except:
            continue
            
    # Absolute Fallback if Linux fonts fail
    if font_main is None:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 4. DRAW TEXT
    text_x = 340
    draw.text((text_x, 35), f"ORDER #: {order_num}", fill=0, font=font_main)
    draw.text((text_x, 105), f"ITEM: {item_count}", fill=0, font=font_sub)
    draw.text((text_x, 165), f"MAT: {material}", fill=0, font=font_sub)
    draw.text((text_x, 225), f"DESIGN: {design_name}", fill=0, font=font_sub)
    
    return background.convert('RGB')

# --- STREAMLIT UI ---
st.set_page_config(page_title="Bold Label Maker")
st.title("🏷️ Bold 1-Inch Label Generator")

order_id = st.text_input("Order Number", "211720")
items = st.text_input("Item Count", "1 of 1")
mat = st.text_input("Material", "Linen Cotton Canvas")
design = st.text_input("Design Name", "Sweetgrass Final PNG")

if st.button("Generate Bold Label"):
    img = create_label(order_id, items, mat, design)
    st.image(img, caption="Preview (1 inch tall)", use_container_width=True)
    
    buf = io.BytesIO()
    img.save(buf, format="PNG", dpi=(300, 300))
    st.download_button("Download High-Res Label", buf.getvalue(), f"Label_{order_id}.png", "image/png")
