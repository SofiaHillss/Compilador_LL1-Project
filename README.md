# Compilador **C--**

Este projeto implementa um **compilador LL(1)** desenvolvido em **Python**, como parte da disciplina de **Compiladores**.  

A linguagem criada, chamada **C--**, possui suporte a estruturas básicas de programação, como **variáveis, vetores, funções, laços, condicionais e entrada/saída**.  
O compilador traduz programas escritos em **C--** para **Python**, permitindo sua execução.

---

## Funcionalidades

- **Analisador Léxico**: converte o código-fonte em tokens.  
- **Analisador Sintático (LL(1))**: valida a estrutura do programa de acordo com a gramática.  
- **Analisador Semântico**: checa declarações, tipos e escopo.  
- **Gerador de Código**: traduz programas **C--** para código equivalente em **Python**.  

---
#  Gramatica da linguagem C--

[📄 Ver gramática da linguagem C--](./Docs/gramatica-C--.txt)

## Tabelas First, Follow e Predict

A **tabela de First, Follow e Predict** da linguagem **C--** foi construída utilizando a ferramenta online:  
👉 [http://hackingoff.com/compilers/predict-first-follow-set](http://hackingoff.com/compilers/predict-first-follow-set)

O resultado completo está disponível em PDF no seguinte caminho do repositório:  
[📄 Tabelas First, Follow e Predict](./Docs/tabela_first_follow_predict.pdf)

---
# Como executar

O compilador irá processar o código de exemplo `sort.txt` e gerar o resultado em Python no arquivo `result.py`.

```
git clone https://github.com/SofiaHillss/Compilador_LL1-Project.git
cd Compilador_LL1-Project
python3 main.py

