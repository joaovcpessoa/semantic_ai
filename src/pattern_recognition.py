def recognize_pattern(sentences, keywords):
    results = []
    for i, sentence in enumerate(sentences):
        found_keywords = [keyword for keyword in keywords if keyword in sentence.lower()]
        if found_keywords:
            results.append(
                f"Frase {i+1}: '{sentence}' - Padrões encontrados: {', '.join(found_keywords)}"
            )
    return results


if __name__ == '__main__':
    data = [
        'O gato preto pulou sobre o muro alto.',
        'O cachorro marrom correu atrás da bola.',
        'A gata branca dormiu na cama macia.',
        'O pássaro azul voou alto no céu.',
        'O cão grande latiu para o carteiro.'
    ]

    semantic_keywords = ['gato', 'cachorro', 'cão', 'pássaro', 'pulou', 'correu', 'dormiu', 'voou', 'latiu']

    print('Dados de entrada:')
    for i, sentence in enumerate(data):
        print(f'  {i+1}. {sentence}')

    print('\nPalavras-chave semânticas para busca:', ', '.join(semantic_keywords))

    patterns_found = recognize_pattern(data, semantic_keywords)

    print('\nResultados do reconhecimento de padrões:')
    if patterns_found:
        for result in patterns_found:
            print(result)
    else:
        print('Nenhum padrão semântico encontrado com as palavras-chave fornecidas.')
        