"""Quick check of installed packages"""
import sys

packages = [
    'pandas', 'numpy', 'openpyxl', 'python_pptx', 'sqlalchemy', 
    'pydantic', 'yaml', 'fuzzywuzzy', 'presidio_analyzer', 
    'presidio_anonymizer', 'spacy', 'loguru', 'tqdm'
]

print("Checking installed packages...\n")
missing = []
installed = []

for pkg in packages:
    try:
        if pkg == 'yaml':
            __import__('yaml')
        elif pkg == 'python_pptx':
            __import__('pptx')
        else:
            __import__(pkg)
        installed.append(pkg)
        print(f"[OK] {pkg}")
    except ImportError:
        missing.append(pkg)
        print(f"[MISSING] {pkg}")

print(f"\n[OK] Installed: {len(installed)}/{len(packages)}")
if missing:
    print(f"[MISSING] Missing: {len(missing)}/{len(packages)}")
    print(f"\nMissing packages: {', '.join(missing)}")
    print("\nTo install missing packages, run:")
    print(f"python -m pip install {' '.join(missing)}")

