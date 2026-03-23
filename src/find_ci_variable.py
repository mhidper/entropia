import nbformat
import ast

def find_variables():
    with open(r'C:\Users\Usuario\Documents\Github\Entropía\src\risk index.ipynb', 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    codes = [c.source for c in nb.cells if c.cell_type == 'code']
    
    with open(r'C:\Users\Usuario\Documents\Github\Entropía\src\ci_vars.txt', 'w', encoding='utf-8') as out:
        # Search backward for plots of the index
        for i in range(len(codes)-1, -1, -1):
            code = codes[i]
            if 'plot(' in code and ('composite' in code.lower() or 'index' in code.lower() or 'incertidumbre' in code.lower()):
                out.write(f"--- Cell {i} ---\n")
                lines = code.split('\n')
                for line in lines:
                    if 'plot' in line or 'Index' in line or 'index' in line or '=' in line:
                        out.write(line + '\n')

find_variables()
