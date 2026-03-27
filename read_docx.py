import docx

doc = docx.Document(r"c:\Users\Usuario\Documents\Github\Entropía\Referees\guia_prompts_revision.docx")
with open("doc_content.txt", "w", encoding="utf-8") as f:
    for para in doc.paragraphs:
        if para.text.strip():
            f.write(para.text + "\n")
