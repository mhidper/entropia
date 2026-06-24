import os
import re
from pypdf import PdfReader

BIB_FILE = r'risk_analysis/paper_tex/bib.bib'
MAIN_TEX = r'risk_analysis/paper_tex/main.tex'
PDF_DIR = r'risk_analysis/bibliografía'
OUTPUT_FILE = r'risk_analysis/audit_bibliografia_report.md'

class SimpleBibParser:
    @staticmethod
    def parse(file_path):
        entries = []
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Find entries like @type{id, body}
        raw_entries = re.findall(r'@(\w+)\{([^,]+),\s*(.*?)\n\}', content, re.DOTALL)
        for e_type, e_id, e_body in raw_entries:
            entry = {'TYPE': e_type.strip(), 'ID': e_id.strip()}
            fields = re.findall(r'(\w+)\s*=\s*\{([^}]*)\}', e_body)
            for k, v in fields:
                entry[k.lower()] = v.strip()
            entries.append(entry)
        return entries

class BibAuditAgent:
    def __init__(self):
        self.bib_entries = []
        self.tex_citations = []
        self.potential_citations = []
        self.audit_results = []
        # Mapping common patterns to keys to help the agent
        self.manual_map = {
            '1-s2.0': 'ghirelli2019',
            'S01651765': 'ghirelli2019',
            'baker_epu': 'baker2016measuring',
            'ssrn-4618392': 'asimakopoulos2023',
            'Pavia': 'pavia2018',
            'Aruoba': 'aruoba2008',
            'Bloom': 'bloomuncer',
            'berge': 'berge2020',
            'carriero': 'carriero2018',
            'clark': 'clark2017',
            'ellsebrg': 'ellsberg1961',
            'knight': 'knight1921',
            'jurado': 'jurado2015',
            'rossi': 'rossi2016',
            'mankiw': 'mankiw1986',
            'orphanides': 'orphanides2001',
            'haussler': 'haussler1997',
            'heskes': 'heskes1998'
        }

    def load_data(self):
        self.bib_entries = SimpleBibParser.parse(BIB_FILE)
        with open(MAIN_TEX, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(r'\\cite[^{]*\{([^}]*)\}', content)
            for m in matches:
                self.tex_citations.extend([k.strip() for k in m.split(',')])

    def match_pdf(self, pdf_name):
        base = pdf_name.lower()
        # Check manual map
        for pattern, key in self.manual_map.items():
            if pattern.lower() in base:
                return next((e for e in self.bib_entries if e['ID'] == key), None)
        # Try direct match
        for e in self.bib_entries:
            if e['ID'].lower() in base:
                return e
        return None

    def audit_pdf(self, pdf_path, filename):
        try:
            reader = PdfReader(pdf_path)
            header = "".join([p.extract_text() for p in reader.pages[:3]])
            footer = "".join([p.extract_text() for p in reader.pages[-10:]])
        except Exception:
            return None, "", ""

        e = self.match_pdf(filename)
        audit = {'pdf': filename, 'key': e['ID'] if e else '---', 'status': 'OK' if e else 'NO LINKED KEY', 'notes': []}
        
        if e:
            # Metadata Consistency Check
            year = e.get('year', '')
            if year and year not in header:
                audit['notes'].append(f"Year mismatch? Bib specifies {year}.")
            author = e.get('author', '').split(',')[0].strip().split(' ')[-1].lower()
            if author and author not in header.lower():
                audit['notes'].append(f"Author '{author}' not prominently in title page.")
            
            # Citation Usage Check
            if e['ID'] not in self.tex_citations:
                audit['status'] = 'UNPUBLISHED CITATION'
                audit['notes'].append("Cited in bib but not found in main.tex.")
        
        return audit, header, footer

    def run(self):
        self.load_data()
        pdfs = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
        
        for p in pdfs:
            audit, header, footer = self.audit_pdf(os.path.join(PDF_DIR, p), p)
            if audit:
                self.audit_results.append(audit)
                
                # Extract Potential Citations
                ref_idx = footer.upper().find("REFERENCES")
                if ref_idx != -1:
                    refs_text = footer[ref_idx:]
                    # Heuristic for bibliography entries in Econ papers
                    cands = re.findall(r'([A-Z][a-z]+, [A-Z].*?\d{4}[^\n]*)', refs_text)
                    for c in cands:
                        if len(c) > 30:
                            # Avoid duplicates from current bib
                            if not any(e['ID'].lower() in c.lower() for e in self.bib_entries):
                                self.potential_citations.append({'from': p, 'ref': c.strip()})
        
        self.report()

    def report(self):
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("# Bibliografía Audit Agent - Informe de Integridad\n\n")
            f.write("Este informe ha sido generado automáticamente para verificar la consistencia entre los archivos físicos y el manuscrito.\n\n")
            
            f.write("## 1. Mapeo de Documentos y Estado de Citación\n")
            f.write("| Archivo PDF | Clave Detectada | Estado | Observaciones |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            for a in self.audit_results:
                obs = "; ".join(a['notes']) if a['notes'] else "-"
                f.write(f"| {a['pdf']} | {a['key']} | {a['status']} | {obs} |\n")
            
            f.write("\n## 2. Sugerencias de Nuevas Referencias (Potenciales)\n")
            f.write("Obras citadas dentro de tu bibliografía actual que podrían fortalecer el marco teórico:\n\n")
            f.write("| PDF Origen | Referencia Candidata |\n")
            f.write("| :--- | :--- |\n")
            seen = set()
            for p in self.potential_citations:
                clean = p['ref'].replace('|', ' ')
                if clean not in seen:
                    f.write(f"| {p['from']} | {clean} |\n")
                    seen.add(clean)

if __name__ == "__main__":
    agent = BibAuditAgent()
    agent.run()
