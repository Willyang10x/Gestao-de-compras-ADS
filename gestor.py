import json

ARQUIVO_DADOS = 'dados.json'

def carregar_dados():

    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def salvar_dados(compras):

    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(compras, f, indent=4)


def _gerar_proximo_id(compras):

    if not compras:
        return 1
    ultimo_id = max(compra['id'] for compra in compras)
    return ultimo_id + 1

def _buscar_compra_por_id(compras, id_compra):
    for compra in compras:
        if compra['id'] == id_compra:
            return compra
    return None

def _imprimir_compra(compra):
    print(f"  [ID: {compra['id']}] - Cliente: {compra['cliente']}")
    print(f"    Produtos: {compra['produtos']}")
    print(f"    Valor Total: R${compra['valor_total']:.2f}")



def cadastrar_compra():

    print("\n--- Cadastro de Nova Compra ---")
    

    cliente = input("Digite o nome do cliente: ")
    produtos = input("Digite os produtos (separados por vírgula): ")
    while True:
        try:
            valor_total = float(input("Digite o valor total da compra (ex: 150.99): "))
            break
        except ValueError:
            print("Valor inválido. Use ponto (.) como separador.")

    compras = carregar_dados()
    

    nova_compra = {
        "id": _gerar_proximo_id(compras),
        "cliente": cliente,
        "produtos": produtos,
        "valor_total": valor_total
    }
    
    compras.append(nova_compra)
    salvar_dados(compras)
    print("Compra cadastrada com sucesso!")

def listar_compras(lista_para_imprimir=None):

    if lista_para_imprimir is None:
        print("\n--- Todas as Compras Cadastradas ---")
        lista_para_imprimir = carregar_dados()

    if not lista_para_imprimir:
        print("Nenhuma compra encontrada.")
        return

    for compra in lista_para_imprimir:
        _imprimir_compra(compra) 

def alterar_compra():

    print("\n--- Alterar Compra ---")
    listar_compras()
    
    try:
        id_para_alterar = int(input("Digite o ID da compra que deseja alterar: "))
    except ValueError:
        print("ID inválido. Deve ser um número.")
        return

    compras = carregar_dados()
    compra_encontrada = _buscar_compra_por_id(compras, id_para_alterar)

    if not compra_encontrada:
        print(f"Compra com ID {id_para_alterar} não encontrada.")
        return

    print(f"Alterando dados da Compra [ID: {compra_encontrada['id']}]. Deixe em branco para manter.")


    novo_cliente = input(f"Cliente ({compra_encontrada['cliente']}): ")
    if novo_cliente:
        compra_encontrada['cliente'] = novo_cliente

    novos_produtos = input(f"Produtos ({compra_encontrada['produtos']}): ")
    if novos_produtos:
        compra_encontrada['produtos'] = novos_produtos

    novo_valor_str = input(f"Valor Total ({compra_encontrada['valor_total']}): ")
    if novo_valor_str:
        try:
            compra_encontrada['valor_total'] = float(novo_valor_str)
        except ValueError:
            print("Valor inválido, mantendo o antigo.")

    salvar_dados(compras)
    print("Compra alterada com sucesso!")

def excluir_compra():

    print("\n--- Excluir Compra ---")
    listar_compras()
    
    try:
        id_para_excluir = int(input("Digite o ID da compra que deseja EXCLUIR: "))
    except ValueError:
        print("ID inválido. Deve ser um número.")
        return

    compras = carregar_dados()
    
    compras_atualizadas = [
        compra for compra in compras 
        if compra['id'] != id_para_excluir
    ]

    if len(compras) == len(compras_atualizadas):
        print(f"Compra com ID {id_para_excluir} não encontrada.")
    else:
        salvar_dados(compras_atualizadas)
        print("Compra excluída com sucesso!")

def filtrar_compras():

    print("\n--- Filtrar Compras por Cliente ---")
    termo = input("Digite o nome do cliente (ou parte dele) para buscar: ").lower()
    
    compras = carregar_dados()
    
    compras_filtradas = [
        compra for compra in compras 
        if termo in compra['cliente'].lower()
    ]

    if not compras_filtradas:
        print(f"Nenhuma compra encontrada para o cliente '{termo}'.")
    else:
        print(f"--- Resultados para '{termo}' ---")
        listar_compras(compras_filtradas)