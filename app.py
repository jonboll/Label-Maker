import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def create_label(order_num, item_count, material, design_name):
    # 1. Setup Dimensions for 1 inch tall at 300 DPI
    # Width: 3 inches (900px), Height: 1 inch (300px)
    dpi = 300
    width = 3 * dpi
    height = 1 * dpi
    
    # 2. Create QR Code with Order Data
    # Including the order number inside the QR data
    qr_data = f"ORDER:{order_num}|ITEM:{item_count}|DESIGN:{design_name}"
    qr = qrcode.QRCode(version=1, box_size=10, border=0)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Resize QR to fit comfortably in the 1-inch height (e.g., 240x240 px)
    qr_side = int(height * 0.8)
    qr_img = qr_img.resize((qr_side, qr_side))
    
    # 3. Create Canvas
    background = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(background)
    
    # Paste QR Code (centered vertically)
    margin = int((height - qr_side) / 2)
    background.paste(qr_img, (margin, margin))
    
    # 4. Text Configuration
    # Using a larger font size for 300 DPI clarity
    try:
        # If running locally, you can specify a path to a font file
        font_main = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 32)
    except:
        font_main = ImageFont.load_default()
        font_small = ImageFont.load_default()

    text_x = qr_side + (margin * 2)
    
    # Drawing the text
    draw.text((text_x, 50), f"ORDER #: {order_num}", fill="black", font=font_main)
    draw.text((text_x, 110), f"ITEM: {item_count}", fill="black", font=font_small)
    draw.text((text_x, 160), material, fill="black", font=font_small)
    draw.text((text_x, 210), f"DESIGN: {design_name}", fill="black", font=font_small)
    
    return background

# --- STREAMLIT UI ---
st.title("📏 1-Inch Label Generator")

order_id = st.text_input("Order Number", "211720")
items = st.text_input("Item Count", "1 of 1")
mat = st.text_input("Material", "Linen Cotton Canvas")
design = st.text_input("Design Name", "Sweetgrass Final PNG")

if st.button("Generate 1x3 Label"):
    img = create_label(order_id, items, mat, design)
    st.image(img, caption="Preview (300 DPI)", use_container_width=True)
    
    buf = io.BytesIO()
    img.save(buf, format="PNG", dpi=(300, 300)) # Saves DPI info in metadata
    
    st.download_button(
        label="Download Label",
        data=buf.getvalue(),
        file_name=f"Label_{order_id}.png",
        mime="image/png"
    )
