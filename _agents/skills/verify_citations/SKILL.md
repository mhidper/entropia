---
name: verify_citations
description: Skill to verify that bibliographic citations in the LaTeX manuscript match the claims natively expressed in the supporting PDFs.
---

# Verify Citations Skill

This skill defines the standard operating procedure for auditing bibliographic citations during manuscript revision.

## Objective
Ensure that every claim assigned to a citation in the manuscript is genuinely supported by the source document.

## Workflow

1. **Identify the Claim and the Citation**:
   Review the manuscript text where the citation is used and explicitly isolate the claim that is being attributed to the author(s).

2. **Locate the PDF**:
   Look for the cited PDF file in the directory: `C:\Users\Usuario\Documents\Github\Entropía\risk_analysis\bibliografía`.
   - You can use the `list_dir` tool or `run_command` to find the exact file.

3. **Handle Missing PDFs**:
   If the PDF is **not found** in the directory:
   - STOP immediately.
   - Inform the user exactly which PDF is missing (e.g., "Falta el PDF de [Autor Año] en la carpeta bibliografía. Por favor búscalo, súbelo a la carpeta y avísame para reintentar la comprobación.").

4. **Extract and Verify Text (If PDF is found)**:
   - Extract the text from the PDF. You can use Python scripts via `run_command` (e.g., using `PyPDF2` or `pymupdf`) to parse the PDF text if it is not directly readable.
   - Read the relevant sections (Abstract, Introduction, Conclusion, or Keyword Search).
   - Select the exact excerpt from the PDF that supports or refutes the manuscript's claim.

5. **Report to User**:
   Provide a response to the user that explicitly includes:
   - The original claim from our manuscript.
   - The exact quote from the PDF supporting the claim (quote it verbatim).
   - An assessment of whether our claim faithfully represents the source, or if we should tweak our wording (e.g., softening the language).
