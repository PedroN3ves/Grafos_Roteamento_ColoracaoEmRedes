## Parte 2 – Alocação de Canais Wi-Fi (Coloração de Grafos)

### 1. Apresentação do Problema e Complexidade (NP-Difícil)
Nesta parte do projeto, o objetivo é alocar canais de operação para uma rede de pontos de acesso Wi-Fi, garantindo que nenhum par de roteadores com sobreposição de sinal utilize o mesmo canal. O objetivo principal é descobrir o **número cromático $\chi(G)$** da rede, ou seja, a quantidade estritamente mínima de canais necessários para evitar qualquer interferência.

Este cenário modela o clássico **Problema de Coloração de Vértices**, que é classificado como **NP-Difícil**. Isto significa que, à medida que a rede cresce, o número de combinações sofre uma explosão combinatória e o tempo de solução cresce de forma exponencial. Não existe um algoritmo conhecido capaz de encontrar a solução ótima em tempo polinomial, o que torna abordagens de brute force inviáveis para redes de maior escala devido ao tempo de execução impraticável.

### 2. Abordagem Matemática e Algoritmo "Branch and Bound"
Para contornar esse problema e garantir o resultado matematicamente ótimo exigido, descartamos algoritmos gulosos simples e adotámos uma abordagem exata baseada no algoritmo de **Branch and Bound**.

O problema foi mapeado através de variáveis binárias booleanas, onde $x_{v,c} = 1$ se o roteador $v$ utilizar o canal $c$, e $0$ caso contrário. A árvore de busca opera sob duas restrições fundamentais:
1.  **Regra de Atribuição:** $\sum x_{v,c} = 1$. Cada roteador da rede tem de receber exatamente um canal, não podendo ficar inativo nem operar em dois canais simultaneamente.
2.  **Restrição de Conflito:** $x_{u,c} + x_{v,c} \le 1$. Para qualquer par de vizinhos ($u$ e $v$), a soma das suas variáveis para o mesmo canal $c$ nunca pode exceder 1. 

A grande vantagem desta modelação é o mecanismo de "**Poda**": sempre que o algoritmo encontra uma coloração válida, o número de cores utilizado torna-se o novo limite superior. Se, ao explorar um novo ramo da árvore, o algoritmo detectar que a equação de conflito falhou ou que já atingiu o limite superior de cores, ele aborta imediatamente essa ramificação.
Funcionando de forma análoga ao Backtraking, mas é mais eficiente justamente por otimizar a busca pelas podas.

### 3. Pseudocódigo do Funcionamento
O funcionamento do Branch and Bound pode ser resumido no pseudocódigo abaixo:

```text
Algoritmo ResolverColoracao(G, v, cores_usadas)
Require: G = (V, E) onde n = |V|, v ∈ V, cores_usadas

início:
Se v > n então
início
    Se cores_usadas < RecordeGlobal então
    início
        RecordeGlobal <-- cores_usadas
        salvar MelhorConfiguracaoAtual()
    Fim
    retornar
Fim

Se cores_usadas >= RecordeGlobal então
início
    retornar
Fim

para todo c ∈ {1, ..., n} fazer
início
    // Inequação de Conflito 
    Se CanalValidoParaVizinhos(G, v, c) então
    início
        
        Cor[v] <-- c
        
        novas_cores_usadas <-- max(cores_usadas, c)
        
        ResolverColoracao(G, v + 1, novas_cores_usadas)
        
        Cor[v] <-- ∅
        
    Fim
Fim
Fim
```

Ao contrário de algoritmos gulosos, o Branch and Bound garante encontrar o número cromático exato $\chi(G)$ porque realiza uma enumeração implícita de todo o espaço de soluções. O algoritmo apenas descarta os caminhos que são matematicamente comprovados como piores ou iguais ao recorde já estabelecido. Isso assegura que a solução ótima global nunca seja acidentalmente ignorada durante o processo de corte da árvore.
