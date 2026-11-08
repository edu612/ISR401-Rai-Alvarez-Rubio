# ISR401 - Clasificación de requisitos

En este repositorio guardo las fuentes del informe y el PDF compilado.

## Requisitos para compilar

- El compilador Tectonic instalado y disponible en el `PATH`.
- Python 3.8 o superior.
- Conexión a internet la primera vez que se compila, para que Tectonic descargue los paquetes LaTeX necesarios. La bibliografía usa el estilo `IEEEtran`.

## Compilación

El archivo principal es `informe.tex`; las referencias están en `referencias.bib`. En Windows, desde la carpeta raíz del repositorio, ejecuto:

```powershell
python .\compilar.py
```

El script revisa si Tectonic está instalado. Si falta, muestra un mensaje en español con la guía oficial de instalación. Si está disponible, lo ejecuta para procesar el documento, las citas y la bibliografía. Guarda los archivos de compilación en `build/` y deja el PDF final en `output/pdf/informe.pdf`.

También puedo compilar manualmente con este comando:

```powershell
New-Item -ItemType Directory -Force build, output\pdf
tectonic --outdir build informe.tex
Copy-Item build\informe.pdf output\pdf\informe.pdf -Force
```

## Contenido

- `informe.tex`: informe editable, redactado en primera persona.
- `referencias.bib`: referencia usada, en formato BibTeX.
- `compilar.py`: script de compilación y verificación de dependencias.
- `output/pdf/informe.pdf`: versión compilada del informe.

El punto de discusión con un compañero queda pendiente para completarlo después de hacer esa comparación.
