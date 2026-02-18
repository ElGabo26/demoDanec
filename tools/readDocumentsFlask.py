import PyPDF2
import docx
import pandas as pd


def extract_text_from_pdf(file_stream):
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"[Error leyendo PDF: {str(e)}]"

def extract_text_from_docx(file_stream):
    try:
        doc = docx.Document(file_stream)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"[Error leyendo DOCX: {str(e)}]"

def extract_text_from_excel(file_stream):
    try:
        df = pd.read_excel(file_stream)
        return df.to_string()
    except Exception as e:
        return f"[Error leyendo EXCEL: {str(e)}]"
    
    
def get_file_content(file_storage):
    filename = file_storage.filename.lower()
    content = f"\n--- INICIO ARCHIVO: {file_storage.filename} ---\n"
    
    if filename.endswith('.pdf'):
        content += extract_text_from_pdf(file_storage.stream)
    elif filename.endswith('.docx'):
        content += extract_text_from_docx(file_storage.stream)
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        content += extract_text_from_excel(file_storage.stream)
    else:
        content += str(file_storage.read().decode("utf-8", errors="ignore"))
        
    content += f"\n--- FIN ARCHIVO: {file_storage.filename} ---\n"
    return content
    
if __name__=='__main__':
    pass