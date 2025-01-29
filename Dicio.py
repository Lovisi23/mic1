# Dicionário de Instruções do MIC-1 (representação binária)
inst = {
    'LODD': '0000',  # Carregar valor de memória para registrador
    'STOD': '0001',  # Armazenar valor de registrador na memória
    'ADDD': '0010',  # Somar valores de dois registradores
    'SUBD': '0011',  # Subtrair valores de dois registradores
    'JPOS': '0100',  # Pular para endereço se registrador for positivo
    'JZER': '0101',  # Pular para endereço se registrador for zero
    'JNEG': '1100',  # Pular para endereço se registrador for negativo
    'JUMP': '0110',  # Pular para endereço incondicionalmente
    'LOCO': '0111',  # Carregar valor imediato para registrador
    'LODL': '1000',  # Carregar valor de memória em posição de registrador + offset
    'STODL': '1001',  # Armazenar valor de registrador em posição de memória + offset
    'ADDL': '1010',  # Somar valor de registrador e memória + offset
    'PUSHI': '1011',  # Empilhar valor imediato na memória
    'POPI': '1101',  # Desempilhar valor da memória para registrador
    'INSP': '1111'   # Incrementar o ponteiro de pilha
}