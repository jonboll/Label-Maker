import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def create_label(order_num, item_count, material, design_name):
    # 1. Dimensions for 1 inch tall at 300 DPI
    # Width 4 inches (1200px) gives more room for long design names
    dpi = 300
    width = 4 * dpi 
    height = 1 * dpi
    
    # 2. Generate QR Code with "Nearest Neighbor" scaling for sharpness
    # This is the "Usable Data" fix:
    qr_data = f"ORDER:{order_num}\nITEM:{item_count}\nDESIGN:{design_name}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L, # High readability
        box_size=10,
        border=1,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create the QR image - keeping it strictly Black and White
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Resize using NEAREST to keep the squares sharp (Prevents "No Data" errors)
    qr_side = int(height * 0.9)
    qr_img = qr_img.resize((qr_side, qr_side), resample=Image.NEAREST)
    
    # 3. Create Canvas
    background = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(background)
    
    # Paste QR Code with a small left margin
    background.paste(qr_img, (20, int((height - qr_side) / 2)))
    
    # 4. Text - Simplified for basic system fonts
    text_x = qr_side + 60
    
    # Draw text with specific spacing
    draw.text((text_x, 40), f"ORDER #: {order_num}", fill="black")
    draw.text((text_x, 100), f"ITEM: {item_count}", fill="black")
    draw.text((text_x, 160), f"MAT: {material}", fill="black")
    draw.text((text_x, 220), f"DESIGN: {design_name}", fill="black")
    
    return background

# --- STREAMLIT UI ---
st.set_page_config(page_title="Label Maker Pro")
st.title("🏷️ 1-Inch Label Generator")

order_id = st.text_input("Order Number", "211720")
items = st.text_input("Item Count", "1 of 1")
mat = st.text_input("Material", "Linen Cotton Canvas")
design = st.text_input("Design Name", "Sweetgrass Final PNG")

if st.button("Generate & Test QR"):
    img = create_label(order_id, items, mat, design)
    
    # Display the result
    st.image(img, caption="Ensure QR is sharp and not blurry", use_container_width=True)
    
    # Save to buffer
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    
    st.download_button(
        label="Download Label",
        data=buf.getvalue(),
        file_name=f"Label_{order_id}.png",
        mime="image/png"
    )
