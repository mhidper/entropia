#!/usr/bin/env python3
"""
Bibliography Analysis Agent
============================
Analyzes the bibliography of a research paper to:
  1. Extract all references cited in the main paper (main.pdf)
  2. Extract references from each PDF in the bibliography folder
  3. Build a cross-citation network
  4. Identify papers cited by multiple bibliography sources but absent from the main paper
  5. Rank candidates by relevance and produce a structured report

Usage:
    python bibliography_agent.py

Output:
    bibliography_gap_report.md  — full analysis in Markdown
    bibliography_network.json   — raw citation data (optional)

Configuration (edit paths below if needed):
    MAIN_PAPER_PATH  — path to your paper PDF
    BIBLIOGRAPHY_DIR — folder containing the bibliography PDFs
    OUTPUT_DIR       — where to save the report
"""

import os
import re
import json
import pdfplumber
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
SCRIPT_DIR       = Path(__file__).parent
MAIN_PAPER_PATH  = SCRIPT_DIR / "paper_tex" / "main.pdf"
BIBLIOGRAPHY_DIR = SCRIPT_DIR / "bibliografía"
OUTPUT_DIR       = SCRIPT_DIR

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def extract_pdf_text(pdf_path: Path) -> str:
    """Extract all text from a PDF using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"  ⚠ Could not read {pdf_path.name}: {e}")
    return text


def find_references_section(text: str) -> str:
    """Return text starting from the References / Bibliography section."""
    patterns = [
        r'\n\s{0,4}References?\s*\n',
        r'\n\s{0,4}REFERENCES?\s*\n',
        r'\n\s{0,4}Bibliography\s*\n',
        r'\n\s{0,4}BIBLIOGRAPHY\s*\n',
        r'\n\s{0,4}Works Cited\s*\n',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return text[m.start():]
    # Fallback: last ~4000 characters
    return text[-4000:]


def parse_reference_blocks(refs_text: str) -> list:
    """
    Split a references section into individual reference strings.
    Handles the most common academic formats.
    """
    lines = refs_text.split('\n')
    refs = []
    current = []

    def looks_like_ref_start(line):
        """A new reference typically starts with a capital letter / author name."""
        stripped = line.strip()
        if not stripped:
            return False
        # Numbered: [1] or 1.
        if re.match(r'^\[\d{1,3}\]', stripped):
            return True
        if re.match(r'^\d{1,3}\.\s', stripped):
            return True
        # Author-year: starts with capital, has a 4-digit year nearby
        if re.match(r'^[A-ZÁÉÍÓÚÑÜ]', stripped) and re.search(r'\b(19|20)\d{2}\b', stripped):
            return True
        return False

    for line in lines:
        if looks_like_ref_start(line) and current:
            joined = ' '.join(current).strip()
            if len(joined) > 30:
                refs.append(joined)
            current = [line]
        elif line.strip():
            current.append(line)
        else:
            if current:
                joined = ' '.join(current).strip()
                if len(joined) > 30:
                    refs.append(joined)
                current = []

    if current:
        joined = ' '.join(current).strip()
        if len(joined) > 30:
            refs.append(joined)

    return refs


def extract_author_year_title(ref_text: str) -> dict:
    """
    Extract structured data from a reference string.
    Returns dict with keys: raw, first_author, year, title_fragment, key
    """
    result = {"raw": ref_text, "first_author": "", "year": "", "title_fragment": "", "key": ""}

    # Year
    years = re.findall(r'\b(19[5-9]\d|20[0-2]\d)\b', ref_text)
    if years:
        result["year"] = years[0]

    # First author last name
    # Pattern 1: "Smith, J." or "Smith, John"
    m = re.match(r'^(?:\[\d+\]\s*)?([A-ZÁÉÍÓÚÑÜ][a-záéíóúñü\-]+)[\s,\.]', ref_text.strip())
    if m:
        result["first_author"] = m.group(1)
    else:
        # Pattern 2: "J. Smith" or "John Smith"
        m2 = re.match(r'^[A-Z]\.\s+([A-ZÁÉÍÓÚÑÜ][a-záéíóúñü\-]+)', ref_text.strip())
        if m2:
            result["first_author"] = m2.group(1)

    # Title fragment (first 60 chars after year or after author block)
    if result["year"]:
        idx = ref_text.find(result["year"])
        title_start = ref_text[idx + 4:].strip().lstrip('.').strip()
        result["title_fragment"] = title_start[:80]

    # Normalized key for matching: lowercase_author + year
    a = result["first_author"].lower()
    y = result["year"]
    result["key"] = f"{a}_{y}" if a and y else ref_text[:30].lower()

    return result


def normalize_key(text: str) -> str:
    """Normalize any citation-like text to a matching key."""
    year = ""
    author = ""
    years = re.findall(r'\b(19[5-9]\d|20[0-2]\d)\b', text)
    if years:
        year = years[0]
    m = re.search(r'([A-ZÁÉÍÓÚÑÜ][a-záéíóúñü\-]{2,})', text)
    if m:
        author = m.group(1).lower()
    return f"{author}_{year}" if author and year else text[:30].lower()


# ─── MAIN PAPER REFERENCES (ground truth from reading the PDF) ─────────────────
# These are the 23 references cited in main.pdf, extracted manually from p.24-25.
MAIN_PAPER_REFS = [
    {"key": "aruoba_2008",        "display": "Aruoba (2008)",               "title": "Data revisions are not well-behaved"},
    {"key": "asimakopoulos_2023", "display": "Asimakopoulos et al. (2023)", "title": "GDP revisions are not cool"},
    {"key": "baker_2016",         "display": "Baker, Bloom & Davis (2016)", "title": "Measuring economic policy uncertainty"},
    {"key": "bloom_2009",         "display": "Bloom (2009)",                "title": "The impact of uncertainty shocks"},
    {"key": "breto_2019",         "display": "Bretó et al. (2019)",         "title": "Entropy-based ML algorithm for combining macroeconomic forecasts"},
    {"key": "carriero_2018",      "display": "Carriero et al. (2018)",      "title": "Measuring uncertainty and its impact on the economy"},
    {"key": "clark_2017",         "display": "Clark & Mertens (2017)",      "title": "Measuring uncertainty measures for point forecasts from surveys"},
    {"key": "croushore_2011",     "display": "Croushore (2011)",            "title": "Frontiers of real-time data analysis"},
    {"key": "ellsberg_1961",      "display": "Ellsberg (1961)",             "title": "Risk, ambiguity, and the savage axioms"},
    {"key": "faust_2005",         "display": "Faust, Rogers & Wright (2005)","title": "News and noise in G-7 GDP announcements"},
    {"key": "galvao_2019",        "display": "Galvao & Mitchell (2019)",    "title": "Measuring data uncertainty: fan charts for GDP growth"},
    {"key": "ghirelli_2019",      "display": "Ghirelli et al. (2019)",      "title": "A new economic policy uncertainty index for Spain"},
    {"key": "haussler_1997",      "display": "Haussler & Opper (1997)",     "title": "Mutual information, metric entropy, cumulative relative entropy risk"},
    {"key": "heskes_1998",        "display": "Heskes (1998)",               "title": "Bias/variance decompositions for likelihood-based estimators"},
    {"key": "jurado_2015",        "display": "Jurado, Ludvigson & Ng (2015)","title": "Measuring uncertainty"},
    {"key": "knight_1921",        "display": "Knight (1921)",               "title": "Risk, Uncertainty and Profit"},
    {"key": "mankiw_1986",        "display": "Mankiw & Shapiro (1986)",     "title": "News or noise: An analysis of GNP revisions"},
    {"key": "mankiw_1984",        "display": "Mankiw, Runkle & Shapiro (1984)","title": "Are preliminary announcements of the money stock rational forecasts?"},
    {"key": "orphanides_2001",    "display": "Orphanides (2001)",           "title": "Monetary policy rules based on real-time data"},
    {"key": "patterson_1991",     "display": "Patterson & Heravi (1991)",   "title": "Direct estimation of entropy and revisions to national income accounts"},
    {"key": "pavia_2018",         "display": "Pavía et al. (2018)",         "title": "Statistical approach to measurement of quality of official statistics: Spanish GDP"},
    {"key": "rossi_2016",         "display": "Rossi, Sekhposyan & Soupre (2016)", "title": "Understanding the sources of macroeconomic uncertainty"},
    {"key": "shoja_2017",         "display": "Shoja & Soofi (2017)",        "title": "Uncertainty, information, and disagreement of economic forecasters"},
]

MAIN_PAPER_KEYS = {r["key"] for r in MAIN_PAPER_REFS}

# Author tokens used for fuzzy matching against extracted references
MAIN_AUTHOR_TOKENS = {
    "aruoba": "aruoba_2008",
    "asimakopoulos": "asimakopoulos_2023",
    "baker": "baker_2016",
    "bloom": "bloom_2009",
    "breto": "breto_2019",
    "carriero": "carriero_2018",
    "clark": "clark_2017",
    "mertens": "clark_2017",
    "croushore": "croushore_2011",
    "ellsberg": "ellsberg_1961",
    "faust": "faust_2005",
    "galvao": "galvao_2019",
    "ghirelli": "ghirelli_2019",
    "haussler": "haussler_1997",
    "heskes": "heskes_1998",
    "jurado": "jurado_2015",
    "ludvigson": "jurado_2015",
    "knight": "knight_1921",
    "mankiw": "mankiw_1984",  # covers both 1984/1986
    "orphanides": "orphanides_2001",
    "patterson": "patterson_1991",
    "heravi": "patterson_1991",
    "pavia": "pavia_2018",
    "rossi": "rossi_2016",
    "sekhposyan": "rossi_2016",
    "shoja": "shoja_2017",
    "soofi": "shoja_2017",
}


def match_to_main_paper_ref(ref_text: str) -> str | None:
    """Return a main-paper reference key if this ref matches one, else None."""
    lower = ref_text.lower()
    year_match = re.search(r'\b(19[5-9]\d|20[0-2]\d)\b', ref_text)
    year = year_match.group(1) if year_match else ""

    for token, key in MAIN_AUTHOR_TOKENS.items():
        if token in lower:
            # Extra check for Mankiw to disambiguate 1984 vs 1986
            if token == "mankiw":
                if year == "1984":
                    return "mankiw_1984"
                elif year == "1986":
                    return "mankiw_1986"
                elif "shapiro" in lower and "runkle" in lower:
                    return "mankiw_1984"
                elif "shapiro" in lower:
                    return "mankiw_1986"
                return key
            return key
    return None


# ─── CORE ANALYSIS ────────────────────────────────────────────────────────────

def analyze_bibliography_pdf(pdf_path: Path) -> dict:
    """
    For a single bibliography PDF, return:
      - all parsed references
      - which main-paper refs it cites
      - all other references (potential gap candidates)
    """
    text = extract_pdf_text(pdf_path)
    refs_section = find_references_section(text)
    ref_blocks = parse_reference_blocks(refs_section)

    cites_main = set()
    other_refs  = []

    for block in ref_blocks:
        main_key = match_to_main_paper_ref(block)
        if main_key:
            cites_main.add(main_key)
        else:
            parsed = extract_author_year_title(block)
            if parsed["first_author"] and parsed["year"]:
                other_refs.append(parsed)

    return {
        "filename": pdf_path.name,
        "total_refs_found": len(ref_blocks),
        "cites_main_paper_refs": sorted(cites_main),
        "other_refs": other_refs,
    }


def build_citation_network(results: list) -> dict:
    """
    Aggregate results across all bibliography PDFs.
    Returns:
      - cross_citations: how many bibliography papers cite each main-paper ref
      - gap_candidates: refs NOT in main paper, with count of bibliography papers citing them
    """
    cross_citations = Counter()
    gap_pool: dict[str, dict] = {}  # key -> {count, display, raw_examples}

    for r in results:
        for key in r["cites_main_paper_refs"]:
            cross_citations[key] += 1

        for ref in r["other_refs"]:
            k = ref["key"]
            if k not in gap_pool:
                gap_pool[k] = {
                    "key": k,
                    "first_author": ref["first_author"],
                    "year": ref["year"],
                    "title_fragment": ref["title_fragment"],
                    "raw": ref["raw"][:200],
                    "cited_by_files": [],
                    "count": 0,
                }
            if r["filename"] not in gap_pool[k]["cited_by_files"]:
                gap_pool[k]["cited_by_files"].append(r["filename"])
                gap_pool[k]["count"] += 1

    # Sort gap candidates by citation frequency
    gap_candidates = sorted(gap_pool.values(), key=lambda x: -x["count"])

    return {
        "cross_citations": dict(cross_citations),
        "gap_candidates": gap_candidates,
    }


# ─── REPORT GENERATION ────────────────────────────────────────────────────────

def generate_report(
    main_refs: list,
    bib_results: list,
    network: dict,
    output_path: Path,
) -> str:
    """Write a Markdown report and return its content."""

    cross = network["cross_citations"]
    gaps  = network["gap_candidates"]
    today = datetime.now().strftime("%Y-%m-%d")

    # ── Section 1: Header
    lines = [
        f"# Análisis de Bibliografía — Agente de Gaps Académicos",
        f"",
        f"**Paper analizado:** A Multidimensional Framework for Economic Uncertainty Quantification  ",
        f"**Autores:** Manuel Hidalgo-Pérez & Leandro Navarro Pablo  ",
        f"**Fecha de análisis:** {today}  ",
        f"**PDFs analizados en bibliografía:** {len(bib_results)}  ",
        f"",
        "---",
        "",
    ]

    # ── Section 2: Summary of main paper references & their cross-citation score
    lines += [
        "## 1. Referencias del paper y su relevancia en la literatura",
        "",
        "La siguiente tabla muestra cuántos papers de tu bibliografía citan cada referencia que ya tienes en el paper. Esto indica qué tan \"central\" es cada trabajo en la red de citas.",
        "",
        "| # | Referencia | Año | Citado por N papers bibliografía | Relevancia |",
        "|---|-----------|-----|----------------------------------|-----------|",
    ]

    sorted_main = sorted(main_refs, key=lambda r: -cross.get(r["key"], 0))
    for i, ref in enumerate(sorted_main, 1):
        n = cross.get(ref["key"], 0)
        bars = "●" * n + "○" * max(0, 5 - n)
        relevance = "🔴 Muy alta" if n >= 4 else "🟠 Alta" if n >= 3 else "🟡 Media" if n >= 2 else "⚪ Baja" if n == 1 else "⬜ No detectada"
        lines.append(f"| {i} | {ref['display']} | {ref['year'] or '—'} | {n} ({bars}) | {relevance} |")

    lines += ["", ""]

    # ── Section 3: Cross-citation map per bibliography PDF
    lines += [
        "## 2. Mapa de citas cruzadas por paper de bibliografía",
        "",
        "Para cada PDF de la bibliografía, los trabajos del paper principal que cita.",
        "",
    ]

    for r in sorted(bib_results, key=lambda x: -len(x["cites_main_paper_refs"])):
        cited_display = []
        for key in r["cites_main_paper_refs"]:
            main_ref = next((m for m in main_refs if m["key"] == key), None)
            if main_ref:
                cited_display.append(main_ref["display"])
        n_found = r["total_refs_found"]
        n_cited = len(cited_display)

        fname = r["filename"].replace(".pdf", "")
        lines.append(f"### `{fname}`")
        lines.append(f"- Referencias extraídas: {n_found} | Cita {n_cited} referencias del paper principal")
        if cited_display:
            lines.append(f"- Cita: {'; '.join(cited_display)}")
        else:
            lines.append("- No se detectaron referencias cruzadas con el paper principal (posible fallo de extracción o paper muy distinto)")
        lines.append("")

    # ── Section 4: Gap Analysis — MAIN OUTPUT
    lines += [
        "## 3. Gap Analysis — Candidatos NO citados en tu paper",
        "",
        "> Papers que aparecen en la bibliografía de tus fuentes pero que **no están citados en tu paper**.",
        "> Ordenados por número de papers de la bibliografía que los citan (proxy de relevancia en la literatura).",
        "",
    ]

    # Filter: only show gaps cited by ≥2 bibliography papers (more reliable)
    high_priority = [g for g in gaps if g["count"] >= 2]
    medium_priority = [g for g in gaps if g["count"] == 1]

    lines += [
        "### 🔴 Alta prioridad — citados por 2 o más fuentes de tu bibliografía",
        "",
    ]

    if high_priority:
        lines += [
            "| Ranking | Primer autor | Año | N fuentes | Fragmento de título | Citado por |",
            "|---------|-------------|-----|-----------|---------------------|-----------|",
        ]
        for i, g in enumerate(high_priority, 1):
            title = g["title_fragment"][:60] if g["title_fragment"] else "—"
            cited_by = ", ".join([f.replace(".pdf","") for f in g["cited_by_files"][:3]])
            if len(g["cited_by_files"]) > 3:
                cited_by += f" (+{len(g['cited_by_files'])-3} más)"
            lines.append(f"| {i} | {g['first_author']} | {g['year']} | **{g['count']}** | {title} | {cited_by} |")
        lines += ["", ""]

        # Detailed cards for top candidates
        lines += ["### Fichas detalladas de candidatos de alta prioridad", ""]
        for i, g in enumerate(high_priority[:15], 1):
            lines += [
                f"#### {i}. {g['first_author']} ({g['year']}) — citado por {g['count']} fuentes",
                f"- **Fragmento de referencia:** {g['raw'][:200]}",
                f"- **Citado en:** {', '.join([f.replace('.pdf','') for f in g['cited_by_files']])}",
                "",
            ]
    else:
        lines.append("_No se encontraron candidatos con ≥2 citas cruzadas. Ver sección de prioridad media._")
        lines.append("")

    lines += [
        "### 🟡 Prioridad media — citados por exactamente 1 fuente",
        "",
        f"Se encontraron {len(medium_priority)} papers únicos citados por exactamente 1 fuente bibliográfica.",
        "Se muestran los primeros 30 ordenados por año (más recientes primero).",
        "",
    ]

    medium_sorted = sorted(medium_priority, key=lambda x: x["year"], reverse=True)[:30]
    if medium_sorted:
        lines += [
            "| Primer autor | Año | Fragmento de título | Citado en |",
            "|-------------|-----|---------------------|----------|",
        ]
        for g in medium_sorted:
            title = g["title_fragment"][:55] if g["title_fragment"] else "—"
            source = g["cited_by_files"][0].replace(".pdf","") if g["cited_by_files"] else "—"
            lines.append(f"| {g['first_author']} | {g['year']} | {title} | {source} |")
    lines += ["", ""]

    # ── Section 5: Papers in bibliography folder not cited in main paper
    lines += [
        "## 4. PDFs en la carpeta bibliografía no citados en el paper",
        "",
        "Archivos descargados que no aparecen en la lista de referencias del paper:",
        "",
    ]
    main_file_stems = {
        "aruoba2008", "asimakopoulos2023", "baker2016measuring", "bloomuncer",
        "carriero2018", "clark2017", "croushore2011", "ellsberg1961", "faust2005",
        "galvao2019", "ghirelli2019", "haussler1997", "heskes1998", "jurado2015",
        "knight1921", "mankiw1984", "mankiw1986", "orphanides2001", "patterson1991",
        "pavia2018", "rossi2016", "shoja2017",
    }
    all_bib_files = sorted(BIBLIOGRAPHY_DIR.glob("*.pdf"))
    not_cited_pdfs = [f for f in all_bib_files if f.stem not in main_file_stems]

    for f in not_cited_pdfs:
        lines.append(f"- `{f.name}`")
    lines += ["", "_Nota: `carriero2018tech.pdf` es el apéndice técnico de Carriero et al. (2018), que sí está citado._", ""]

    # ── Section 6: Paper cited in main but not in bibliography folder
    lines += [
        "## 5. Referencias del paper sin PDF en la carpeta bibliografía",
        "",
        "Trabajos citados en el paper pero cuyo PDF no está descargado:",
        "",
    ]
    bib_stems = {f.stem for f in BIBLIOGRAPHY_DIR.glob("*.pdf")}
    missing_pdfs = {
        "breto_2019": "Bretó et al. (2019) — Entropy-based ML algorithm for combining macroeconomic forecasts. *Entropy*, 21(10):1015.",
    }
    for key, desc in missing_pdfs.items():
        lines.append(f"- **{desc}**")
    lines += [""]

    # ── Section 7: Methodology note
    lines += [
        "---",
        "",
        "## Nota metodológica",
        "",
        "El agente extrae texto de cada PDF, localiza la sección de referencias mediante patrones de encabezado,",
        "segmenta referencias individuales, e identifica author+year como clave de normalización.",
        "La coincidencia con el paper principal usa tokens de apellido de primer autor.",
        "La fiabilidad de extracción depende de la calidad del PDF (escaneados o columnas complejas pueden fallar).",
        "Se recomienda revisar manualmente los candidatos de alta prioridad antes de incorporarlos al paper.",
        "",
        f"_Generado automáticamente por `bibliography_agent.py` el {today}_",
    ]

    content = "\n".join(lines)
    output_path.write_text(content, encoding="utf-8")
    return content


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  BIBLIOGRAPHY ANALYSIS AGENT")
    print("  A Multidimensional Framework for Economic Uncertainty")
    print("=" * 60)

    # Validate paths
    if not MAIN_PAPER_PATH.exists():
        print(f"✗ Main paper not found: {MAIN_PAPER_PATH}")
        return
    if not BIBLIOGRAPHY_DIR.exists():
        print(f"✗ Bibliography directory not found: {BIBLIOGRAPHY_DIR}")
        return

    bib_pdfs = sorted(BIBLIOGRAPHY_DIR.glob("*.pdf"))
    print(f"\n→ Found {len(bib_pdfs)} PDFs in bibliography folder")
    print(f"→ Main paper has {len(MAIN_PAPER_REFS)} known references\n")

    # Process each bibliography PDF
    results = []
    for pdf in bib_pdfs:
        print(f"  Processing: {pdf.name}")
        r = analyze_bibliography_pdf(pdf)
        results.append(r)
        print(f"    Found {r['total_refs_found']} refs | "
              f"Cites {len(r['cites_main_paper_refs'])} main-paper refs")

    # Build network
    print("\n→ Building citation network...")
    network = build_citation_network(results)

    high_priority = [g for g in network["gap_candidates"] if g["count"] >= 2]
    total_unique  = len(network["gap_candidates"])
    print(f"  Total unique gap candidates: {total_unique}")
    print(f"  High-priority (cited ≥2 times): {len(high_priority)}")

    # Save JSON data
    json_path = OUTPUT_DIR / "bibliography_network.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "main_paper_refs": MAIN_PAPER_REFS,
            "bibliography_results": [
                {k: v for k, v in r.items() if k != "other_refs"}
                for r in results
            ],
            "cross_citations": network["cross_citations"],
            "top_gap_candidates": network["gap_candidates"][:50],
        }, f, ensure_ascii=False, indent=2)
    print(f"\n→ Raw data saved to: {json_path.name}")

    # Generate report
    report_path = OUTPUT_DIR / "bibliography_gap_report.md"
    print(f"→ Generating Markdown report...")
    generate_report(MAIN_PAPER_REFS, results, network, report_path)
    print(f"→ Report saved to: {report_path.name}")

    # Quick summary
    print("\n" + "=" * 60)
    print("  TOP CROSS-CITATIONS (main paper refs, by N bib papers citing them)")
    print("=" * 60)
    sorted_cross = sorted(network["cross_citations"].items(), key=lambda x: -x[1])
    for key, n in sorted_cross[:8]:
        ref = next((r for r in MAIN_PAPER_REFS if r["key"] == key), {"display": key})
        print(f"  {n:2d}x  {ref['display']}")

    if high_priority:
        print("\n" + "=" * 60)
        print("  TOP GAP CANDIDATES (not in your paper, cited by ≥2 bib papers)")
        print("=" * 60)
        for g in high_priority[:10]:
            print(f"  {g['count']:2d}x  {g['first_author']} ({g['year']}) — {g['title_fragment'][:60]}")

    print("\n✓ Analysis complete.\n")


if __name__ == "__main__":
    main()
