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