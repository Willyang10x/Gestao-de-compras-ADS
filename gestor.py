import json  # Traz os dados do arquivo(.json)
from datetime import datetime  # Ferramenta para import a data e a hora do salvamento

ARQUIVO_DADOS = 'dados.json'


def carregar_dados():
    """Tenta ler o arquivo. Se não conseguir, finge que tá vazio."""
    try:
        # Tenta abrir o arquivo 'dados.json' no modo 'r' (read/leitura)
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            # Traduz o texto do arquivo pra lista do Python
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir (erro 1) ou estiver todo bagunçado (erro 2)...
        return []  # ...retorna uma lista vazia pra não travar o programa.


def salvar_dados(compras):
    """Pega a lista da memória e grava no arquivo de verdade."""
    # Abre o arquivo no modo 'w' (write/escrita).
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(compras, f, indent=4)


def _gerar_proximo_id(compras):
    if not compras:  # Se a lista estiver vazia...
        return 1

    # Se já tem gente, ele olha o ID de todo mundo, pega o maior (max) e soma 1.
    return max(compra['id'] for compra in compras) + 1


def _buscar_compra_por_id(compras, id_compra):
    for compra in compras:        # Para cada compra na lista...
        # Se o crachá (ID) for igual ao que eu quero...
        if compra['id'] == id_compra:
            return compra
    # Se rodou a lista toda e não achou, devolve "Nada".
    return None


def _imprimir_compra(compra):
    # O .get() é um seguro: Se não tiver data gravada, ele escreve "Data não registrada" em vez de dar erro.
    data_formatada = compra.get('data', 'Data não registrada')

    print(f"  [ID: {compra['id']}] - Data: {data_formatada}")
    print(f"    Cliente: {compra['cliente']}")
    print(f"    Produtos: {compra['produtos']}")
    print(f"    Valor Total: R${compra['valor_total']:.2f}")
    print("-" * 30)


def cadastrar_compra():
    print("\n--- Cadastro de Nova Compra ---")

    cliente = input("Nome do cliente: ")
    produtos = input("Produtos: ")

    while True:
        try:
            valor_total = float(input("Valor total: "))
            break
        except ValueError:
            print("Valor inválido.")

    # Pega a hora atual. O strftime é tipo formatar a data: Dia/Mês/Ano Hora:Minuto.
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    compras = carregar_dados()

    nova_compra = {
        "id": _gerar_proximo_id(compras),
        "cliente": cliente,
        "produtos": produtos,
        "valor_total": valor_total,
        "data": data_atual
    }

    compras.append(nova_compra)
    #  Salva a nova compra na lista

    salvar_dados(compras)
    print(f"Compra registrada em {data_atual}!")


def listar_compras(lista_para_imprimir=None):

    if lista_para_imprimir is None:
        print("\n--- Histórico de Compras ---")
        lista_para_imprimir = carregar_dados()

    if not lista_para_imprimir:
        print("Nenhuma compra encontrada.")
        return

    for compra in lista_para_imprimir:
        _imprimir_compra(compra)


def alterar_compra():
    print("\n--- Alterar Compra ---")
    listar_compras()  # Mostra tudo pro usuário saber o ID.

    try:
        id_op = int(input("ID para alterar: "))
    except ValueError:
        return

    compras = carregar_dados()

    compra = _buscar_compra_por_id(compras, id_op)

    if not compra:  # Se o buscar não encontrar volta com "None" (nada)...
        print("Não encontrado.")
        return

    novo_cli = input(f"Cliente ({compra['cliente']}): ")
    if novo_cli:
        compra['cliente'] = novo_cli

    novo_prod = input(f"Produtos ({compra['produtos']}): ")
    if novo_prod:
        compra['produtos'] = novo_prod

    novo_val = input(f"Valor ({compra['valor_total']}): ")
    if novo_val:
        try:
            compra['valor_total'] = float(novo_val)  # Tenta virar número
        except ValueError:
            # Se der erro, finge que nada aconteceu e mantém o valor velho.
            pass

    salvar_dados(compras)  # Salva as mudanças.
    print("Atualizado!")


def excluir_compra():
    print("\n--- Excluir Compra ---")
    listar_compras()
    try:
        id_op = int(input("ID para excluir: "))
    except ValueError:
        return

    compras = carregar_dados()

    # Aqui cria uma NOVA lista copiando todo mundo, MENOS o que a gente quer excluir.

    nova_lista = [c for c in compras if c['id'] != id_op]

    if len(compras) == len(nova_lista):
        print("Não encontrado.")
    else:
        salvar_dados(nova_lista)  # Salva a lista nova .
        print("Excluído!")


def filtrar_compras():
    print("\n--- Filtrar ---")
    # Transforma tudo em minúsculo pra facilitar a busca.
    termo = input("Nome do cliente: ").lower()
    compras = carregar_dados()

    # Cria uma lista só com quem tem o 'termo' dentro do nome.
    filtradas = [c for c in compras if termo in c['cliente'].lower()]

    if not filtradas:
        print("Nenhum registro encontrado.")
    else:
        # Reutiliza a função de listar, mas agora só passa a lista filtrada.
        listar_compras(filtradas)
