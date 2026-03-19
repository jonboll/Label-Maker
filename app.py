import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def create_label(order_num, item_count, material, design_name):
    # --- RESOLUTION & DIMENSIONS ---
    scale_factor = 2 
    width, height = 1350 * scale_factor, 300 * scale_factor  
    
    # --- COLOR DEFINITIONS ---
    # New Blue Color: #839eb9 -> (131, 158, 185)
    custom_blue = (131, 158, 185)  
    pure_black = (0, 0, 0)        
    
    # 1. QR CODE GENERATION (Now using the blue color)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=20,
        border=4, 
    )
    qr.add_data(order_num)
    qr.make(fit=True)
    
    # Apply the blue color to the fill_color parameter
    qr_img = qr.make_image(fill_color=custom_blue, back_color="white").convert('RGB')
    
    qr_side = 560 
    qr_img = qr_img.resize((qr_side, qr_side), resample=Image.LANCZOS)
    
    # 2. CANVAS CREATION
    background = Image.new('RGB', (width, height), color=(255, 255, 255))
    background.paste(qr_img, (20, 20))
    draw = ImageDraw.Draw(background)
    
    # 3. SMART FONT LOADING
    try:
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        font_main = ImageFont.truetype(font_path, 140)
        font_sub = ImageFont.truetype(font_path, 90)
    except:
        font_main = ImageFont.load_default(size=120)
        font_sub = ImageFont.load_default(size=80)

    # 4. DRAW TEXT (Pure Black)
    text_x = 700
    draw.text((text_x, 60), f"ORDER #: {order_num}", fill=pure_black, font=font_main)
    draw.text((text_x, 210), f"ITEM: {item_count}", fill=pure_black, font=font_sub)
    draw.text((text_x, 330), f"MAT: {material}", fill=pure_black, font=font_sub)
    draw.text((text_x, 450), f"DESIGN: {design_name}", fill=pure_black, font=font_sub)
    
    return background


# --- STREAMLIT UI ---
# This changes the name in the browser tab
st.set_page_config(page_title="Manual Label Creator", layout="centered")

# This changes the big title at the top of the webpage
st.title("🏷️ Manual Label Creator") 
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
