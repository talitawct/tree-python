class Node:
    def __init__(self, caractere):
        self.caractere = caractere  # o caractere armazenado neste nó
        self.filhos = {}            # dicionário para os filhos

class Raiz:
    def __init__(self) :
        self.raiz = Node("")  # a raiz vazia
        self.palavras = {}

    def inserir_palavra(self, palavra):
        # insere uma palavra na trie
        nodo_atual = self.raiz

        for letra in palavra:
            if letra not in nodo_atual.filhos:              # se a letra não está na árvore, cria um novo nó
                nodo_atual.filhos[letra] = Node(letra)

            nodo_atual = nodo_atual.filhos[letra]           # avança para o próximo nó
        # adiciona o nó especial '*' ao final da palavra
        if '*' in nodo_atual.filhos:
            return f"palavra ja existente: {palavra}"

        nodo_atual.filhos['*'] = Node('*')
        self.palavras[palavra] = 0
        return f"palavra inserida: {palavra}"

    def consultar_palavra(self, palavra):
        # consulta uma palavra na trie e incrementa seu contador
        nodo_atual = self.raiz

        for letra in palavra:
            if letra not in nodo_atual.filhos:
                return f"palavra inexistente: {palavra}"

            nodo_atual = nodo_atual.filhos[letra]

        if '*' in nodo_atual.filhos:
            self.palavras[palavra] += 1
            return f"palavra existente: {palavra} {self.palavras[palavra]}"

        return f"palavra inexistente: {palavra}"

    # def palavras_mais_consultadas2(self):
    #     # retorna TODAS as palavras com seus contadores, destacando as mais consultadas
    #     if not self.palavras:
    #         return "trie vazia"
    #
    #     # encontra o maior número de consultas
    #     max_consultas = max(self.palavras.values())
    #
    #     # ordena todas as palavras em ordem alfabética
    #     todas_palavras = sorted(self.palavras.items())
    #
    #     # prepara a saída
    #     resultado = ["todas as palavras:"]
    #     for palavra, contador in todas_palavras:
    #         linha = f"{palavra}: {contador}"
    #         if contador == max_consultas:
    #             linha += " (mais consultada)"  # destaca as palavras mais consultadas
    #         resultado.append(linha)
    #
    #     return "\n".join(resultado)

    def palavras_mais_consultadas(self):
        # retorna as palavras mais consultadas
        if not self.palavras:
            return "trie vazia"

        # variáveis para armazenar o maior numero de consultas e as palavras correspondentes
        max_consultas = 0
        mais_consultadas = []


        for palavra, contador in self.palavras.items():
            if contador > max_consultas:
                max_consultas = contador
                mais_consultadas = [palavra]     # substitui a lista pelas novas palavras
            elif contador == max_consultas:      # encontrou outra palavra com o mesmo número de consultas
                mais_consultadas.append(palavra)

        # ordena a lista de palavras mais consultadas
        mais_consultadas.sort()

        # prepara a saida
        resultado = ["palavras mais consultadas:"]
        resultado.extend(mais_consultadas)
        resultado.append(f"numero de acessos: {max_consultas}")

        return "\n".join(resultado)

    def imprime_trie(self):
        if not self.raiz.filhos:
            return "trie vazia"

        resultado = []              # lista para armazenar a saída
        pilha = [(self.raiz, "")]   # pilha para o nó e prefixos

        while pilha:                # enquanto houver nós para processar
            nodo, prefixo = pilha.pop()

            # determina o rótulo do nó
            if nodo.caractere == "":
                rotulo = "letra: raiz"
            elif nodo.caractere == "*":
                resultado.append("letra: *")
                continue
            else:
                rotulo = f"letra: {nodo.caractere}"

            # coleta os filhos em ordem alfabética
            filhos = sorted(nodo.filhos.keys())
            filhos_str = " ".join(f"{f}" if f == "*" else f for f in filhos)


            linha = f"{rotulo} - {filhos_str}" if filhos else rotulo
            resultado.append(linha)

            # adiciona os filhos na pilha
            for filho in reversed(filhos):  # reverso para manter a ordem correta na pilha
                pilha.append((nodo.filhos[filho], prefixo + filho))

        return "\n".join(resultado)

    
