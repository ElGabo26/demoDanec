import PyPDF2
import docx
import pandas as pd

def extract_text_from_pdf_path(path):
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return f"[Error leyendo PDF: {str(e)}]"


def extract_text_from_docx_path(path):
    try:
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"[Error leyendo DOCX: {str(e)}]"


def extract_text_from_excel_path(path):
    try:
        df = pd.read_excel(path)
        return df.to_string()
    except Exception as e:
        return f"[Error leyendo EXCEL: {str(e)}]"


def get_file_content_from_path(path):
    filename = path.lower()
    content=''
    if filename.endswith(".pdf"):
        content += extract_text_from_pdf_path(path)
    elif filename.endswith(".docx"):
        content += extract_text_from_docx_path(path)
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        content += extract_text_from_excel_path(path)
    else:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content += f.read()
        except Exception as e:
            print(e)
            content += f"[Error leyendo archivo de texto: {str(e)}]"
    return content

if __name__=="__main__":
    root=input('inserte la ruta> ')
    content=get_file_content_from_path(root)
    print(content)