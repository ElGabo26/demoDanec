import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Agente Revisor EPN", layout="wide")

st.title("🤖 Agente Revisor de Solicitudes de Auspicio DANEC")
st.markdown("---")

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración del Trámite")
    tipo_tramite = st.selectbox(
        "Seleccione el tipo de trámite:",
        ["Pago de inscripción", "Viáticos y pasajes", "Salida exterior fuera de proyecto"]
    )

# Área de carga de archivos
st.subheader("1. Carga de Documentación")
uploaded_files = st.file_uploader(
    "Arrastre sus documentos o fotos aquí", 
    accept_multiple_files=True,
    type=['pdf', 'docx', 'xlsx', 'png', 'jpg']
)

# Botón de Acción
if st.button("Analizar Documentación", type="primary"):
    if not uploaded_files:
        st.warning("Por favor, suba al menos un archivo para analizar.")
    else:
        with st.spinner('El agente está leyendo y cruzando información de los documentos...'):
            try:
                # Preparar archivos para enviar al backend
                files_payload = []
                for f in uploaded_files:
                    files_payload.append(('files', (f.name, f.getvalue(), f.type)))
                
                data_payload = {'tramite': tipo_tramite}
                
                # Enviar al Backend
                response = requests.post(
                    "http://127.0.0.1:5000/analizar", 
                    files=files_payload, 
                    data=data_payload
                )
                
                if response.status_code == 200:
                    st.success("Análisis completado")
                    resultado = response.json().get("resultado", "Sin respuesta")
                    
                    # Mostrar Resultados
                    st.subheader("2. Diagnóstico del Agente")
                    st.markdown(resultado)
                else:
                    st.error(f"Error en el servidor: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("No se pudo conectar con el Backend. Asegúrate de ejecutar 'python backend.py'.")

# Ejecutar: °streamlit run frontend.py