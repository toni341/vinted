import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter
import io

st.set_page_config(page_title="VANTAGE AI", page_icon="⚡")

# Titolo e Stile
st.markdown("<h1 style='text-align: center; color: #000000;'>⚡ VANTAGE AI</h1>", unsafe_allow_html=True)
st.write("---")
st.write("Sveglia! Carica la tua foto e trasformala in uno scatto da showroom.")

# Caricatore file
uploaded_file = st.file_uploader("Scegli una foto...", type=['jpg','jpeg','png','jfif'])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGBA")
    
    with st.spinner("L'IA sta lavorando..."):
        # Processo di rimozione sfondo (Ottimizzato)
        no_bg = remove(img)
        
        # Creazione ombra professionale
        shadow = Image.new("RGBA", no_bg.size, (0,0,0,0))
        mask = no_bg.split()[-1].point(lambda x: 80 if x > 0 else 0)
        shadow.putalpha(mask)
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        
        # Sfondo grigio studio (molto pulito per Vinted)
        bg = Image.new("RGBA", no_bg.size, (235, 235, 235))
        
        # Composizione finale
        combined = Image.alpha_composite(bg, shadow)
        final = Image.alpha_composite(combined, no_bg).convert("RGB")
        
        # Mostra risultato
        st.image(final, use_container_width=True)
        
        # Bottone di Download
        buf = io.BytesIO()
        final.save(buf, format="JPEG", quality=90)
        st.download_button(label="📥 SCARICA FOTO PRO", data=buf.getvalue(), file_name="vantage_pro.jpg", mime="image/jpeg")

st.write("---")
st.caption("Powered by Napoli Power 🐊")
