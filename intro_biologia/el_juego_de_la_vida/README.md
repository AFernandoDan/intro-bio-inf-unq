🧗🏻‍♀️DESAFIO I: Enumerá las diferencias que existen entre una célula procariota y eucariota.

Procariotas
    - fueron las primeras en aparecer
    - carecen de nucleo limitado por membrana
    - tienen pilis que les permiten adherirse y transmitir plasmidos
    - pueden tener flagelos que les dan movilidad
    
Eucariotas
    - tienen organelas membranosas
    - tienen nucleo
    - no tiene pared celular
    - son mas grandes y complejas que las procariotas

🧗🏻‍♀️DESAFIO II: Dado el código genético como se muestra en la tabla:

Código genético universal

Crea un script en Python que tome como argumento una secuencia proteica e imprima una cadena de ARN codificante. Podés usar de ejemplo el siguiente péptido (cadena corta de aminoácidos):

Sec1: ‘ATVEKGGKHKTGPNEKGKKIFVQKCSQCHTVLHGLFGRKTGQA'

Resumen breve de la solucion:
El script toma una secuencia de ADN, valida invariantes basicos (alfabeto A/C/G/T, longitud multiplo de 3 y ausencia de STOP interno) y devuelve la cadena de aminoacidos traducida.

Uso:
python .\intro_biologia\el_juego_de_la_vida\desafio2.py

🧗🏻‍♀️DESAFIO III: En muchos de los genes codificados en el ADN existe un motivo recurrente ubicado antes de la secuencia codificante del gen que direcciona la unión de la ARN Polimerasa II, la proteína encargada de copiar el ADN a un ARN mensajero. Ésta secuencia denominada caja TATA (consistente en una secuencia de nucleótidos 'TATAAA') se encuentra presente en lo que se denomina región promotora de diversos genes, en organismos de todos los reinos (Smale and Kadonaga 2003; Lifton et al. 1978)

👉 Creá un script en Python que, tomando como input un archivo con una secuencia de ADN, permita identificar las regiones promotoras de un gen, considerando que tal región comienza y termina con la caja TATA.

Resumen breve de la solucion:
El script lee una secuencia (texto o FASTA), busca todas las cajas TATAAA y reporta regiones promotoras armadas por pares consecutivos, informando secuencia e indices de inicio/fin.

Uso:
python .\intro_biologia\el_juego_de_la_vida\desafio3.py .\ejemplos\proteina_tata.fasta

🧗🏻‍♀️DESAFIO IV: Vamos a divertirnos un poco mientras aprendemos, ¡y no hay mejor modo de hacer esto que jugando!

👉 Diseñá un juego rpg interactivo sobre la expresión génica que se muestre en la consola (que se ejecute mediante CLI de manera similar a lo visto en el Bashaton). Tené en cuenta que lo vas a tener que compartir con la clase.

¡El cielo es límite, a divertirse!