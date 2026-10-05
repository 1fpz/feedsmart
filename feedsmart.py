"""
FeedSmart - Sistema de Gestão de Feedbacks de Usuários
CP5 - Computational Thinking with Python

Integrantes:
Felipe Ilek - RM 571322
Marcos Vinicius - RM 569366
Michel Hanada - RM 571987
"""

import json
import os
from datetime import datetime

# tupla com os tipos de usuario
TIPOS = ("Usuário final", "Administrador", "Testador")

# cores para o terminal
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
RESET = "\033[0m"

# os arquivos ficam na mesma pasta do programa (funciona em qualquer IDE)
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQ_USUARIOS_JSON = os.path.join(PASTA, "usuarios.json")
ARQ_FEEDBACKS_JSON = os.path.join(PASTA, "feedbacks.json")
ARQ_USUARIOS_TXT = os.path.join(PASTA, "usuarios.txt")
ARQ_FEEDBACKS_TXT = os.path.join(PASTA, "feedbacks.txt")


def ler_inteiro(mensagem, minimo, maximo):
    """Pede um número inteiro ao usuário até ele digitar um valor válido."""
    while True:
        try:
            numero = int(input(mensagem))
            if minimo <= numero <= maximo:
                return numero
            print(VERMELHO + f"Digite um número entre {minimo} e {maximo}." + RESET)
        except ValueError:
            print(VERMELHO + "Entrada inválida! Digite apenas números." + RESET)


def ler_nota():
    """Pede uma nota de 0 a 10 até o usuário digitar um valor válido."""
    while True:
        try:
            nota = float(input("Nota (0 a 10): ").replace(",", "."))
            if 0 <= nota <= 10:
                return nota
            print(VERMELHO + "A nota deve ser de 0 a 10." + RESET)
        except ValueError:
            print(VERMELHO + "Entrada inválida! Digite um número." + RESET)


