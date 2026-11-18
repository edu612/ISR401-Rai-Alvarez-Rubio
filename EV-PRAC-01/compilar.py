from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
tectonic = shutil.which("tectonic")
if tectonic:
    subprocess.run([tectonic, "-X", "compile", "--outdir", str(BUILD), str(ROOT / "main.tex")], check=True)
    shutil.copy2(BUILD / "main.pdf", ROOT / "main.pdf")
else:
    pdflatex = shutil.which("pdflatex")
    if not pdflatex:
        raise SystemExit("Instale Tectonic o pdfLaTeX para compilar el documento.")
    subprocess.run([pdflatex, "-interaction=nonstopmode", "-halt-on-error", "-output-directory", str(BUILD), str(ROOT / "main.tex")], check=True)
    shutil.copy2(BUILD / "main.pdf", ROOT / "main.pdf")
