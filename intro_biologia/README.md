DESAFÍO I: ¿Podrías buscar un ejemplo de macromoléculas que almacenen información sobre la ‘identidad’ de un organismo dado?

El ADN y ARN son e jemplos de macromoleculas que almacenan información sobre la identidad de los organismos.

🧗🏻‍♀️ DESAFÍO II: Proponé una forma de expresar la información contenida en la estructura primaria de las proteínas usando tipos de datos de los lenguajes de programación que conocés.

🧗🏻‍♀️ DESAFÍO III: ¿ En qué tipo de datos podrías expresar la información de la estructura terciaria proteica?
Se podria utilizar una matriz de N x 3 para modelar las posiciones de cada aminoacido que forma la proteina 
con estructura terciaria.

🧗🏻‍♀️DESAFÍO IV: Rosalind Franklin es una científica muy relevante, que tuvo menos reconocimiento del merecido. ¿Cuáles fueron sus contribuciones en este campo? ¿Qué nos cuenta su historia acerca del mundo de la ciencia?

En primera instancia si bien desde joven mostro aptitudes para la ciencia, su propio padre fue detractora de que se dedicara a la investigación por el hecho de ser mujer. Contribuyo en el descubrimiento de la estructura helicoidal del ADN mediante la toma de imagen de difracción de rayos X. Logro por el cual no fue reconocida como deberia, ya que fue traicionada por Maurice Winkins quien dio acceso sin permiso a las investigaciones y descubrimientos hechos por Rosalind a otros investigadores que practicamente se robaron todo el credito.

Tambien contribuyo a el conocimiento de la estructura del Virus del Mosaico del Tabaco (TMV) y la polio respectivamente, trabajo el cual fue completado de forma postuma por su equipo de trabajo.

Murio con tan solo 37 años a causa de un cancer (relacionado con la exposición constante a los rayos X).

🧗🏻‍♀️ DESAFÍO V: Escribí un scrip en Python que prediga la estructura secundaria que adoptará cada residuo (aminoácido) de la secuencia proteica dada, especificandola como H (si es una hélice), B (si es una hoja beta plegada) y L (si es un bucle o loop).

Para este desafio se implemento un CLI para facilitar las pruebas de entrada/salida del algoritmo.

CLI (resumen breve)

Uso:
python -m intro_biologia.cli [-h] (-i INPUT | -s SECUENCIA | --stdin) [--id ID] [-f {texto,fasta,tsv,json}] [-o OUTPUT]

Opciones principales:
-i, --input       Archivo de entrada FASTA o secuencia cruda.
-s, --secuencia   Secuencia directa (codigo de una letra).
--stdin           Lee FASTA o secuencia cruda desde entrada estandar.
--id              Identificador para secuencia directa (default: secuencia).
-f, --formato     Formato de salida: texto, fasta, tsv o json.
-o, --output      Guarda la salida en archivo (si no, imprime en pantalla).
-h, --help        Muestra ayuda completa.

Ejemplos:
python -m intro_biologia.cli --secuencia AELMQK --id prot1
python -m intro_biologia.cli --input ../ejemplos/tres_proteinas.fasta --formato texto
python -m intro_biologia.cli --help

DESAFÍO VI: ¿Qué hace distintos a dos individuos de una especie? Propone una forma de corroborar tu respuesta realizando un diagrama de un posible método computacional para dicho fin.

Lo que hace distintos a dos individuos de una especie son principalmente sus secuencias de Aminoacidos (Protenoma) y sus secuencias de Nucleotidos (Genoma).
Diagrama del Método Computacional

El siguiente algoritmo en seudocódigo compara las secuencias de dos individuos para reportar sus diferencias exactas:

```text
ALGORITMO Encontrar_Diferencias_Biologicas:

  ENTRADA: 
    Individuo_1 (Sus listas de ADN y Proteínas)
    Individuo_2 (Sus listas de ADN y Proteínas)

  PREPARAR:
    Crear un "Reporte_de_Mutaciones" tabular vacío.

  PROCESO:
    POR CADA secuencia (ya sea un cromosoma o una proteína):
      
      POR CADA posición dentro de esa secuencia:
        Letra_A = Leer la letra del Individuo_1 en esta posición
        Letra_B = Leer la letra del Individuo_2 en esta posición
        
        SI Letra_A NO ES IGUAL a Letra_B:
          ANOTAR en "Reporte_de_Mutaciones": 
            - Nombre de la secuencia
            - Número de la posición (índice biológico)
            - Lo que tenía el Individuo 1 (Letra_A)
            - Lo que tenía el Individuo 2 (Letra_B)

  SALIDA:
    ENTREGAR el "Reporte_de_Mutaciones"
```    

🧗🏻‍♀️DESAFÍO VII (Ejercicio basado en Rosalind): Los motivos lineales son elementos de secuencia que comúnmente se encuentran en dominios intrínsecamente desordenados. Consisten, en promedio, de cinco residuos que determinan la función y participan en interacciones proteína-proteína (Podes leer más aquí).

Para permitir la presencia de sus formas variables, un motivo proteico se representa con una notación abreviada de la siguiente manera: [XY] significa "X o Y", y {X} significa "cualquier aminoácido excepto X". Por ejemplo, el motivo de N-glicosilación se escribe como N{P}[ST]{P}.

Puedes ver la descripción completa y las características de una proteína en particular mediante su identificador de acceso "uniprot_id" en la base de datos UniProt, insertando el número de identificación en:

http://www.uniprot.org/uniprot/uniprot_id

Alternativamente, puedes obtener la secuencia de una proteína en formato FASTA siguiendo el enlace:

http://www.uniprot.org/uniprot/uniprot_id.fasta

Por ejemplo, los datos de la proteína B5ZC00 se encuentran en: http://www.uniprot.org/uniprot/B5ZC00

Dado: Un máximo de 15 identificadores de la base de datos de proteínas UniProt

Retornar: Para cada proteína que posea el motivo de N-glicosilación, imprimir su identificador de acceso seguido de una lista de posiciones en la secuencia de la proteína donde se encuentra el motivo.

CLI (resumen breve)

Uso:
python -m intro_biologia.desafio7 --ids ID1 ID2 ID3 ... --motivo "N{P}[ST]{P}" [--formato texto|json] [-o OUTPUT]

Opciones principales:
--ids              Lista de hasta 15 IDs de UniProt para descargar y analizar.
--input            Archivo FASTA local con una o varias proteinas.
--secuencia        Secuencia directa de aminoacidos.
--stdin            Lee FASTA o secuencia cruda desde la entrada estandar.
--motivo           Motivo biologico estilo Rosalind, por ejemplo N{P}[ST]{P}.
--formato          Salida en texto o JSON.
-o, --output       Guarda la salida en un archivo.

Ejemplos:
python -m intro_biologia.desafio7 --ids P12345 Q8N158 O43521 --motivo "N{P}[ST]{P}" --formato texto
python -m intro_biologia.desafio7 --input ../ejemplos/tres_proteinas.fasta --motivo "AELMQK" --formato json
python -m intro_biologia.desafio7 --secuencia NVTSPNQT --motivo "N{P}[ST]{P}"

