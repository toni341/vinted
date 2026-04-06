import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
import io

st.set_page_config(page_title="VANTAGE AI", page_icon="⚡")
st.title("⚡ VANTAGE AI")
st.write("Sveglia! Trasforma le tue foto in scatti da showroom.")

uploaded_file = st.file_uploader("Trascina qui la foto...", type=['jpg','png','jpeg','jfif'])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGBA")
    with st.spinner("L'intelligenza artificiale sta lavorando..."):
        # Rimozione sfondo
        no_bg = remove(img)
        # Ombra reale per profondità
        shadow = Image.new("RGBA", no_bg.size, (0,0,0,0))
        mask = no_bg.split()[-1].point(lambda x: 75 if x > 0 else 0)
        shadow.putalpha(mask)
        shadow = shadow.filter(ImageFilter.GaussianBlur(15))
        # Sfondo Grigio professionale
        bg = Image.new("RGBA", no_bg.size, (215, 215, 215))
        # Unione
        final = Image.alpha_composite(bg, shadow)
        final = Image.alpha_composite(final, no_bg).convert("RGB")
        
        st.image(final, caption="Foto pronta per Vinted", use_container_width=True)
        buf = io.BytesIO()
        final.save(buf, format="JPEG", quality=95)
        st.download_button("📥 SCARICA ORA", buf.getvalue(), "vantage_pro.jpg", "image/jpeg")