def ler_texto(mensagem):
    """Pede um texto ao usuário e não deixa ficar vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print(VERMELHO + "Esse campo não pode ficar vazio." + RESET)


def ler_data():
    """Pede uma data no formato DD/MM/AAAA. Se der ENTER, usa a data de hoje."""
    while True:
        data = input("Data (DD/MM/AAAA) ou ENTER para hoje: ").strip()
        if data == "":
            return datetime.now().strftime("%d/%m/%Y")
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return data
        except ValueError:
            print(VERMELHO + "Data inválida! Exemplo: 25/09/2026" + RESET)


def cadastrar_usuario(usuarios):
    """Cadastra um novo usuário (nome, idade, profissão e tipo) na lista."""
    print("\n--- CADASTRAR USUÁRIO ---")
    nome = ler_texto("Nome: ").replace(";", ",")
    idade = ler_inteiro("Idade: ", 1, 120)
    profissao = ler_texto("Profissão: ").replace(";", ",")

    print("Tipo de usuário:")
    for i in range(len(TIPOS)):
        print(f"{i + 1} - {TIPOS[i]}")
    opcao = ler_inteiro("Escolha o tipo: ", 1, len(TIPOS))

    usuario = {
        "id": len(usuarios) + 1,
        "nome": nome,
        "idade": idade,
        "profissao": profissao,
        "tipo": TIPOS[opcao - 1],
    }
    usuarios.append(usuario)
    print(VERDE + f"Usuário {nome} cadastrado com ID {usuario['id']}!" + RESET)


def listar_usuarios(usuarios):
    """Mostra todos os usuários cadastrados."""
    print("\n--- USUÁRIOS ---")
    if len(usuarios) == 0:
        print(AMARELO + "Nenhum usuário cadastrado." + RESET)
        return
    for u in usuarios:
        print(f"ID {u['id']} | {u['nome']} | {u['idade']} anos | {u['profissao']} | {u['tipo']}")


def buscar_usuario(usuarios, id_usuario):
    """Procura um usuário pelo id. Retorna o dicionário ou None se não achar."""
    for u in usuarios:
        if u["id"] == id_usuario:
            return u
    return None


def registrar_feedback(usuarios, feedbacks):
    """Registra um feedback ligado a um usuário que já existe."""
    print("\n--- REGISTRAR FEEDBACK ---")
    if len(usuarios) == 0:
        print(AMARELO + "Cadastre um usuário primeiro!" + RESET)
        return

    listar_usuarios(usuarios)
    # só aceita feedback de usuário que já existe
    id_usuario = ler_inteiro("ID do usuário: ", 1, 100000)
    if buscar_usuario(usuarios, id_usuario) is None:
        print(VERMELHO + "Usuário não encontrado!" + RESET)
        return

    produto = ler_texto("Produto: ").replace(";", ",")  # ";" é o separador do TXT
    texto = ler_texto("Comentário: ").replace(";", ",")
    nota = ler_nota()
    data = ler_data()

    feedback = {
        "usuario_id": id_usuario,
        "produto": produto,
        "texto": texto,
        "nota": nota,
        "data": data,
    }
    feedbacks.append(feedback)
    print(VERDE + "Feedback registrado com sucesso!" + RESET)


def calcular_media(notas):
    """Calcula a média de uma lista de notas."""
    if len(notas) == 0:
        return 0
    return sum(notas) / len(notas)


def agrupar_por_produto(feedbacks):
    """Cria um dicionário onde a chave é o produto e o valor é a lista de notas."""
    produtos = {}
    # percorre os feedbacks e junta as notas de cada produto
    for f in feedbacks:
        if f["produto"] not in produtos:
            produtos[f["produto"]] = []
        produtos[f["produto"]].append(f["nota"])
    return produtos


def listar_por_produto(feedbacks):
    """Mostra os feedbacks de um produto escolhido pelo usuário."""
    print("\n--- FEEDBACKS POR PRODUTO ---")
    if len(feedbacks) == 0:
        print(AMARELO + "Nenhum feedback registrado." + RESET)
        return

    produtos = agrupar_por_produto(feedbacks)
    print("Produtos:", ", ".join(produtos.keys()))
    busca = ler_texto("Digite o nome do produto: ")

    achou = False
    for f in feedbacks:
        if f["produto"].lower() == busca.lower():
            print(f"{f['data']} | Nota {f['nota']} | {f['texto']}")
            achou = True
    if not achou:
        print(AMARELO + "Nenhum feedback para esse produto." + RESET)


def relatorio(feedbacks):
    """Mostra média geral, média por produto (matriz) e contagem por categoria."""
    print("\n--- RELATÓRIO ---")
    if len(feedbacks) == 0:
        print(AMARELO + "Nenhum feedback para analisar." + RESET)
        return

    todas_notas = [f["nota"] for f in feedbacks]
    print(f"Total de feedbacks: {len(feedbacks)}")
    print(f"Média geral: {calcular_media(todas_notas):.2f}")

    # matriz: cada linha = [produto, quantidade, média]
    matriz = []
    produtos = agrupar_por_produto(feedbacks)
    for produto in produtos:
        notas = produtos[produto]
        matriz.append([produto, len(notas), calcular_media(notas)])

    print("\nProduto | Quantidade | Média")
    for linha in matriz:
        print(f"{linha[0]} | {linha[1]} | {linha[2]:.2f}")

    # conta quantas notas caem em cada categoria
    ruins = 0
    regulares = 0
    bons = 0
    for nota in todas_notas:
        if nota <= 4:
            ruins += 1
        elif nota <= 7:
            regulares += 1
        else:
            bons += 1
    print("\nCategorias:")
    print(f"Ruins (0 a 4): {ruins}")
    print(f"Regulares (4.1 a 7): {regulares}")
    print(f"Bons (7.1 a 10): {bons}")


def insights(usuarios, feedbacks):
    """Desafio extra: gera frases automáticas sobre produtos e usuários."""
    print("\n--- INSIGHTS ---")
    if len(feedbacks) == 0:
        print(AMARELO + "Nenhum feedback para analisar." + RESET)
        return

    # avisa os produtos com média baixa
    produtos = agrupar_por_produto(feedbacks)
    for produto in produtos:
        media = calcular_media(produtos[produto])
        if media < 6:
            print(VERMELHO + f"Produto {produto} tem média abaixo de 6 - precisa de melhorias." + RESET)

    # conta quantos feedbacks cada usuário enviou
    for u in usuarios:
        quantidade = 0
        for f in feedbacks:
            if f["usuario_id"] == u["id"]:
                quantidade += 1
        if quantidade > 5:
            print(VERDE + f"Usuário {u['nome']} enviou mais de 5 feedbacks - perfil engajado." + RESET)


def salvar(usuarios, feedbacks):
    """Salva usuários e feedbacks em arquivos JSON e também em arquivos TXT."""
    try:
        # JSON
        with open(ARQ_USUARIOS_JSON, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
        with open(ARQ_FEEDBACKS_JSON, "w", encoding="utf-8") as arquivo:
            json.dump(feedbacks, arquivo, indent=4, ensure_ascii=False)

        # TXT (uma linha por registro, campos separados por ;)
        with open(ARQ_USUARIOS_TXT, "w", encoding="utf-8") as arquivo:
            for u in usuarios:
                linha = f"{u['id']};{u['nome']};{u['idade']};{u['profissao']};{u['tipo']}\n"
                arquivo.write(linha)
        with open(ARQ_FEEDBACKS_TXT, "w", encoding="utf-8") as arquivo:
            for f in feedbacks:
                linha = f"{f['usuario_id']};{f['produto']};{f['nota']};{f['data']};{f['texto']}\n"
                arquivo.write(linha)
        print(VERDE + "Dados salvos em JSON e TXT com sucesso!" + RESET)
    except OSError:
        print(VERMELHO + "Erro ao salvar os arquivos." + RESET)


def carregar_json():
    """Lê usuários e feedbacks dos arquivos JSON. Retorna as duas listas."""
    usuarios = []
    feedbacks = []
    try:
        with open(ARQ_USUARIOS_JSON, "r", encoding="utf-8") as arquivo:
            usuarios = json.load(arquivo)
        with open(ARQ_FEEDBACKS_JSON, "r", encoding="utf-8") as arquivo:
            feedbacks = json.load(arquivo)
    except FileNotFoundError:
        print(AMARELO + "Arquivos JSON não encontrados (começando vazio)." + RESET)
    except json.JSONDecodeError:
        print(VERMELHO + "Arquivo JSON corrompido." + RESET)
        usuarios = []
        feedbacks = []
    return usuarios, feedbacks


def carregar_txt():
    """Lê usuários e feedbacks dos arquivos TXT. Retorna as duas listas."""
    usuarios = []
    feedbacks = []
    try:
        with open(ARQ_USUARIOS_TXT, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(";")
                if len(partes) == 5:
                    usuarios.append({
                        "id": int(partes[0]),
                        "nome": partes[1],
                        "idade": int(partes[2]),
                        "profissao": partes[3],
                        "tipo": partes[4],
                    })
        with open(ARQ_FEEDBACKS_TXT, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(";")
                if len(partes) == 5:
                    feedbacks.append({
                        "usuario_id": int(partes[0]),
                        "produto": partes[1],
                        "nota": float(partes[2]),
                        "data": partes[3],
                        "texto": partes[4],
                    })
    except FileNotFoundError:
        print(AMARELO + "Arquivos TXT não encontrados (começando vazio)." + RESET)
    except ValueError:
        print(VERMELHO + "Arquivo TXT tem linhas inválidas." + RESET)
        usuarios = []
        feedbacks = []
    return usuarios, feedbacks


def menu():
    """Mostra as opções do menu."""
    print("\n==============================")
    print("   FEEDSMART - FEEDBACKS")
    print("==============================")
    print("1 - Cadastrar usuário")
    print("2 - Listar usuários")
    print("3 - Registrar feedback")
    print("4 - Ver feedbacks por produto")
    print("5 - Relatório")
    print("6 - Insights automáticos")
    print("7 - Salvar dados (JSON e TXT)")
    print("8 - Carregar dados")
    print("0 - Sair")


def main():
    """Função principal: roda o menu até o usuário escolher sair."""
    # carrega os dados salvos (se existirem) ao abrir o programa
    usuarios, feedbacks = carregar_json()

    # repete o menu até o usuário digitar 0
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_usuario(usuarios)
        elif opcao == "2":
            listar_usuarios(usuarios)
        elif opcao == "3":
            registrar_feedback(usuarios, feedbacks)
        elif opcao == "4":
            listar_por_produto(feedbacks)
        elif opcao == "5":
            relatorio(feedbacks)
        elif opcao == "6":
            insights(usuarios, feedbacks)
        elif opcao == "7":
            salvar(usuarios, feedbacks)
        elif opcao == "8":
            print("1 - Carregar do JSON")
            print("2 - Carregar do TXT")
            formato = ler_inteiro("Escolha o formato: ", 1, 2)
            if formato == 1:
                novos_usuarios, novos_feedbacks = carregar_json()
            else:
                novos_usuarios, novos_feedbacks = carregar_txt()

            # só troca os dados se carregou alguma coisa (evita perder tudo por erro)
            if len(novos_usuarios) == 0 and len(novos_feedbacks) == 0:
                print(AMARELO + "Nada foi carregado. Os dados atuais foram mantidos." + RESET)
            else:
                usuarios = novos_usuarios
                feedbacks = novos_feedbacks
                print(VERDE + f"Carregados {len(usuarios)} usuários e {len(feedbacks)} feedbacks." + RESET)
        elif opcao == "0":
            salvar(usuarios, feedbacks)
            print("Até logo!")
            break
        else:
            print(VERMELHO + "Opção inválida! Escolha de 0 a 8." + RESET)


main()
