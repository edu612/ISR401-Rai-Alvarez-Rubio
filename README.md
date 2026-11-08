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

- El compilador Tectonic instalado y disponible en el `PATH`.
- Python 3.8 o superior.
- Conexión a internet la primera vez que se compila, para que Tectonic descargue los paquetes LaTeX necesarios. La bibliografía usa el estilo `IEEEtran`.

## Compilación

El archivo principal es `FORM-TL-01/main.tex`; las referencias están en `FORM-TL-01/referencias.bib`. En Windows, desde la carpeta raíz del repositorio, ejecuto:

```powershell
python .\FORM-TL-01\compilar.py
```

El script revisa si Tectonic está instalado. Si falta, muestra un mensaje en español con la guía oficial de instalación. Si está disponible, lo ejecuta para procesar el documento, las citas y la bibliografía. Guarda los archivos de compilación en `FORM-TL-01/build/` y deja el PDF final en `FORM-TL-01/main.pdf`.

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
