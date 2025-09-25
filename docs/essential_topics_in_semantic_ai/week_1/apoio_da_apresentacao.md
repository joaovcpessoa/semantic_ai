Este documento apresenta um resumo do artigo "Early-Exit Criteria for Edge Semantic Segmentation" e da apresentação "Early-Exit Criteria for Edge Semantic Segmentation" do IEEE International Conference on Machine Learning for Communication and Networking (ICMLCN) 2025. Ambos os materiais abordam a otimização de Redes Neurais Profundas com Saída Antecipada (EE-DNNs) para segmentação semântica em ambientes com recursos limitados e sensíveis à latência, como dispositivos de borda e nuvem.

## Introdução e Contexto

As EE-DNNs são redes neurais multi-saída projetadas para dividir o processamento entre dispositivos locais, de borda e de nuvem, utilizando camadas de saída auxiliares. O principal desafio é implementar soluções de segmentação semântica em cenários com recursos limitados e sensíveis à latência, devido à falta de um critério de saída eficiente para interromper o processo de inferência mais cedo. A segmentação semântica, ao contrário da classificação de imagens, foca na classificação em nível de pixel, atribuindo informações semânticas a regiões específicas de uma imagem.

## Critério de Saída Baseado em Entropia Normalizada (NE)

Tradicionalmente, o critério de Entropia Normalizada (NE) é usado em classificação de imagens, onde uma baixa entropia indica alta confiança na saída da rede. Se a NE estiver abaixo de um limiar, a inferência pode ser concluída em uma saída antecipada. No entanto, a adaptação do NE para segmentação semântica apresenta desafios significativos:

• Complexidade: Enquanto o NE é O(n) na classificação de imagens, torna-se O(n³) na segmentação semântica, pois depende simultaneamente do tamanho da imagem e do número de classes.

• Restrições de Funções de Perda: O NE exige que a função de perda minimize a entropia das saídas, tornando-o incompatível com funções de perda baseadas em região (como Lovász-Softmax), que não minimizam a entropia.

## Critério de Saída Baseado em Região (VI)

Para superar as limitações do NE, os autores propõem um critério de saída baseado em região, utilizando a Variação da Informação (VI) como métrica. Este critério funciona comparando as diferenças entre as segmentações geradas por saídas antecipadas consecutivas. Se as diferenças forem insignificantes, a rede pode concluir a inferência.

As vantagens do critério baseado em VI incluem:

• Melhor Escalabilidade: A complexidade do VI é O(n²), dependendo do tamanho da imagem ou do número de classes, mas não de ambos simultaneamente, o que o torna mais escalável que o NE para segmentação semântica.

• Compatibilidade: Funciona bem com diferentes funções de perda, incluindo as baseadas em distribuição e em região, sem restringir a escolha durante o treinamento.

• Eficiência: O tempo de execução do VI permanece quase constante com o aumento do número de classes, ao contrário do NE.

## Configuração Experimental

Os experimentos foram realizados utilizando o dataset Pascal VOC 2012 para segmentação semântica, contendo 2.913 imagens coloridas com 6.929 objetos em 20 classes. A divisão foi de 50% para treino, 20% para validação e 30% para teste. A rede neural utilizada como backbone foi uma DeepLabV3 pré-treinada, com 7 saídas antecipadas espaçadas uniformemente em termos de FLOPs. O treinamento foi realizado por 250 épocas com um batch size de 32, utilizando o framework PyTorch.

## Resultados Experimentais

Os resultados demonstram a superioridade do critério baseado em VI:

• Economia de FLOPs: O critério baseado em VI economiza entre 680 milhões e 2.62 bilhões de operações de ponto flutuante por imagem em média, mantendo um desempenho semelhante em termos de mIoU (Interseção sobre União Média) em comparação com o NE.

• Distribuição de Inferências: O VI utiliza melhor as saídas intermediárias, distribuindo as inferências de forma mais eficiente e reduzindo a necessidade de enviar imagens para processamento nas camadas finais da rede (na nuvem).

• Tempo de Execução: Para 100 classes, o NE leva aproximadamente 122ms, enquanto o VI se mantém em torno de 8,7ms, evidenciando sua melhor escalabilidade e eficiência.

• Latência: Em cenários de processamento paralelo, o VI supera o NE em termos de FLOPs a partir de uma taxa de desempenho de 0,88, e o NE subutiliza as saídas intermediárias, aumentando a latência de comunicação ao enviar mais dados para a nuvem.

## Conclusões e Trabalhos Futuros

O estudo conclui que o critério de saída baseado em região, utilizando VI, é mais adequado para segmentação semântica em EE-DNNs, oferecendo melhor escalabilidade, compatibilidade com diversas funções de perda e maior eficiência computacional. Os trabalhos futuros incluem a investigação de outras métricas de saída, o desenvolvimento de critérios sensíveis à rede que considerem os requisitos de transmissão de dados e a adaptação dinâmica de limiares com base no estado da rede. Além disso, sugere-se estender o conceito para outras tarefas de visão computacional, como detecção de objetos ou estimação de pose.

