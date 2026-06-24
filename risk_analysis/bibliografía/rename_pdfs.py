import os

rename_map = {
    "berge 2020.pdf": "berge2020.pdf",
    "Bloom uncer shocks Ec 09.pdf": "bloomuncer.pdf",
    "carriero 2018.pdf": "carriero2018.pdf",
    "carriero 2018 tech note.pdf": "carriero2018tech.pdf",
    "clark 2017.pdf": "clark2017.pdf",
    "ellsebrg 1961.pdf": "ellsberg1961.pdf",
    "jurado 2015.pdf": "jurado2015.pdf",
    "knight 1921.pdf": "knight1921.pdf",
    "rossi 2016.pdf": "rossi2016.pdf",
    "Haussler-MutualInformationMetric-1997.pdf": "haussler1997.pdf",
    "Pavia et al 2019.pdf": "pavia2018.pdf",
    "2011-frontiers-of-real-time-data-analysis.pdf": "croushore2011.pdf",
    "Aruoba-DataRevisionsWell-2008.pdf": "aruoba2008.pdf",
    "ssrn-4618392.pdf": "asimakopoulos2023.pdf",
    "2010-monetary-policy-rules-based-on-real-time-data.pdf": "orphanides2001.pdf",
    "w1939.pdf": "mankiw1986.pdf",
    "baker_epu.pdf": "baker2016measuring.pdf",
}

for old_name, new_name in rename_map.items():
    if os.path.exists(old_name):
        try:
            os.rename(old_name, new_name)
            print(f"Renamed: '{old_name}' -> '{new_name}'")
        except Exception as e:
            print(f"Error renaming '{old_name}': {e}")
    else:
        print(f"File not found: '{old_name}'")

print("\n--- Remaining Unmapped Files ---")
for file in os.listdir("."):
    if file.endswith(".pdf") and file not in rename_map.values():
        print(file)
