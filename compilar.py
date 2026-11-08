"""Compila el informe y deja el PDF en output/pdf/."""

from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
PDF_DIR = ROOT / "output" / "pdf"


def main() -> int:
    tectonic = shutil.which("tectonic")
    if tectonic is None:
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
        print(
            "No encuentro Tectonic en el PATH.\n"
            "Instálalo siguiendo la guía oficial: "
            "https://tectonic-typesetting.github.io/install.html\n"
            "Después, abre una terminal nueva, comprueba `tectonic --version` "
            "y vuelve a ejecutar `python compilar.py`.",
            file=sys.stderr,
        )
        return 1

    BUILD.mkdir(exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    print("Compilando informe.tex con Tectonic...")
    result = subprocess.run(
        [tectonic, "--outdir", str(BUILD), "informe.tex"],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        print(
            "La compilación no terminó correctamente. Revisa el mensaje de Tectonic.",
            file=sys.stderr,
        )
        return result.returncode

    compiled_pdf = BUILD / "informe.pdf"
    if not compiled_pdf.is_file():
        print("Tectonic terminó, pero no encuentro build/informe.pdf.", file=sys.stderr)
        return 1

    final_pdf = PDF_DIR / "informe.pdf"
    shutil.copy2(compiled_pdf, final_pdf)
    print(f"PDF creado en: {final_pdf.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
