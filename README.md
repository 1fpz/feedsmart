# FeedSmart

Sistema de gestão de feedbacks de usuários, feito em Python e executado no terminal.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Interface](https://img.shields.io/badge/interface-terminal-lightgrey)
![Licença](https://img.shields.io/badge/licença-MIT-green)

Projeto da disciplina **Computational Thinking with Python** (Engenharia de Software, FIAP).

## O que ele faz

- Cadastra usuários (nome, idade, profissão e tipo)
- Registra feedbacks com produto, comentário, nota (0 a 10) e data
- Mostra os feedbacks de um produto específico
- Gera relatório com média geral, média por produto e distribuição das notas
- Gera insights automáticos (produtos com média baixa e usuários engajados)
- Salva e carrega os dados em **JSON** e **TXT**
- Valida todas as entradas (números, datas, campos vazios, arquivos ausentes ou corrompidos)

## Como executar

Requisitos: Python 3.8 ou superior. Não há dependências externas, apenas a biblioteca padrão.

```bash
git clone https://github.com/SEU-USUARIO/feedsmart.git
cd feedsmart
python feedsmart.py
```

Os dados são carregados automaticamente do JSON ao abrir. Se os arquivos não existirem, o programa começa vazio.

## Menu

```
==============================
   FEEDSMART - FEEDBACKS
==============================
1 - Cadastrar usuário
2 - Listar usuários
3 - Registrar feedback
4 - Ver feedbacks por produto
5 - Relatório
6 - Insights automáticos
7 - Salvar dados (JSON e TXT)
8 - Carregar dados
0 - Sair
```

A opção `0` salva os dados antes de encerrar.

## Exemplo de saída

Relatório com os dados de exemplo que acompanham o repositório:

```
--- RELATÓRIO ---
Total de feedbacks: 14
Média geral: 7.00

Produto | Quantidade | Média
FeedApp | 6 | 8.58
FeedBot | 5 | 4.50
FeedDash | 3 | 8.00

Categorias:
Ruins (0 a 4): 2
Regulares (4.1 a 7): 5
Bons (7.1 a 10): 7
```

Insights automáticos:

```
--- INSIGHTS ---
Produto FeedBot tem média abaixo de 6 - precisa de melhorias.
Usuário Carlos Souza enviou mais de 5 feedbacks - perfil engajado.
```

## Faixas de nota

| Categoria | Faixa       |
|-----------|-------------|
| Ruim      | 0 a 4       |
| Regular   | acima de 4 até 7 |
| Bom       | acima de 7 até 10 |

## Estrutura do projeto

```
feedsmart/
├── feedsmart.py      # código principal
├── usuarios.json     # usuários (JSON)
├── feedbacks.json    # feedbacks (JSON)
├── usuarios.txt      # usuários (TXT: id;nome;idade;profissao;tipo)
├── feedbacks.txt     # feedbacks (TXT: id_usuario;produto;nota;data;comentario)
└── README.md
```

## Organização do código

| Grupo        | Funções                                                        |
|--------------|----------------------------------------------------------------|
| Validação    | `ler_inteiro`, `ler_nota`, `ler_texto`, `ler_data`             |
| Cadastro     | `cadastrar_usuario`, `listar_usuarios`, `buscar_usuario`, `registrar_feedback` |
| Análise      | `calcular_media`, `agrupar_por_produto`, `listar_por_produto`, `relatorio`, `insights` |
| Arquivos     | `salvar`, `carregar_json`, `carregar_txt`                      |

Estruturas de dados usadas: **listas** (usuários e feedbacks), **dicionários** (cada registro), **tuplas** (tipos de usuário) e **matrizes** (linhas do relatório).

## Possíveis melhorias

- Remover e editar usuários e feedbacks
- Filtrar feedbacks por período
- Exportar o relatório em CSV ou PDF
- Testes automatizados com `unittest` ou `pytest`

## Autor

- Felipe Ilek

## Licença

Distribuído sob a licença MIT.
