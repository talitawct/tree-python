class Node:
    def __init__(self, caractere):
        self.caractere = caractere
        self.end_of_word = False
        self.left = None
        self.right = None
        self.count = 0

class Raiz:
    def __init__(self):
        self.raiz = None

    def inserir_palavra(self, palavra):
        self.raiz, inseriu = self._inserir_irmao(self.raiz, palavra, 0)
        if inseriu:
            return f'palavra inserida: {palavra}'
        else:
            return f'palavra ja existente: {palavra}'

    def _inserir_irmao(self, no, palavra, i):
        # Se não houver nó na lista de irmãos, cria
        if no is None:
            novo = Node(palavra[i])
            if i == len(palavra) - 1:
                # Última letra: insere o nó terminador como filho
                novo.left = self._inserir_terminacao(None)
                return (novo, True)
            else:
                novo.left, inseriu = self._inserir_irmao(None, palavra, i + 1)
                return (novo, inseriu)

        # Compara o caractere a inserir com o caractere do nó corrente
        if palavra[i] < no.caractere:
            # Deve ser inserido antes do nó corrente
            novo = Node(palavra[i])
            if i == len(palavra) - 1:
                novo.left = self._inserir_terminacao(None)
            else:
                novo.left, inseriu = self._inserir_irmao(None, palavra, i + 1)
            novo.right = no
            return (novo, True)
        elif palavra[i] > no.caractere:
            # Procura inserir na lista de irmãos à direita
            no.right, inseriu = self._inserir_irmao(no.right, palavra, i)
            return (no, inseriu)
        else:
            # Encontrou o nó com o mesmo caractere
            if i == len(palavra) - 1:
                # Último caractere: precisamos inserir o terminador se ainda não existir
                if self._tem_terminacao(no.left):
                    # Palavra já existe
                    return (no, False)
                else:
                    no.left = self._inserir_terminacao(no.left)
                    return (no, True)
            else:
                no.left, inseriu = self._inserir_irmao(no.left, palavra, i + 1)
                return (no, inseriu)

    def _inserir_terminacao(self, no):
        if no is None:
            return Node('*')
        # Se o primeiro nó já é '*', nada a fazer
        if no.caractere == '*':
            return no
        # Se '*' deve vir antes do nó atual
        if '*' < no.caractere:
            novo = Node('*')
            novo.right = no
            return novo
        else:
            no.right = self._inserir_terminacao(no.right)
            return no

    def _tem_terminacao(self, no):
        atual = no
        while atual:
            if atual.caractere == '*':
                return True
            atual = atual.right
        return False

    def consultar_palavra(self, palavra):
        atual = self.raiz
        i = 0

        while atual and i < len(palavra):
            # Procura o nó com o caractere palavra[i] na lista de irmãos
            while atual and palavra[i] > atual.caractere:
                atual = atual.right
            if not atual or palavra[i] != atual.caractere:
                return f'palavra inexistente: {palavra}'
            # Se encontrou, avança para os filhos (próximo caractere)
            i += 1
            if i < len(palavra):
                atual = atual.left

        if atual:
            # Agora procuramos o nó terminador '*' entre os filhos de atual
            atual = atual.left
            while atual and atual.caractere != '*':
                atual = atual.right
            if atual and atual.caractere == '*':
                atual.count += 1
                return f'palavra existente: {palavra} {atual.count}'

        return f'palavra inexistente: {palavra}'

    def imprimir_trie(self):
        def pre_ordem(no):
            if no is None:
                return ""
            # Formata o nó atual
            linha = f"letra: {no.caractere} fesq: {no.left.caractere if no.left else 'nil'} fdir: {no.right.caractere if no.right else 'nil'}\n"
            # Primeiro imprime os filhos (esquerda) e depois os irmãos (direita)
            return linha + pre_ordem(no.left) + pre_ordem(no.right)
        
        if not self.raiz:
            return "trie vazia"
        return pre_ordem(self.raiz).strip()

    def palavras_mais_consultadas(self):
        if not self.raiz:
            return "trie vazia"

        palavras = []

        def coletar(no, prefixo):
            if no is None:
                return
            # Se o nó é terminador, a palavra está completa
            if no.caractere == '*':
                palavras.append((prefixo, no.count))
            else:
                # Acumula o caractere no prefixo e desce para os filhos
                nova_prefixo = prefixo + no.caractere
                coletar(no.left, nova_prefixo)
            # Independentemente se é terminador ou não, percorre os irmãos mantendo o mesmo prefixo
            coletar(no.right, prefixo)

        coletar(self.raiz, "")

        if not palavras:
            return "trie vazia"

        # Determina o maior número de acessos
        max_acessos = max(count for (_, count) in palavras)
        # Filtra as palavras que possuem esse contador
        mais_consultadas = [palavra for (palavra, count) in palavras if count == max_acessos]
        mais_consultadas.sort()  # em ordem alfabética

        # Monta a string de saída
        saida = "palavras mais consultadas:\n"
        for palavra in mais_consultadas:
            saida += palavra + "\n"
        saida += f"numero de acessos: {max_acessos}"
        return saida

    def palavras_por_prefixo(self, prefixo):
        if not self.raiz:
            return "trie vazia"

        # Busca o nó correspondente ao último caractere do prefixo
        no_prefixo = self._buscar_prefixo(self.raiz, prefixo, 0)
        saida = f"palavras com prefixo: {prefixo}"
        if no_prefixo is None:
            # Prefixo não encontrado: retorna apenas a linha de cabeçalho
            return saida

        # Coleta todas as palavras a partir dos filhos do nó encontrado
        palavras = self._coletar_palavras(no_prefixo.left, prefixo)
        palavras.sort()

        if palavras:
            saida += "\n" + "\n".join(palavras)
        return saida

    def _buscar_prefixo(self, no, prefixo, i):
        if no is None:
            return None
        current = no
        while current:
            if current.caractere == prefixo[i]:
                if i == len(prefixo) - 1:
                    return current
                else:
                    return self._buscar_prefixo(current.left, prefixo, i + 1)
            elif prefixo[i] < current.caractere:
                return None
            else:
                current = current.right
        return None

    def _coletar_palavras(self, no, palavra):
        resultado = []
        current = no
        while current:
            if current.caractere == '*':
                resultado.append(palavra)
            else:
                resultado.extend(self._coletar_palavras(current.left, palavra + current.caractere))
            current = current.right
        return resultado


    def palavras_por_sufixo(self, sufixo):
        if not self.raiz:
            return "trie vazia"
        
        # Coleta todas as palavras armazenadas na trie
        todas_palavras = self._coletar_palavras(self.raiz, "")
        # Filtra somente aquelas que terminam com o sufixo informado
        palavras_sufixo = [palavra for palavra in todas_palavras if palavra.endswith(sufixo)]
        palavras_sufixo.sort()  # ordena alfabeticamente
        
        saida = f"palavras com sufixo: {sufixo}"
        if palavras_sufixo:
            saida += "\n" + "\n".join(palavras_sufixo)
        return saida