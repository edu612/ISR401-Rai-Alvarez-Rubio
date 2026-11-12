"""Compila el informe y ofrece instalar Tectonic si todavía no está disponible."""

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


def install_directory() -> Path:
    local_app_data = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return local_app_data / "Programs" / "Tectonic"


def find_windows_asset() -> Tuple[str, Optional[str]]:
    if platform.machine().lower() not in {"amd64", "x86_64"}:
        raise RuntimeError("La instalación automática requiere Windows x64.")
    request = urllib.request.Request(
        RELEASES_API,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "ISR401-report-builder"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        release = json.load(response)
    for asset in release.get("assets", []):
        if asset.get("name", "").endswith("x86_64-pc-windows-msvc.zip"):
            return asset["browser_download_url"], asset.get("digest")
    raise RuntimeError("No encontré el paquete oficial de Tectonic para Windows x64.")


def add_to_user_path(directory: Path) -> None:
    import winreg

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_QUERY_VALUE | winreg.KEY_SET_VALUE) as key:
        try:
            current, value_type = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current, value_type = "", winreg.REG_EXPAND_SZ
        entries = [entry for entry in current.split(";") if entry]
        known = {os.path.normcase(os.path.normpath(entry)) for entry in entries}
        target = os.path.normcase(os.path.normpath(str(directory)))
        if target not in known:
            entries.append(str(directory))
            winreg.SetValueEx(key, "Path", 0, value_type, ";".join(entries))
    os.environ["PATH"] = str(directory) + os.pathsep + os.environ.get("PATH", "")


def install_tectonic() -> Path:
    if sys.platform != "win32":
        raise RuntimeError(f"La instalación automática es para Windows. Guía: {INSTALL_GUIDE}")
    url, expected = find_windows_asset()
    destination = install_directory()
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="tectonic-install-") as temporary:
        archive_path = Path(temporary) / "tectonic.zip"
        request = urllib.request.Request(url, headers={"User-Agent": "ISR401-report-builder"})
        digest = hashlib.sha256()
        with urllib.request.urlopen(request, timeout=60) as response, archive_path.open("wb") as archive_file:
            while chunk := response.read(1024 * 1024):
                archive_file.write(chunk)
                digest.update(chunk)
        if expected and expected.startswith("sha256:") and digest.hexdigest().lower() != expected.split(":", 1)[1].lower():
            raise RuntimeError("La verificación SHA-256 del instalador no coincidió.")
        with zipfile.ZipFile(archive_path) as archive:
            name = next((item for item in archive.namelist() if Path(item).name.lower() == "tectonic.exe"), None)
            if name is None:
                raise RuntimeError("El paquete no contiene tectonic.exe.")
            with archive.open(name) as source, (destination / "tectonic.exe").open("wb") as target:
                shutil.copyfileobj(source, target)
    add_to_user_path(destination)
    return destination / "tectonic.exe"


def find_or_install() -> Optional[str]:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    binary = shutil.which("tectonic")
    if binary:
        return binary
    installed = install_directory() / "tectonic.exe"
    if sys.platform == "win32" and installed.is_file():
        add_to_user_path(installed.parent)
        return str(installed)
    print("No encuentro Tectonic. Si aceptas, descargaré el ejecutable oficial de Windows x64,")
    print("lo instalaré en tu perfil y lo agregaré al PATH para futuras ejecuciones.")
    try:
        answer = input("¿Quieres instalarlo ahora? [S/n]: ").strip().lower()
    except EOFError:
        print("Abre una terminal interactiva para instalar Tectonic.", file=sys.stderr)
        return None
    if answer not in {"", "s", "sí", "si", "y", "yes"}:
        print(f"Puedes instalarlo más tarde: {INSTALL_GUIDE}")
        return None
    try:
        binary = str(install_tectonic())
    except Exception as error:
        print(f"No pude instalar Tectonic: {error}\nGuía oficial: {INSTALL_GUIDE}", file=sys.stderr)
        return None
    print("Tectonic quedó instalado; ahora compilaré el informe.")
    return binary


def main() -> int:
    tectonic = find_or_install()
    if tectonic is None:
        return 1
    BUILD.mkdir(exist_ok=True)
    print("Compilando TA-IND-01/main.tex...")
    result = subprocess.run([tectonic, "--outdir", str(BUILD), "main.tex"], cwd=ROOT, check=False)
    if result.returncode:
        return result.returncode
    compiled = BUILD / "main.pdf"
    if not compiled.is_file():
        print("No encuentro el PDF compilado.", file=sys.stderr)
        return 1
    shutil.copy2(compiled, ROOT / "main.pdf")
    print(f"PDF creado: {ROOT / 'main.pdf'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
