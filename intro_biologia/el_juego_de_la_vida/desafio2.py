codigo_genetico_adn = {
    # Fila T
    'TTT': 'Phe', 'TTC': 'Phe', 'TTA': 'Leu', 'TTG': 'Leu',
    'TCT': 'Ser', 'TCC': 'Ser', 'TCA': 'Ser', 'TCG': 'Ser',
    'TAT': 'Tyr', 'TAC': 'Tyr', 'TAA': 'STOP', 'TAG': 'STOP',
    'TGT': 'Cys', 'TGC': 'Cys', 'TGA': 'STOP', 'TGG': 'Try',
    
    # Fila C
    'CTT': 'Leu', 'CTC': 'Leu', 'CTA': 'Leu', 'CTG': 'Leu',
    'CCT': 'Pro', 'CCC': 'Pro', 'CCA': 'Pro', 'CCG': 'Pro',
    'CAT': 'His', 'CAC': 'His', 'CAA': 'Gln', 'CAG': 'Gln',
    'CGT': 'Arg', 'CGC': 'Arg', 'CGA': 'Arg', 'CGG': 'Arg',
    
    # Fila A
    'ATT': 'Iso', 'ATC': 'Iso', 'ATA': 'Iso', 'ATG': 'Met',
    'ACT': 'Thr', 'ACC': 'Thr', 'ACA': 'Thr', 'ACG': 'Thr',
    'AAT': 'Asn', 'AAC': 'Asn', 'AAA': 'Lys', 'AAG': 'Lys',
    'AGT': 'Ser', 'AGC': 'Ser', 'AGA': 'Arg', 'AGG': 'Arg',
    
    # Fila G
    'GTT': 'Val', 'GTC': 'Val', 'GTA': 'Val', 'GTG': 'Val',
    'GCT': 'Ala', 'GCC': 'Ala', 'GCA': 'Ala', 'GCG': 'Ala',
    'GAT': 'Asp', 'GAC': 'Asp', 'GAA': 'Glu', 'GAG': 'Glu',
    'GGT': 'Gly', 'GGC': 'Gly', 'GGA': 'Gly', 'GGG': 'Gly'
}

def validar_invariantes_adn(secuencia):
    """Verifica los invariantes de la secuencia de entrada (ADN)."""
    
    # Invariante 1: Longitud y Módulo
    if len(secuencia) % 3 != 0:
        raise ValueError("Invariante roto: La secuencia de ADN debe tener una longitud múltiplo de 3.")
        
    # Invariante 2: Alfabeto Estricto
    bases_validas = {'A', 'C', 'G', 'T'}
    if not all(base in bases_validas for base in secuencia):
        raise ValueError("Invariante roto: La secuencia contiene caracteres inválidos. Solo se permiten A, C, G, T.")

def validar_invariantes_aminoacidos(cadena_aminoacidos):
    """Verifica los invariantes de la secuencia de salida (Proteína)."""
    
    # Invariante 3: Carencia de Paradas Internas
    # Comprobamos si hay un 'STOP' en cualquier lugar menos en la última posición [:-1]
    if 'STOP' in cadena_aminoacidos[:-1]:
        raise ValueError("Invariante roto: Se encontró un codón de parada (STOP) en el medio de la secuencia.")

def traducir_adn_a_aminoacidos(secuencia):
    # 1. Validar la entrada
    validar_invariantes_adn(secuencia)
    
    # 2. Cortar en codones
    codones = [secuencia[i:i+3] for i in range(0, len(secuencia), 3)]
    
    # 3. Mapear al diccionario
    cadena_aminoacidos = list(map(codigo_genetico_adn.get, codones))
    
    # 4. Validar la salida biológica
    validar_invariantes_aminoacidos(cadena_aminoacidos)
    
    return cadena_aminoacidos

def serializar_cadena_aminoacidos(aminoacidos):
    return '-'.join(aminoacidos)

if __name__ == "__main__":
    # leemos la secuencia de ADN y aplicamos .upper() para evitar errores si el usuario usa minúsculas
    secuencia = input("Ingrese la secuencia de ADN: ").upper()
    
    try:
        # obtenemos la cadena de aminoácidos
        aminoacidos = traducir_adn_a_aminoacidos(secuencia)
        # imprimimos la cadena serializada
        print("La cadena de aminoácidos es:", serializar_cadena_aminoacidos(aminoacidos))
    except ValueError as error:
        # Atrapamos las violaciones de los invariantes
        print(f"Error de validación -> {error}")