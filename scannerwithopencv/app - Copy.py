import streamlit as st
import cv2
import numpy as np
from PIL import Image
import json
from neo4j import GraphDatabase


st.set_page_config(page_title="QR Code Scanner", page_icon="📷")
st.title(" QR Code Scanner")
st.write("Use your phone or laptop camera to scan a QR code.")

# Use Streamlit camera input
img_file = st.camera_input("Take a photo of a QR code")

if img_file:
    # Read image with PIL and convert to OpenCV format
    img = Image.open(img_file)
    img_np = np.array(img)

    # Detect and decode QR code
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img_np)

    if data:
        st.success(" QR Code Detected!")
        try:
            st.json(json.loads(data))
        except:
            st.write(data)
    else:
        st.error("⚠️ No QR code found in the image.")
