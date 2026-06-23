# Grafos: Roteamento e Coloração em Redes

## Parte 1 – Roteamento de Backbone (Caminho Mínimo)

### 1. Apresentação do Problema
Na primeira parte do projeto, o foco é o roteamento de backbone, que consiste em encontrar a rota de menor custo para a transmissão de dados em um grafo direcionado. Ao contrário da alocação de canais da Parte 2, este é um problema resolvível em tempo polinomial (P). O desafio central desta etapa é lidar com as diferentes naturezas matemáticas dos pesos das conexões (arestas), o que dita a viabilidade e a escolha do algoritmo utilizado.

### 2. Abordagem Algorítmica (Dijkstra e Bellman-Ford)
Para garantir o cálculo exato do caminho de menor custo em diferentes cenários, o sistema faz o uso de dois algoritmos distintos com base na topologia:

* Algoritmo de Dijkstra: É o método de caminho mínimo mais eficiente para grafos sem circuitos de custo negativo, utilizando uma estratégia gulosa com complexidade ótima. Ele é aplicado em redes onde todos os custos de enlace são estritamente positivos.
* Algoritmo de Bellman-Ford: O algoritmo de Dijkstra não é aplicável a grafos com pesos negativos. Em alguns dos grafos analisados, existem custos negativos que representam os ganhos e descontos associados aos SLAs (Service Level Agreements) na rede. O Bellman-Ford é utilizado aqui pela capacidade de tratar custos negativos (SLA) via relaxamento iterativo.

### 3. Justificativa das Escolhas
A necessidade de alterar entre os dois algoritmos ocorre por uma obrigação matemática. O Dijkstra parte do princípio de que o custo acumulado de um caminho sempre aumenta a cada nova aresta percorrida. Quando a rede possui pesos negativos (descontos de SLA), essa lógica é quebrada. Nesses casos, o algoritmo de Bellman-Ford garante que a rota feche corretamente ao relaxar todas as arestas do grafo V-1 vezes, propagando todos os descontos aplicáveis sem perder a precisão do cálculo final.

---

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

---

## Instruções de Execução

O projeto foi desenvolvido em Python 3. Certifique-se de ter o Python 3 instalado no seu ambiente.

### Parte 1 - Roteamento (Backbone)
Para gerar as rotas de menor custo, navegue até o diretório `parte1` e execute o solver:

```bash
cd parte1
python3 solver.py
```

Os arquivos `saida_parte1_p.txt` e `saida_parte1_m.txt` serão gerados automaticamente no mesmo diretório.

### Parte 2 - Coloração de Grafos (Wi-Fi)
Para gerar a alocação de canais, navegue até o diretório `parte2` e execute o script principal:

```bash
cd parte2
python3 main.py
```

Os arquivos `saida_parte2_p.txt` e `saida_parte2_m.txt` serão gerados automaticamente no mesmo diretório, assegurando o número cromático mínimo através de Branch and Bound.

---
Grupo
Ana Leticia Nobre da Silva
Arthur Vinicius Fernandes de Carvalho
Pedro Henrique Oliveira Neves
