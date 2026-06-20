# Comparativo Final: Roteamento vs. Coloração em Redes

## 1. Complexidade e Natureza dos Problemas
Na primeira parte do projeto, lidamos com o roteamento de backbone, focado em achar o caminho de menor custo em um grafo direcionado. Como esse é um problema resolvível em tempo polinomial (P), conseguimos aplicar o algoritmo de Dijkstra direto nos cenários com pesos positivos. Já para o grafo que tinha custos negativos (representando os ganhos dos SLAs), usamos o Bellman-Ford para garantir que o cálculo fechasse corretamente.

Por outro lado, a alocação de canais Wi-Fi da segunda parte cai no clássico Problema de Coloração de Vértices, que é NP-Difícil. Como o número de combinações explode muito rápido e algoritmos gulosos quase nunca entregam a solução matematicamente ótima (o número cromático mínimo), a nossa melhor saída foi implementar uma busca exata usando **Branch and Bound**.

## 2. Escolha dos Algoritmos e Validação
- **Roteamento:** A troca do Dijkstra pelo Bellman-Ford no grafo médio foi uma obrigação matemática. O Dijkstra parte do princípio de que o custo do caminho sempre aumenta a cada nova aresta, o que simplesmente quebra a lógica quando temos pesos negativos. O Bellman-Ford resolve isso relaxando as arestas $V-1$ vezes, propagando direito os "descontos" dos SLAs.
- **Coloração (Wi-Fi):** O Branch and Bound se mostrou bem eficiente para os tamanhos de rede que testamos. O segredo dele é a técnica de poda: o código corta a busca na hora se perceber que já usou mais cores que o recorde atual ou se dois roteadores vizinhos pegarem o mesmo canal. Além disso, a função de validação que construímos serviu para auditar a matriz final e provar que a restrição de interferência zero foi realmente cumprida.

## Conclusão
A prática deixou clara a diferença nas abordagens para gerenciar redes. Para o roteamento de pacotes de dados, precisamos de algoritmos super rápidos e determinísticos que rodem em tempo real. Já na hora de planejar a infraestrutura física — como configurar os canais de rádio-frequência do Wi-Fi —, faz mais sentido gastar processamento com algoritmos combinatórios mais pesados, desde que eles garantam que a rede vá funcionar sem interferências.