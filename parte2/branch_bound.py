class SolucionadorColoracao:
    def __init__(self, matriz_adjacencia, num_vertices):
        self.matriz_adjacencia = matriz_adjacencia
        self.num_vertices = num_vertices
        self.melhor_recorde = float('inf')
        self.melhor_configuracao = []
        self.cores = [0] * num_vertices 

    def canal_valido_para_vizinhos(self, vertice, cor_testada):
        """
        Verifica a inequação de conflito usando a matriz de adjacência.
        """
        for vizinho in range(self.num_vertices):
            # Se houver conexão e o vizinho já usar a cor testada, falha.
            if self.matriz_adjacencia[vertice][vizinho] == 1:
                if self.cores[vizinho] == cor_testada:
                    return False
        return True

    def resolver_coloracao(self, vertice, cores_usadas):
        if vertice == self.num_vertices:
            if cores_usadas < self.melhor_recorde:
                self.melhor_recorde = cores_usadas
                self.melhor_configuracao = list(self.cores)
            return

        if cores_usadas >= self.melhor_recorde:
            return

        for c in range(1, self.num_vertices + 1):
            if c >= self.melhor_recorde:
                break

            if self.canal_valido_para_vizinhos(vertice, c):
                self.cores[vertice] = c
                novas_cores_usadas = max(cores_usadas, c)
                self.resolver_coloracao(vertice + 1, novas_cores_usadas)
                self.cores[vertice] = 0

    def executar(self):
        self.resolver_coloracao(0, 0)
        return self.melhor_recorde, self.melhor_configuracao