from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
EVIDENCIAS = ROOT / "evidencias"

def main():
    required = [EVIDENCIAS / f"hoja-{i:02d}.jpg" for i in range(1, 5)]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        raise SystemExit("Faltan las fotografías originales: " + ", ".join(missing))
    BUILD.mkdir(exist_ok=True)
    tectonic = shutil.which("tectonic")
    pdflatex = shutil.which("pdflatex")
    if tectonic:
        command = [tectonic, "--outdir", str(BUILD), str(ROOT / "main.tex")]
    elif pdflatex:
        command = [pdflatex, "-interaction=nonstopmode", "-halt-on-error",
                   "-output-directory", str(BUILD), str(ROOT / "main.tex")]
    else:
        raise SystemExit("Instala Tectonic o pdfLaTeX para compilar el documento.")
    subprocess.run(command, cwd=ROOT, check=True)
    generated = BUILD / "main.pdf"
    if not generated.is_file():
        raise SystemExit("La compilación terminó sin generar main.pdf.")
    shutil.copy2(generated, ROOT / "main.pdf")
    print("PDF generado correctamente:", ROOT / "main.pdf")

if __name__ == "__main__":
    main()
