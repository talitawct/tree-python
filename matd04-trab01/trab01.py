from raiz import Raiz

# inicializa a trie
raiz = Raiz()

while True:
    var = input().strip() # remove espaços em branco do input

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

    elif var == 'p':  # imprimir a trie
        resultado = raiz.imprime_trie()
        print(resultado)

    elif var == 'e':  # sair do programa
        break
