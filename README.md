# ISR401 - Clasificación de requisitos

En este repositorio guardo las fuentes del informe y el PDF compilado dentro de `FORM-TL-01`, como pide la organización de entrega.

```text
FORM-TL-01/
├── main.tex
├── main.pdf
├── referencias.bib
└── compilar.py
```

El informe contiene la clasificación de los 20 enunciados, cinco requisitos de calidad cuantificados y una comparación documental con el trabajo de un compañero. Las resoluciones están redactadas como conclusiones propias, sin atribuirle una conversación o un acuerdo directo.

## Requisitos para compilar

- Python 3.8 o superior.
- En Windows x64, si Tectonic no está instalado, el script pregunta si quieres instalarlo. Si aceptas, descarga la publicación oficial más reciente, la instala en tu perfil y agrega su carpeta al `PATH` de usuario.
- Conexión a internet para instalar Tectonic cuando falta y para la primera compilación, que descarga los paquetes LaTeX necesarios. La bibliografía usa el estilo `IEEEtran`.

## Compilación

El archivo principal es `FORM-TL-01/main.tex`; las referencias están en `FORM-TL-01/referencias.bib`. En Windows, desde la carpeta raíz del repositorio, ejecuto:

```powershell
python .\FORM-TL-01\compilar.py
```

El script busca Tectonic en el `PATH` y también revisa `%LOCALAPPDATA%\Programs\Tectonic`, por si la terminal aún no ha cargado el cambio de `PATH`. Solo pregunta si no lo encuentra en ninguno de esos lugares. Si aceptas, descarga el ejecutable desde las publicaciones oficiales de Tectonic, lo instala en esa carpeta, agrega la ruta al `PATH` de usuario y sigue con la compilación. Como reconoce la instalación local en las siguientes ejecuciones, ya no vuelve a preguntar. Guarda los archivos de compilación en `FORM-TL-01/build/` y deja el PDF final en `FORM-TL-01/main.pdf`. En otros sistemas operativos, instala Tectonic siguiendo la [guía oficial](https://tectonic-typesetting.github.io/install.html).

También puedo compilar manualmente con este comando:

```powershell
Set-Location FORM-TL-01
New-Item -ItemType Directory -Force build
tectonic --outdir build main.tex
Copy-Item build\main.pdf main.pdf -Force
```

## TA-IND-01 - Análisis de PeiGo

La segunda actividad está organizada así:

```text
TA-IND-01/
├── main.tex
├── main.pdf
├── referencias.bib
├── compilar.py
└── figuras/
```

Para compilar el informe en Windows desde la raíz del repositorio, ejecuto:

```powershell
python .\TA-IND-01\compilar.py
```

El script detecta Tectonic en el `PATH` o en `%LOCALAPPDATA%\Programs\Tectonic`. Si no lo encuentra, pregunta si quiero instalarlo; al aceptar, descarga el ejecutable oficial, lo agrega al `PATH` del usuario y compila el PDF. En ejecuciones posteriores reconoce la instalación y compila directamente. Guarda los auxiliares en `TA-IND-01/build/` y genera el resultado en `TA-IND-01/main.pdf`. Requiere conexión a internet durante la instalación y la primera compilación.

El archivo principal es `TA-IND-01/main.tex`, las referencias están en `TA-IND-01/referencias.bib` y las tres capturas propias de PeiGo están en `TA-IND-01/figuras/`.

## Contenido

- `FORM-TL-01/main.tex`: informe editable, redactado en primera persona.
- `FORM-TL-01/referencias.bib`: referencias usadas, en formato BibTeX.
- `FORM-TL-01/compilar.py`: script de compilación y verificación de dependencias.
- `FORM-TL-01/main.pdf`: versión compilada del informe.
