import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def create_label(order_num, item_count, material, design_name):
    dpi = 300
    width = 1200  # 4 inches
    height = 300  # 1 inch
    
    # 1. GENERATE A SIMPLE, BOLD QR CODE
    # We only put the Order Number in here to keep the pattern simple and scannable
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4, # <--- CRITICAL: Provides the white "Quiet Zone" scanners need
    )
    qr.add_data(order_num)
    qr.make(fit=True)
    
    # Create a sharp B&W image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('L')
    
    # Resize QR to fit height perfectly (keeping it square)
    qr_side = 280 
    qr_img = qr_img.resize((qr_side, qr_side), resample=Image.NEAREST)
    
    # 2. CREATE THE CANVAS (High Contrast L mode)
    background = Image.new('L', (width, height), color=255) # 255 is White
    
    # Paste QR with a bit of padding from the left edge
    background.paste(qr_img, (10, 10))
    
    # 3. ADD TEXT
    # We use a built-in PIL font. Note: it may look small; for a professional 
    # look on Streamlit Cloud, you'd eventually want to upload an 'arial.ttf'
    draw = ImageDraw.Draw(background)
    
    text_x = 320
    draw.text((text_x, 50), f"ORDER: {order_num}", fill=0)
    draw.text((text_x, 100), f"ITEM: {item_count}", fill=0)
    draw.text((text_x, 150), f"MAT: {material}", fill=0)
    draw.text((text_x, 200), f"DESIGN: {design_name}", fill=0)
    
    return background.convert('RGB')

# --- STREAMLIT UI ---
st.title("🏷️ 1-Inch QR Label Fix")
st.write("If this doesn't scan, try increasing the 'Order Number' length.")

order_id = st.text_input("Order Number (QR Content)", "211720")
items = st.text_input("Item Count", "1 of 1")
mat = st.text_input("Material", "Linen Cotton Canvas")
design = st.text_input("Design Name", "Sweetgrass Final PNG")

if st.button("Generate Final Label"):
    img = create_label(order_id, items, mat, design)
    st.image(img, caption="Scan this preview with your phone camera", width=600)
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    
    st.download_button("Download Label", buf.getvalue(), f"{order_id}.png", "image/png")
