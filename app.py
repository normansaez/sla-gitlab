import streamlit as st
import requests
import os
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime

load_dotenv()

GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
GITLAB_PROJECT_ID = os.getenv('GITLAB_PROJECT_ID')
GITLAB_API_URL = os.getenv('GITLAB_API_URL')
GITLAB_BASE_URL = os.getenv('GITLAB_BASE_URL')

if not GITLAB_TOKEN or not GITLAB_PROJECT_ID or not GITLAB_API_URL or not GITLAB_BASE_URL:
    raise ValueError("Una o más variables de entorno no están configuradas correctamente.")

import subprocess

# Botón para ejecutar el script
if st.button("Ejecutar Script"):
    result = subprocess.run(["python", "tickets_abiertos.py"], capture_output=True, text=True)
    
    # Mostrar salida y errores
    st.write("Salida del Script:")
    st.text(result.stdout)
    if result.stderr:
        st.error("Errores del Script:")
        st.text(result.stderr)
    else:
        st.success("Script ejecutado con éxito")

