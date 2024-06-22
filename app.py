import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
GITLAB_PROJECT_ID = os.getenv('GITLAB_PROJECT_ID')
GITLAB_API_URL = os.getenv('GITLAB_API_URL')
GITLAB_BASE_URL = os.getenv('GITLAB_BASE_URL')

if not GITLAB_TOKEN or not GITLAB_PROJECT_ID or not GITLAB_API_URL or not GITLAB_BASE_URL:
    st.error("Una o más variables de entorno no están configuradas correctamente.")
    st.stop()

# Función para obtener issues de GitLab con paginación
def get_issues():
    headers = {
        'Private-Token': GITLAB_TOKEN
    }
    issues = []
    page = 1
    
    while True:
        url = f"{GITLAB_API_URL}/projects/{GITLAB_PROJECT_ID}/issues?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            page_issues = response.json()
            if not page_issues:
                break
            issues.extend(page_issues)
            page += 1
        else:
            st.error(f"Error al obtener issues: {response.status_code}")
            break

    return issues

# Función para obtener las notas de un issue con paginación
def get_issue_notes(issue_iid):
    headers = {
        'Private-Token': GITLAB_TOKEN
    }
    notes = []
    page = 1
    
    while True:
        url = f"{GITLAB_API_URL}/projects/{GITLAB_PROJECT_ID}/issues/{issue_iid}/notes?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            page_notes = response.json()
            if not page_notes:
                break
            notes.extend(page_notes)
            page += 1
        else:
            st.error(f"Error al obtener notas del issue {issue_iid}: {response.status_code}")
            break
    
    # Ordenar las notas por fecha de creación para asegurar que la última nota es la correcta
    notes.sort(key=lambda x: x['created_at'])
    return notes

# Función para mostrar los issues abiertos con el autor del último comentario y el último asignado
def show_open_issues_with_details(issues):
    open_issues = [issue for issue in issues if issue['state'] == 'opened']
    
    if open_issues:
        st.write("Tickets abiertos:")
        for issue in open_issues:
            issue_url = f"{GITLAB_BASE_URL}/-/issues/{issue['iid']}"
            notes = get_issue_notes(issue['iid'])
            last_comment_author = notes[-1]['author']['name'] if notes else 'Sin comentarios'
            last_assignee = issue['assignee']['name'] if issue['assignee'] else 'No asignado'
            st.write(f"- {issue['title']} (IID: {issue['iid']}) Último comentario por: {last_comment_author} Último asignado a: {last_assignee}")
            st.write(f"[Ver Issue]({issue_url})")
    else:
        st.write("No hay tickets abiertos.")

# Interfaz de usuario de Streamlit
st.title("Gestión de Issues en GitLab")

if st.button("Cargar Issues"):
    issues = get_issues()
    show_open_issues_with_details(issues)

