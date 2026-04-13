def comparar_individuos_simple(ind1, ind2):
    """
    Compara dos individuos y genera un reporte tabular simple
    con las diferencias encontradas, con columnas bien alineadas.
    """
    header = f"{'Secuencia':<12} {'Posicion':<10} {'Valor_Ind_1':<15} {'Valor_Ind_2':<15} {'Info'}"
    lineas_reporte = [header]
    
    # 1. Analizar el Genoma
    for i, (seq1, seq2) in enumerate(zip(ind1["genoma"], ind2["genoma"])):
        nombre_secuencia = f"chr{i+1}"
        
        for pos, (letra1, letra2) in enumerate(zip(seq1, seq2)):
            if letra1 != letra2:
                pos_biologica = pos + 1 
                # Aplicamos el mismo ancho fijo a los datos
                linea = f"{nombre_secuencia:<12} {pos_biologica:<10} {letra1:<15} {letra2:<15} Mutación en ADN"
                lineas_reporte.append(linea)

    # 2. Analizar el Proteoma 
    for i, (seq1, seq2) in enumerate(zip(ind1["proteoma"], ind2["proteoma"])):
        nombre_secuencia = f"prot{i+1}"
        
        for pos, (letra1, letra2) in enumerate(zip(seq1, seq2)):
            if letra1 != letra2:
                pos_biologica = pos + 1
                linea = f"{nombre_secuencia:<12} {pos_biologica:<10} {letra1:<15} {letra2:<15} Mutación en Proteína"
                lineas_reporte.append(linea)

    return "\n".join(lineas_reporte)

# EJECUCIÓN DE PRUEBA

individuo_A = {
    "genoma": ["ATCGGTA", "GGCTAG"], 
    "proteoma": ["MLPGLA", "MKWTC"]  
}

individuo_B = {
    "genoma": ["ATCCGTA", "GGCTAG"], 
    "proteoma": ["MLPGLA", "MKWAC"]  
}

reporte = comparar_individuos_simple(individuo_A, individuo_B)
print(reporte)