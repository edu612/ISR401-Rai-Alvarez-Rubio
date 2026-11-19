# EV-PRAC-01 – Evaluación práctica

Reproducción en PDF de las cuatro hojas originales de la evaluación del sistema FRIOVAC. `main.tex` incorpora las páginas del archivo `referencia.pdf` sin transcribirlas ni alterar su contenido visual.

## Archivos

- `main.tex`: documento fuente en LaTeX.
- `main.pdf`: documento compilado.
- `compilar.py`: script para compilar el documento.
- `referencia.pdf`: archivo original utilizado por LaTeX.

## Requisitos

Se necesita Python 3 y uno de estos compiladores: Tectonic o pdfLaTeX.

## Compilación

Desde la raíz del repositorio:

```bash
python EV-PRAC-01/compilar.py
```

El PDF generado se guarda en `EV-PRAC-01/main.pdf` y mantiene las cuatro páginas, su tamaño y su aspecto original.
