import docx
import io

def convert_docx_to_txt(input_path, output_path):
    doc = docx.Document(input_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        for para in doc.paragraphs:
            f.write(para.text + '\n')

if __name__ == "__main__":
    convert_docx_to_txt(r'C:\Users\Usuario\Documents\Github\Entropía\Referees\guia_prompts_ronda2.docx', 
                        r'C:\Users\Usuario\Documents\Github\Entropía\Referees\guia_prompts_ronda2.txt')
    print("DONE")
