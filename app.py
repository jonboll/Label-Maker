import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def create_label(order_num, item_count, material, design_name):
    # 600 DPI Resolution
    scale_factor = 2 
    width, height = 1350 * scale_factor, 300 * scale_factor  
    
    # --- COLOR DEFINITIONS ---
    sage_green = (136, 154, 137)  # #889a89 for the QR
    pure_black = (0, 0, 0)        # For the Text
    
    # 1. QR CODE (Sage Green)
    qr = qrcode.QRCode(version=1, box_size=20, border=4)
    qr.add_data(order_num)
    qr.make(fit=True)
    
    # Apply green only here
    qr_img = qr.make_image(fill_color=sage_green, back_color="white").convert('RGB')
    
    qr_side = 560 
    qr_img = qr_img.resize((qr_side, qr_side), resample=Image.LANCZOS)
    
    # 2. CANVAS
    background = Image.new('RGB', (width, height), color=(255, 255, 255))
    background.paste(qr_img, (20, 20))
    draw = ImageDraw.Draw(background)
    
    # 3. FONTS
    try:
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        font_main = ImageFont.truetype(font_path, 140)
        font_sub = ImageFont.truetype(font_path, 90)
    except:
        font_main = ImageFont.load_default(size=120)
        font_sub = ImageFont.load_default(size=80)

    # 4. DRAW TEXT (Black)
    text_x = 700
    # We explicitly set fill to pure_black here
    draw.text((text_x, 60), f"ORDER #: {order_num}", fill=pure_black, font=font_main)
    draw.text((text_x, 210), f"ITEM: {item_count}", fill=pure_black, font=font_sub)
    draw.text((text_x, 330), f"MAT: {material}", fill=pure_black, font=font_sub)
    draw.text((text_x, 450), f"DESIGN: {design_name}", fill=pure_black, font=font_sub)
    
    return background


# --- STREAMLIT UI ---
# This changes the name in the browser tab
st.set_page_config(page_title="Custom Label Creator", layout="centered")

# This changes the big title at the top of the webpage
st.title("🏷️ Custom Label Creator") 
st.write("One inch tall label")

order_id = st.text_input("Order Number", "211720")
items = st.text_input("Item Count", "1 of 1")
mat = st.text_input("Material", "Linen Cotton Canvas")
design = st.text_input("Design Name", "Sweetgrass Final PNG")

if st.button("Generate High-Res Label"):
    img = create_label(order_id, items, mat, design)
    
    # The preview will look large, so we cap the display width
    st.image(img, caption="High-Resolution Preview", width=800)
    
    buf = io.BytesIO()
    # Saving with 600 DPI metadata
    img.save(buf, format="PNG", dpi=(600, 600))
    
    # Ensure this is indented exactly the same as the 'buf' lines above
    st.download_button(
        label="Download 600 DPI Label",
        data=buf.getvalue(),
        file_name=f"{order_id}_code.png",
        mime="image/png"
    )
