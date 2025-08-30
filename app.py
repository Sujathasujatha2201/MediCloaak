import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
from cryptography.fernet import Fernet
import base64
import io

# Generate or load key
if "key" not in st.session_state:
    st.session_state.key = Fernet.generate_key()
cipher_suite = Fernet(st.session_state.key)

st.title("🔐 MediCloak - Secure Medical Files")

st.write("Upload a *PDF* or *Image*, encrypt/decrypt it securely.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])

action = st.radio("Select action", ["Encrypt", "Decrypt"])

if uploaded_file:
    file_bytes = uploaded_file.read()

    if action == "Encrypt":
        encrypted_data = cipher_suite.encrypt(file_bytes)
        st.success("File encrypted successfully!")
        
        # Download encrypted file
        b64 = base64.b64encode(encrypted_data).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="encrypted.txt">Download Encrypted File</a>'
        st.markdown(href, unsafe_allow_html=True)

    elif action == "Decrypt":
        try:
            decrypted_data = cipher_suite.decrypt(file_bytes)
            st.success("File descrypted successfully!")
            
            # Display file if it's an image
            try:
                img = Image.open(io.BytesIO(decrypted_data))
                st.image(img, caption="Decrypted Image")
            except:
                st.download_button("Download Decrypted File", decrypted_data, file_name="decrypted_file")
        except:
            st.error("Invalid file or wrong key!")