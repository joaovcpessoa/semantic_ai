# Critérios de Early-Exit para Segmentação Semântica em Edge

## Introdução e Problema

Redes Neurais Profundas com Saída Antecipada (Early-Exit Deep Neural Networks - EE-DNNs) são arquiteturas multi-saída projetadas para ambientes com recursos limitados e sensíveis à latência, como dispositivos de borda (edge devices). Elas utilizam camadas de saída auxiliares para dividir o processamento entre dispositivos locais, de borda e de nuvem. No contexto da segmentação semântica, que consiste em particionar uma imagem em regiões semanticamente relevantes e atribuir-lhes informações (e.g., legendas), a literatura carece de uma política de saída eficiente para interromper o processo de inferência mais cedo, otimizando o uso de recursos e reduzindo a latência.

O critério de saída convencional para EE-DNNs é baseado na Entropia Normalizada (Normalized Entropy - NE), onde uma baixa NE indica alta confiança na saída gerada. No entanto, adaptar este critério da classificação de imagens para a segmentação semântica apresenta desafios significativos. Enquanto na classificação de imagens a complexidade do critério baseado em NE é O(n) (linear com o número de classes), na segmentação semântica ela se torna O(n³) porque exige o cálculo da NE para cada pixel, tornando-a dependente do tamanho da imagem e do número de classes simultaneamente. Além disso, o critério baseado em NE pode restringir a escolha de funções de perda durante o treinamento, pois exige a minimização da entropia da saída.

## Contribuições do Artigo

Para preencher essa lacuna, o artigo apresenta duas contribuições principais:

1. Adaptação do critério de saída baseado em Entropia Normalizada (NE): Os autores adaptam o critério baseado em NE da classificação de imagens para a segmentação semântica e analisam suas deficiências.

2. Proposta de um critério de saída baseado em região: É proposto um novo critério de saída baseado em região que compara as diferenças de segmentação entre saídas geradas em saídas antecipadas consecutivas. Este critério é implementado usando a Variação da Informação (Variation of Information - VI) como métrica de saída.

As análises dos autores revelam que a abordagem baseada em região é mais adequada para a segmentação semântica, pois explora as saídas antecipadas intermediárias de forma mais eficiente. Os experimentos demonstram que uma EE-DNN baseada em região oferece o mesmo desempenho de Interseção sobre União Média (mIoU) que uma EE-DNN com NE, economizando em média pelo menos 630 milhões de operações de ponto flutuante por imagem.

## Critério de Saída Baseado em Região

O objetivo do treinamento de segmentação semântica é minimizar as discrepâncias entre as segmentações da DNN e a verdade fundamental. O critério de saída baseado em região proposto explora o fato de que as diferenças entre as saídas de camadas antecipadas consecutivas diminuem à medida que o processamento avança para camadas mais profundas. Se duas saídas consecutivas (Yi-1 e Yi) são muito semelhantes, significa que a rede já está confiante em sua segmentação, e o processo de inferência pode ser interrompido.

Para implementar este critério, os autores utilizam a Variação da Informação (VI) como métrica de saída. A VI mede as mudanças de informação entre dois agrupamentos (clusterings), que neste caso são as segmentações geradas por saídas antecipadas consecutivas. A complexidade computacional da VI é O(n²), o que a torna mais escalável do que a NE para segmentação semântica, pois depende do tamanho da imagem ou do número de classes, mas não de ambos simultaneamente. Além disso, a VI mostrou-se eficaz com EE-DNNs treinadas com diferentes funções de perda (baseadas em distribuição e em região), ao contrário da NE, que restringe a escolha da função de perda.

## Configuração Experimental e Resultados

Os experimentos foram realizados usando PyTorch e o conjunto de dados Pascal VOC 2012 para segmentação semântica. Foram utilizadas EE-DNNs com sete saídas antecipadas, espaçadas uniformemente em termos de operações de ponto flutuante (FLOPs). Um DeepLabV3 pré-treinado foi usado como backbone da DNN. Os modelos foram treinados por 250 épocas.

Os resultados experimentais compararam o desempenho dos critérios de saída baseados em NE e VI, avaliando o trade-off entre o desempenho da segmentação (mIoU) e o custo computacional (FLOPs). As principais descobertas incluem:

• Vantagem do VI: Para níveis de desempenho mais altos (mIoU), o critério baseado em VI superou o NE em termos de economia de FLOPs, especialmente em dispositivos de borda. Isso significa que menos imagens precisaram ser processadas pelas camadas mais profundas da rede, resultando em menor custo computacional e latência.

• Escalabilidade: A VI demonstrou melhor escalabilidade com o tamanho da imagem e o número de classes em comparação com a NE, que apresentou um aumento significativo no tempo de execução com o aumento do número de classes.

• Subutilização de Saídas Antecipadas com NE: O critério baseado em NE subutilizou as saídas antecipadas intermediárias, fazendo com que a maioria das imagens fosse enviada para a saída final (na nuvem), o que aumenta a latência e o custo de comunicação. Em contraste, o critério baseado em VI distribuiu as inferências de forma mais eficiente entre as saídas antecipadas.

## Conclusão

O trabalho aborda a necessidade crítica de um critério de saída eficiente para EE-DNNs em segmentação semântica, especialmente em configurações de co-inferência edge-cloud. Os autores adaptaram o critério baseado em NE e identificaram suas limitações, como a baixa escalabilidade e a restrição na escolha de funções de perda. Em resposta, propuseram um critério de saída baseado em região, implementado com a Variação da Informação (VI), que se mostrou superior em termos de escalabilidade, compatibilidade com diversas funções de perda e eficiência computacional.

O critério baseado em VI permite que as EE-DNNs interrompam o processo de inferência quando as diferenças entre as segmentações consecutivas são desprezíveis, resultando em economia significativa de FLOPs e melhor aproveitamento das saídas antecipadas. Este avanço é crucial para a implantação bem-sucedida de EE-DNNs em cenários de borda e nuvem, onde a latência e o consumo de recursos são fatores críticos. Futuras pesquisas podem explorar outras métricas de saída e critérios que considerem os requisitos de transmissão de dados para ajustes dinâmicos de limiares.
