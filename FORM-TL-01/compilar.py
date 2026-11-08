"""Compila main.tex y pregunta si debe instalar Tectonic cuando falta."""

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional, Tuple


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
RELEASES_API = "https://api.github.com/repos/tectonic-typesetting/tectonic/releases/latest"
INSTALL_GUIDE = "https://tectonic-typesetting.github.io/install.html"


def _install_directory() -> Path:
    local_app_data = Path(
        os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
    )
    return local_app_data / "Programs" / "Tectonic"


def _windows_asset() -> Tuple[str, Optional[str]]:
    machine = platform.machine().lower()
    if machine not in {"amd64", "x86_64"}:
        raise RuntimeError(
            "La instalación automática está preparada para Windows x64; "
            f"la arquitectura detectada es {machine or 'desconocida'}."
        )

    request = urllib.request.Request(
        RELEASES_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "ISR401-report-builder",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        release = json.load(response)

    for asset in release.get("assets", []):
        if asset.get("name", "").endswith("x86_64-pc-windows-msvc.zip"):
            return asset["browser_download_url"], asset.get("digest")
    raise RuntimeError("No encontré el paquete oficial de Tectonic para Windows x64.")


def _add_to_user_path(directory: Path) -> None:
    import winreg

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Environment",
        0,
        winreg.KEY_QUERY_VALUE | winreg.KEY_SET_VALUE,
    ) as key:
        try:
            current_path, value_type = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_path, value_type = "", winreg.REG_EXPAND_SZ

        entries = [entry for entry in current_path.split(";") if entry]
        normalized = {os.path.normcase(os.path.normpath(entry)) for entry in entries}
        target = os.path.normcase(os.path.normpath(str(directory)))
        if target not in normalized:
            entries.append(str(directory))
            winreg.SetValueEx(key, "Path", 0, value_type, ";".join(entries))

    # Hace que el compilador quede disponible en esta ejecución; la entrada del
    # registro también la carga cualquier terminal nueva.
    os.environ["PATH"] = str(directory) + os.pathsep + os.environ.get("PATH", "")


def _download_and_install() -> Path:
    if sys.platform != "win32":
        raise RuntimeError(
            "La instalación automática está disponible para Windows. "
            f"Para otro sistema, sigue esta guía: {INSTALL_GUIDE}"
        )

    download_url, expected_digest = _windows_asset()
    install_dir = _install_directory()
    install_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="tectonic-install-") as temp_dir:
        archive_path = Path(temp_dir) / "tectonic.zip"
        request = urllib.request.Request(
            download_url, headers={"User-Agent": "ISR401-report-builder"}
        )
        digest = hashlib.sha256()
        with urllib.request.urlopen(request, timeout=60) as response:
            with archive_path.open("wb") as archive_file:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    archive_file.write(chunk)
                    digest.update(chunk)

        if expected_digest and expected_digest.startswith("sha256:"):
            actual = digest.hexdigest().lower()
            expected = expected_digest.split(":", 1)[1].lower()
            if actual != expected:
                raise RuntimeError("La verificación SHA-256 del instalador no coincidió.")

        with zipfile.ZipFile(archive_path) as archive:
            binary_name = next(
                (
                    name
                    for name in archive.namelist()
                    if Path(name).name.lower() == "tectonic.exe"
                ),
                None,
            )
            if binary_name is None:
                raise RuntimeError("El paquete descargado no contiene tectonic.exe.")
            binary_path = install_dir / "tectonic.exe"
            with archive.open(binary_name) as source, binary_path.open("wb") as target:
                shutil.copyfileobj(source, target)

    _add_to_user_path(install_dir)
    return install_dir / "tectonic.exe"


def _find_or_install_tectonic() -> Optional[str]:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    tectonic = shutil.which("tectonic")
    if tectonic:
        return tectonic

    print("No encuentro Tectonic en el PATH.")
    print("Si aceptas, descargaré el ejecutable oficial para Windows x64,")
    print("lo instalaré en tu perfil y lo agregaré al PATH de tu usuario.")
    print("Una vez instalado, no volveré a preguntarte en las próximas compilaciones.")
    try:
        answer = input("¿Quieres instalarlo ahora? [S/n]: ").strip().lower()
    except EOFError:
        print("Ejecuta este script desde una terminal interactiva para instalarlo.", file=sys.stderr)
        return None

    if answer not in {"", "s", "sí", "si", "y", "yes"}:
        print(f"No instalé Tectonic. Puedes hacerlo más tarde: {INSTALL_GUIDE}")
        return None

    try:
        binary_path = _download_and_install()
    except Exception as error:
        print(f"No pude instalar Tectonic: {error}", file=sys.stderr)
        print(f"Guía oficial: {INSTALL_GUIDE}", file=sys.stderr)
        return None

    tectonic = shutil.which("tectonic") or str(binary_path)
    print("Tectonic quedó instalado y agregado al PATH de tu usuario.")
    return tectonic


def main() -> int:
    tectonic = _find_or_install_tectonic()
    if tectonic is None:
        return 1

    BUILD.mkdir(exist_ok=True)
    print("Compilando main.tex con Tectonic...")
    result = subprocess.run(
        [tectonic, "--outdir", str(BUILD), "main.tex"],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        print(
            "La compilación no terminó correctamente. Revisa el mensaje de Tectonic.",
            file=sys.stderr,
        )
        return result.returncode

    compiled_pdf = BUILD / "main.pdf"
    if not compiled_pdf.is_file():
        print("Tectonic terminó, pero no encuentro build/main.pdf.", file=sys.stderr)
        return 1

    final_pdf = ROOT / "main.pdf"
    shutil.copy2(compiled_pdf, final_pdf)
    print(f"PDF creado en: {final_pdf.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
