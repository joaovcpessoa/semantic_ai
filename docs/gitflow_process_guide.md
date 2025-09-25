# Fluxo de Trabalho usando Gitflow

O Gitflow é uma metodologia de gerenciamento de branches que ajuda equipes a organizar o desenvolvimento de forma clara, separando **produção**, **desenvolvimento** e **novas funcionalidades**. A ideia é garantir que alterações não afetem o código em produção até estarem validadas.

---

## 1. Trabalhando com a branch principal (main)

A branch `main` contém o **código em produção**. Todas as alterações aprovadas e testadas serão mescladas aqui.

```bash
# Troca para a branch main
git switch main

# Atualiza a branch com a última versão do repositório remoto
git pull
```

**Boas práticas:**

* Nunca faça commits diretos na `main`.
* Sempre trabalhe em branches de feature ou release antes de mesclar aqui.

---

## 2. Criando uma branch de feature

Uma **feature branch** é usada para desenvolver uma **nova funcionalidade**, sem afetar a branch principal.

```bash
git checkout -b feature/nome_da_feature
```

* Prefixo `feature/` ajuda a identificar que a branch é para desenvolvimento de funcionalidades.
* `nome_da_feature` deve ser **descritivo**, por exemplo `feature/login_usuario`.

---

## 3. Desenvolvimento finalizado

Quando a feature estiver pronta:

```bash
# Adiciona todas as alterações ao commit
git add .

# Cria um commit descritivo
git commit -m 'feature: Adicionada a função de login de usuário'

# Envia a branch para o repositório remoto
git push -u origin feature/nome_da_feature
```

**Boas práticas de commit:**

* Use mensagens claras e padronizadas, como `feature: descrição`, `fix: descrição`, `chore: descrição`.
* Faça commits pequenos e coesos.

---

## 4. Validar e mesclar a feature na develop

A branch `develop` é o **ambiente de integração**, onde todas as features se encontram antes de gerar uma release.

```bash
# Troca para a branch develop
git switch develop

# Atualiza a develop com o remoto
git pull origin develop

# Mescla a feature na develop
git merge feature/nome_da_feature

# Apaga a branch local da feature
git branch -d feature/nome_da_feature

# Apaga a branch remota da feature
git push origin --delete feature/nome_da_feature
```

**Boas práticas:**

* Sempre atualize a `develop` antes de mesclar (`git pull`).
* Se houver conflitos, resolva com cuidado.
* Garanta que testes automatizados passem antes de mesclar.

---

## 5. Criando a branch de release

Quando um conjunto de features estiver pronto para ser lançado, cria-se uma **release branch** a partir da `develop`. Ela é usada para **ajustes finais, testes e correções de bugs**.

```bash
git checkout -b release/nome_da_feature
git push -u origin release/nome_da_feature
```

**Boas práticas:**

* Prefixo `release/` indica que é uma branch de preparação para produção.
* Evite desenvolver novas features aqui; apenas correções e ajustes.

---

## 6. Release validada e mesclagem na main

Depois que a release for testada e aprovada, mescle na `main` (produção) e na `develop` (para manter alterações sincronizadas):

```bash
# Mesclar na main (produção)
git switch main
git pull origin main
git merge release/nome_da_feature

# Apaga a release local
git branch -d release/nome_da_feature

# Apaga a release remota
git push origin --delete release/nome_da_feature
```

**Dica:**
Se quiser manter histórico limpo, você pode usar `--no-ff` no merge para garantir que cada release apareça como um commit separado no histórico:

```bash
git merge --no-ff release/nome_da_feature
```

---

### Resumão

| Branch      | Propósito                                 |
| ----------- | ----------------------------------------- |
| `main`      | Código em produção                        |
| `develop`   | Integração de todas as features           |
| `feature/*` | Desenvolvimento de novas funcionalidades  |
| `release/*` | Preparação para deploy e correções finais |
