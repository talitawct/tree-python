from raiz import Raiz

# inicializa a trie
raiz = Raiz()

while True:
    var = input().strip()

    if var == 'i':  # Inserir palavras
        word = input().strip()
        resultado = raiz.inserir_palavra(word)
        print(resultado)

    elif var == 'c':  # consultar palavras
        word = input().strip()
        resultado = raiz.consultar_palavra(word)
        print(resultado)

    elif var == 'f':  # palavras mais consultadas
        resultado = raiz.palavras_mais_consultadas()
        print(resultado)

    elif var == 'r':
        word = input().strip()
        resultado = raiz.palavras_por_prefixo(word)
        print(resultado)

    elif var == 's':
        word = input().strip()
        resultado = raiz.palavras_por_sufixo(word)
        print(resultado)
        
    elif var == 'p':  # imprimir a trie
        resultado = raiz.imprimir_trie()
        print(resultado)

    elif var == 'e':  # sair do programa
        break