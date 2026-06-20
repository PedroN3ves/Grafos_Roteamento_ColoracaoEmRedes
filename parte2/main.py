import os
from branch_bound import SolucionadorColoracao

def carregar_grafo_wifi(caminho_ficheiro):
    with open(caminho_ficheiro, 'r', encoding='utf-8') as f:
        linhas = [l.strip().split('\t') for l in f if l.strip()]
    
    # A primeira linha contém o número de vértices e arestas
    n_v, n_a = map(int, linhas[0])
    
    # Inicializar matriz de adjacência preenchida com zeros
    matriz = [[0] * n_v for _ in range(n_v)]
    
    # Preencher as ligações (grafo não-direcionado)
    for i in range(1, len(linhas)):
        u, v = int(linhas[i][0]), int(linhas[i][1])
        matriz[u][v] = 1
        matriz[v][u] = 1 
        
    return n_v, matriz

def auditar_coloracao(matriz, num_vertices, cores):
    """Garante que nenhum par de APs adjacentes usa o mesmo canal."""
    for i in range(num_vertices):
        for j in range(num_vertices):
            if matriz[i][j] == 1 and cores[i] == cores[j]:
                return False
    return True

def executar_parte2(ficheiro_entrada, ficheiro_saida):
    if not os.path.exists(ficheiro_entrada):
        print(f"Aviso: O ficheiro {ficheiro_entrada} não foi encontrado.")
        return

    n_v, matriz = carregar_grafo_wifi(ficheiro_entrada)
    
    # Chamar a classe criada pela Pessoa 2
    solucionador = SolucionadorColoracao(matriz, n_v)
    num_cores, coloracao = solucionador.executar()
    
    # Validação de segurança
    if not auditar_coloracao(matriz, n_v, coloracao):
        print(f"ERRO CRÍTICO: A coloração para {ficheiro_entrada} falhou na validação!")
        return
        
    algoritmo = "Branch and Bound"
    justificativa = "Garante encontrar o numero cromatico exato explorando o espaco de solucoes e podando ramos subotimos. Abordagem exata e ideal para problemas NP-Dificil."
    
    str_coloracao = " ".join([f"{i}={cor}" for i, cor in enumerate(coloracao)])
    
    with open(ficheiro_saida, 'w', encoding='utf-8') as f:
        f.write(f"ALGORITMO: {algoritmo}\n")
        f.write(f"JUSTIFICATIVA: {justificativa}\n")
        f.write(f"NUM_CORES: {num_cores}\n")
        f.write(f"COLORACAO: {str_coloracao}\n")
    
    print(f"Sucesso! {ficheiro_saida} gerado com {num_cores} cores.")

if __name__ == "__main__":
    pasta_saida = r"C:\Users\Arthur\Downloads\projetoGrafos\Grafos_Roteamento_ColoracaoEmRedes\parte2\saida"

    executar_parte2(
        r"C:\Users\Arthur\Downloads\projetoGrafos\Grafos_Roteamento_ColoracaoEmRedes\parte2\grafo_wifi_p.txt",
        os.path.join(pasta_saida, "saida_parte2_p.txt")
    )

    executar_parte2(
        r"C:\Users\Arthur\Downloads\projetoGrafos\Grafos_Roteamento_ColoracaoEmRedes\parte2\grafo_wifi_m.txt",
        os.path.join(pasta_saida, "saida_parte2_m.txt")
    )