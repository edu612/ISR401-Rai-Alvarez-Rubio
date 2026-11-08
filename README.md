# ISR401 - Clasificación de requisitos

En este repositorio guardo las fuentes del informe y el PDF compilado dentro de `FORM-TL-01`, como pide la organización de entrega.

```text
FORM-TL-01/
├── main.tex
├── main.pdf
├── referencias.bib
└── compilar.py
```

El informe contiene la clasificación de los 20 enunciados y cinco requisitos de calidad cuantificados. La discusión de discrepancias con un compañero queda pendiente para completarla después de hacer esa comparación.

## Requisitos para compilar

- Python 3.8 o superior.
- En Windows x64, si Tectonic no está instalado, el script pregunta si quieres instalarlo. Si aceptas, descarga la publicación oficial más reciente, la instala en tu perfil y agrega su carpeta al `PATH` de usuario.
- Conexión a internet para instalar Tectonic cuando falta y para la primera compilación, que descarga los paquetes LaTeX necesarios. La bibliografía usa el estilo `IEEEtran`.

## Compilación

El archivo principal es `FORM-TL-01/main.tex`; las referencias están en `FORM-TL-01/referencias.bib`. En Windows, desde la carpeta raíz del repositorio, ejecuto:

```powershell
python .\FORM-TL-01\compilar.py
```

El script busca Tectonic y solo pregunta por la instalación cuando no lo encuentra. Si aceptas, descarga el ejecutable desde las publicaciones oficiales de Tectonic, lo instala en `%LOCALAPPDATA%\Programs\Tectonic`, agrega esa carpeta al `PATH` de usuario y sigue con la compilación. Como queda instalado en el `PATH`, no vuelve a preguntar en las siguientes ejecuciones. Guarda los archivos de compilación en `FORM-TL-01/build/` y deja el PDF final en `FORM-TL-01/main.pdf`. En otros sistemas operativos, instala Tectonic siguiendo la [guía oficial](https://tectonic-typesetting.github.io/install.html).

También puedo compilar manualmente con este comando:

```powershell
Set-Location FORM-TL-01
New-Item -ItemType Directory -Force build
tectonic --outdir build main.tex
Copy-Item build\main.pdf main.pdf -Force
```

## Contenido

- `FORM-TL-01/main.tex`: informe editable, redactado en primera persona.
- `FORM-TL-01/referencias.bib`: referencias usadas, en formato BibTeX.
- `FORM-TL-01/compilar.py`: script de compilación y verificación de dependencias.
- `FORM-TL-01/main.pdf`: versión compilada del informe.

El punto de discusión con un compañero queda pendiente para completarlo después de hacer esa comparación.
