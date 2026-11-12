# ISR401 - Informes de requisitos

En este repositorio guardo las dos tareas de ISR-401, con sus fuentes editables, referencias, scripts y PDFs compilados.

```text
FORM-TL-01/
├── main.tex
├── main.pdf
├── referencias.bib
└── compilar.py

TA-IND-01/
├── main.tex
├── main.pdf
├── referencias.bib
├── compilar.py
└── figuras/   # tres capturas propias de PeiGo
```

## Requisitos

- Python 3.8 o superior.
- Conexión a internet para instalar Tectonic si hace falta y para descargar los paquetes LaTeX de la primera compilación.

Los dos scripts buscan Tectonic en el `PATH` y en `%LOCALAPPDATA%\Programs\Tectonic`. Si no lo encuentran en Windows x64, preguntan si quiero instalarlo. Al aceptar, descargan la versión oficial, la agregan al `PATH` del usuario y continúan con la compilación. En las siguientes ejecuciones detectan la instalación y no vuelven a preguntar.

En otros sistemas operativos, instalo Tectonic siguiendo la [guía oficial](https://tectonic-typesetting.github.io/install.html) antes de ejecutar el script.

## Cómo compilo las tareas

Desde PowerShell, en la carpeta raíz del repositorio, ejecuto el comando de la tarea que quiero generar:

```powershell
python .\FORM-TL-01\compilar.py
python .\TA-IND-01\compilar.py
```

Para compilar las dos, ejecuto ambos comandos. Cada script deja los archivos auxiliares en la carpeta `build/` de su tarea y actualiza el PDF correspondiente en esa misma carpeta (`main.pdf`). La bibliografía de ambos informes usa el estilo IEEE.

## Qué contiene cada tarea

- `FORM-TL-01/`: clasificación de los 20 enunciados, cinco requisitos de calidad cuantificados y comparación documental.
- `TA-IND-01/`: análisis de la norma aplicado a PeiGo, glosario, 15 requisitos, tabla de clasificación, autoevaluación y reflexión. Las tres capturas propias están en `TA-IND-01/figuras/`.
