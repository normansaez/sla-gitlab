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


# Título del formulario
st.title(GITLAB_TOKEN)


