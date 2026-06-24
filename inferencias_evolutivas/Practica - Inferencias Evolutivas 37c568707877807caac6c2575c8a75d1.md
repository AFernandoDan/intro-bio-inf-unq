# Practica - Inferencias Evolutivas

> *>* bartmosca MGSGDAENGKKIFVQKCAQCHTYEVGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE
> 

🧗🏻‍♀️DESAFÍO I: Detalla las tácticas y/o metodologías que deberían utilizarse para darles una respuesta a los padres del niño. Dadas las secuencias de Mosca, humano y Moscahumano ¿Qué criterios se les ocurren para comparar las secuencias? ¿Qué resultados obtienen del análisis anterior? ¿Qué resultado esperaría obtener si utilizara el resto de las secuencias en el análisis? ¿Por qué?

Comparar la secuencia del `bartmosca` con secuencias de referencia de humano y mosca mediante **alineamiento de secuencias** y **análisis filogenético**. Determinar si la secuencia de `bartmosca` comparte mayor similitud (y por lo tanto un ancestro común más reciente) con la humana o con la de *Drosophila*. Mediante la idea de **clado** interpretar si `bartmosca` cae dentro del grupo de los humanos o forma un grupo intermedio.

Comparar el porcentaje de identidad de `bartmosca` frente a la secuencia humana y frente a la secuencia de Drosophila. Si la identidad con humano es claramente superior a la identidad con Drosophila, concluiremos que la secuencia es predominantemente humana.

Resultados esperados con las tres secuencias: `bartmosca` **se parece mucho más al humano (~93 %) que a la mosca (~77 %). Resultados esperados con todas las secuencias: `bartmosca` formará un clado con el humano, separado de la mosca y de los otros grupos.

🧗🏻‍♀️DESAFÍO II: Como vimos anteriormente existen algunos softwares optimizados para confeccionar alineamientos de secuencias. En particular hemos trabajado con [Clustal](https://www.ebi.ac.uk/Tools/msa/clustalo/) (Larkin et al. 2007). Confecciona el alineamiento para el punto I.

| Secuencia | Alineamiento (131 posiciones) |
| --- | --- |
| **Homo sapiens** | **-----------------------MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKN---KGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE** |
| **bartmosca** | **---------------------MGSGDAENGKKIFVQKCAQCHTYEVGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKN---KGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE** |
| **Drosophila melanogaster** | **-------------------MGVPAGDVEKGKKLFVQRCAQCHTVEAGGKHKVGPNLHGLIGRKTGQAAGFAYTDANKA---KGITWNEDTLFEYLENPKKYIPGTKMIFAGLKKPNERGDLIAYLKSATK-** |

| Comparación | Coincidencias | Posiciones comparables | % Identidad |
| --- | --- | --- | --- |
| bartmosca vs Humano | 97 | 105 | 92.38% |
| bartmosca vs Mosca | 80 | 106 | 75.47% |
| Humano vs Mosca | 80 | 104 | 76.92% |

En este sentido podemos concluir que la secuencia `bartmosca` tiene más similitud con el humano que con la mosca. Inclusive el alineamiento muestra que la mosca tiene más porcentaje de identidad con el humano que con la secuencia `bartmosca`.

Se adjunta el archivo de clustal de los alineamientos de las secuencias.

[clustalo-I20260621-180452-0947-21180432-p2m.aln-clustal_num](clustalo-I20260621-180452-0947-21180432-p2m.aln-clustal_num)

🧗🏻‍♀️DESAFÍO III: Mediante el uso del servidor de [IQtree](http://iqtree.cibiv.univie.ac.at/) (Trifinopoulos et al. 2016), confecciona los árboles filogenéticos para los alineamientos obtenidos en el punto II. Como vemos, el servidor nos permite elegir el modelo de sustitución ¿A qué se refiere? ¿Qué es el Bootstrap? 

¿De qué manera nos habla de la calidad de nuestro árbol? ¿Cómo influye el número de Bootstraps en el resultado? Interpreten los resultados obtenidos, mediante la visualización de los árboles con la herramienta [FigTree](http://tree.bio.ed.ac.uk/software/figtree/). ¿Es necesario realizar algún paso extra, previo a la interpretación del árbol? ¿Por qué?

El Modelo de Sustitución es el modelo matemático que estima la tasa de cambios evolutivos entre aminoácidos. IQ-TREE eligió automáticamente el modelo **Dayhoff + G4**.

El bootstrap es una técnica que evalúa la confiabilidad de cada rama del árbol mediante 1000 réplicas del alineamiento. El valor indica en qué porcentaje de réplicas se recuperó esa misma agrupación. Valores altos (≥90) indican ramas confiables. En nuestro árbol, la rama que une `bartmosca` **+ humano** tiene bootstrap **74** y la rama que agrupa a los animales tiene **84**. A mayor número de réplicas, mayor precisión en la estimación del soporte, aunque a partir de 1000 el beneficio es menor. Usamos 1000 réplicas.

Interpretamos el árbol muestra que `bartmosca` forma un clado con la secuencia humana (bootstrap 74), quedando la mosca como grupo hermano. Esto coincide con los resultados del alineamiento (92,4% de identidad con humano vs 75,5% con mosca). Por lo tanto, la secuencia del `bartmosca` es predominantemente humana.

Fue necesario enraizar el árbol previo a la interpretación utilizando como outgroup la secuencia de la bacteria (*Rhizobium*), para orientar correctamente las relaciones y poder definir clados de forma válida.