import sys
try:
    import PyPDF2
    with open('w1939.pdf', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for i in range(min(5, len(reader.pages))): # read first 5 pages
            text += reader.pages[i].extract_text()
        print("FIRST 5 PAGES:\n", text[:1000])
        
        # Also search for 'trade-off' or 'timeliness' or 'precision'
        print("\n\n--- SEARCHING FOR KEYWORDS ---")
        full_text = ""
        for p in reader.pages:
            full_text += p.extract_text().lower() + "\n"
        
        keywords = ['trade-off', 'timeliness', 'precision', 'accuracy', 'statistical agencies']
        for kw in keywords:
            idx = full_text.find(kw)
            if idx != -1:
                start = max(0, idx - 150)
                end = min(len(full_text), idx + 150)
                print(f"Found '{kw}': ...{full_text[start:end]}...\n")
except Exception as e:
    print("Error:", e)
    
try:
    import fitz # pymupdf
    print("\nPyMuPDF is also available.")
except ImportError:
    pass
