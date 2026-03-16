import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

# --- LABEL GENERATOR ENGINE ---
def create_label(order_num, item_count, material, design_name):
    qr_content = f"Order: {order_num} | Design: {design_name}"
    qr = qrcode.QRCode(version=1, box_size=10, border=0)
    qr.add_data(qr_content)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    width, height = 800, 220
    background = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(background)
    
    qr_img = qr_img.resize((160, 160))
    background.paste(qr_img, (20, 30))
    
    # Use default font for cloud compatibility
    font = ImageFont.load_default()
    
    text_x = 200
    lines = [f"Order #: {order_num}", f"Item {item_count}", material, f"Design: {design_name}"]
    
    y_offset = 40
    for line in lines:
        draw.text((text_x, y_offset), line, fill=(0, 0, 0), font=font)
        y_offset += 35
    
    return background

# --- STREAMLIT INTERFACE ---
st.title("🏷️ Label Generator")
st.write("Fill in the details below to create your label.")

col1, col2 = st.columns(2)

with col1:
    order_id = st.text_input("Order Number", "211720")
    items = st.text_input("Item Count", "1 of 1")

with col2:
    mat = st.text_input("Material", "Linen Cotton Canvas")
    design = st.text_input("Design Name", "Sweetgrass Final PNG")

if st.button("Generate Label"):
    img = create_label(order_id, items, mat, design)
    
    # Show preview in the app
    st.image(img, caption="Preview", use_container_width=True)
    
    # Prepare for download
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Download Label Image",
        data=byte_im,
        file_name=f"Label_{order_id}.png",
        mime="image/png"
    )
