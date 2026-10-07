import json

with open('EDA_DA_ADVANCED_PRESENTATION_READY (1).ipynb', 'r') as f:
    nb = json.load(f)
    
for cell in nb.get('cells', []):
    if cell['cell_type'] == 'markdown':
        source = "".join(cell.get('source', []))
        if source.startswith('#'):
            print(f"MARKDOWN: {source.strip().split(chr(10))[0]}")
    elif cell['cell_type'] == 'code':
        source = "".join(cell.get('source', []))
        if source.strip():
            print(f"CODE (first 2 lines): {source.strip().split(chr(10))[0]}")

