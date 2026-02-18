import re
from flask import Flask, request, jsonify
from openai import OpenAI 
import pandas as pd
from tools.readDocumentsFlask import get_file_content
from tools.makeContext import limpiar_respuesta_deepseek, build_prompt

app = Flask(__name__)

# --- CONFIGURACIÓN LOCAL (OLLAMA) ---
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

MODELO_LOCAL = "deepseek-r1:7b"


# --- Endpoint Principal ---
@app.route('/analizar', methods=['POST'])
def analizar():
    tramite = request.form.get("tramite", "General")
    archivos = request.files.getlist("files")
    
    contexto_documentos = ""
    for archivo in archivos:
        contexto_documentos += get_file_content(archivo) 

    # Prompt REFORZADO para exigir formato
    system_instruction = build_prompt(contexto_documentos)
    print(system_instruction)
    print(contexto_documentos)
    try:
        response = client.chat.completions.create(
            model=MODELO_LOCAL,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Trámite: {tramite}\n\nDocumentos:\n{contexto_documentos}"}
            ],
            temperature=0.1,
        )
        raw_result = response.choices[0].message.content
        
        # --- APLICAMOS LA LIMPIEZA AQUÍ ---
        resultado_final = limpiar_respuesta_deepseek(raw_result)
        
    except Exception as e:
        resultado_final = f"Error en el servidor local: {str(e)}"

    return jsonify({"resultado": resultado_final})

@app.route('/', methods=['GET'])
def probar_conexion():
    return "✅ Backend operativo"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)