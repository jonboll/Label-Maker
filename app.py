import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def create_label(order_num, item_count, material, design_name):
    # Higher Resolution: 600 DPI
    # 1 inch = 600px height | 4.5 inches = 2700px width
    scale_factor = 2 
    width, height = 1350 * scale_factor, 300 * scale_factor  
    
    # 1. QR CODE (Increased scale for resolution)
    qr = qrcode.QRCode(version=1, box_size=20, border=4)
    qr.add_data(order_num)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('L')
    
    # Resize QR to fit the new 600px height
    qr_side = 560 
    qr_img = qr_img.resize((qr_side, qr_side), resample=Image.LANCZOS)
    
    # 2. CANVAS (Using 'L' for high-contrast grayscale)
    background = Image.new('L', (width, height), color=255)
    background.paste(qr_img, (20, 20))
    draw = ImageDraw.Draw(background)
    
    # 3. HIGH-RES FONT SIZING
    # We use even larger font sizes because the canvas is now 600px tall
    try:
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        font_main = ImageFont.truetype(font_path, 140) # Double size for high res
        font_sub = ImageFont.truetype(font_path, 90)
    except:
        # If specific font path fails, we use a scaled-up default
        font_main = ImageFont.load_default(size=120)
        font_sub = ImageFont.load_default(size=80)

    # 4. DRAW TEXT
    # At high resolution, we don't need the 'fake bold' trick anymore; 
    # the font naturally looks clean and heavy.
    text_x = 700
    draw.text((text_x, 60), f"ORDER #: {order_num}", fill=0, font=font_main)
    draw.text((text_x, 210), f"ITEM: {item_count}", fill=0, font=font_sub)
    draw.text((text_x, 330), f"MAT: {material}", fill=0, font=font_sub)
    draw.text((text_x, 450), f"DESIGN: {design_name}", fill=0, font=font_sub)
    
    return background.convert('RGB')


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
    # Saving with 600 DPI metadata so printers know it's 1 inch tall
    img.save(buf, format="PNG", dpi=(600, 600))
    
    st.download_button(
        label="Download 600 DPI Label",
        data=buf.getvalue(),
        file_name=f"Label_HighRes_{order_id}.png",
        mime="image/png"
    )
