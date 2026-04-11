# intro-bio-inf-unq
Repositorio para la materia de Introducción a la Bioinformatica

## CLI de prediccion (Desafio V)

Se incluye un script CLI para predecir estructura secundaria por residuo con etiquetas:

- H: helice
- B: lamina beta
- L: bucle

### Ejemplos rapidos

Prediccion desde secuencia directa:

```powershell
python -m intro_biologia.cli --secuencia AELMQK --id prot1 --formato texto
```

Prediccion desde archivo FASTA:

```powershell
python -m intro_biologia.cli --input .\ejemplos\proteina_mixta_unica.fasta --formato texto
```

Salida en JSON:

```powershell
python -m intro_biologia.cli --input .\ejemplos\tres_proteinas.fasta --formato json
```

Salida en TSV a archivo:

```powershell
python -m intro_biologia.cli --input .\ejemplos\tres_proteinas.fasta --formato tsv --output .\salida.tsv
```

Tambien se puede leer desde stdin:

```powershell
Get-Content .\ejemplos\tres_proteinas.fasta | python -m intro_biologia.cli --stdin --formato fasta
```

Archivos de ejemplo disponibles en `ejemplos/`.
