# --- IMPORTAÇÕES (Trazendo as ferramentas) ---
import json  # Traz a ferramenta que sabe ler e escrever no arquivo do caderno (.json)
from datetime import datetime  # Traz o relógio do computador pra gente saber a hora

# Aqui eu defino o nome do arquivo numa "etiqueta" pra não ter que ficar digitando o nome toda hora e errar.
ARQUIVO_DADOS = 'dados.json'

# --- FUNÇÕES DE ARQUIVO (O trabalho pesado de ler e escrever) ---

def carregar_dados():
    """Tenta ler o arquivo. Se não conseguir, finge que tá vazio."""
    try:
        # Tenta abrir o arquivo 'dados.json' no modo 'r' (read/leitura)
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            return json.load(f)  # Traduz o texto do arquivo pra lista do Python
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir (erro 1) ou estiver todo bagunçado (erro 2)...
        return []  # ...retorna uma lista vazia pra não travar o programa.

def salvar_dados(compras):
    """Pega a lista da memória e grava no arquivo de verdade."""
    # Abre o arquivo no modo 'w' (write/escrita). Cuidado: isso apaga o que tinha antes e escreve por cima!
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        # O 'indent=4' é só pra deixar o texto bonitinho, com recuo, igual num livro.
        json.dump(compras, f, indent=4)

# --- FUNÇÕES AJUDANTES (Os estagiários que fazem tarefas pequenas) ---

def _gerar_proximo_id(compras):
    """Gera o número da etiqueta (ID). Se o último foi 10, esse retorna 11."""
    if not compras: # Se a lista estiver vazia...
        return 1    # ...então a primeira compra é a número 1.
    
    # Se já tem gente, ele olha o ID de todo mundo, pega o maior (max) e soma 1.
    return max(compra['id'] for compra in compras) + 1

def _buscar_compra_por_id(compras, id_compra):
    """Detetive: Procura na lista uma compra que tenha aquele ID específico."""
    for compra in compras:        # Para cada compra na lista...
        if compra['id'] == id_compra: # Se o crachá (ID) for igual ao que eu quero...
            return compra         # ...Achou! Devolve ela.
    return None                   # Se rodou a lista toda e não achou, devolve "Nada".

def _imprimir_compra(compra):
    """Maquiador: Pega os dados feios e mostra bonitinho na tela."""
    # O .get() é um seguro: Se não tiver data gravada, ele escreve "Data não registrada" em vez de dar erro.
    data_formatada = compra.get('data', 'Data não registrada')
    
    # Os 'print' abaixo só desenham na tela. O 'f' antes das aspas deixa colocar variáveis {} no meio do texto.
    print(f"  [ID: {compra['id']}] - Data: {data_formatada}")
    print(f"    Cliente: {compra['cliente']}")
    print(f"    Produtos: {compra['produtos']}")
    # O :.2f significa: "Mostra esse número com 2 casas depois da vírgula" (tipo dinheiro).
    print(f"    Valor Total: R${compra['valor_total']:.2f}")
    print("-" * 30) # Faz uma linha de 30 tracinhos pra separar.

# --- FUNÇÕES PRINCIPAIS (Onde a mágica acontece) ---

def cadastrar_compra():
    print("\n--- Cadastro de Nova Compra ---")
    
    # O input() faz o programa parar e esperar o usuário digitar algo.
    cliente = input("Nome do cliente: ")
    produtos = input("Produtos: ")
    
    # Aqui tem um loop 'while True' (loop infinito) pra obrigar o usuário a digitar um número.
    while True:
        try:
            valor_total = float(input("Valor total: ")) # Tenta converter letra pra número.
            break # Se conseguiu converter, o 'break' quebra o loop e sai.
        except ValueError:
            print("Valor inválido.") # Se digitou letra, avisa e o loop roda de novo.

    # Pega a hora de AGORA. O strftime é tipo formatar a data: Dia/Mês/Ano Hora:Minuto.
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    # 1. Carrega tudo que já existe na memória.
    compras = carregar_dados()
    
    # 2. Cria o pacote da nova compra (Dicionário).
    nova_compra = {
        "id": _gerar_proximo_id(compras), # Pede pro estagiário gerar o ID
        "cliente": cliente,
        "produtos": produtos,
        "valor_total": valor_total,
        "data": data_atual
    }
    
    # 3. Coloca esse pacote novo dentro da lista (append = adicionar no final).
    compras.append(nova_compra)
    
    # 4. Manda gravar tudo no arquivo (Save Game).
    salvar_dados(compras)
    print(f"Compra registrada em {data_atual}!")

def listar_compras(lista_para_imprimir=None):
    # Se ninguém passou uma lista específica, carrega a lista completa do arquivo.
    if lista_para_imprimir is None:
        print("\n--- Histórico de Compras ---")
        lista_para_imprimir = carregar_dados()

    # Se a lista estiver vazia (not lista)...
    if not lista_para_imprimir:
        print("Nenhuma compra encontrada.")
        return # Para a função aqui e vai embora.

    # Se tem coisa, passa item por item e manda o "maquiador" imprimir.
    for compra in lista_para_imprimir:
        _imprimir_compra(compra)

def alterar_compra():
    print("\n--- Alterar Compra ---")
    listar_compras() # Mostra tudo pro usuário saber o ID.
    
    try:
        id_op = int(input("ID para alterar: ")) # Pede o número.
    except ValueError:
        return # Se digitar letra, desiste.

    compras = carregar_dados()
    # Chama o detetive pra achar a compra certa.
    compra = _buscar_compra_por_id(compras, id_op)

    if not compra: # Se o detetive voltou com "None" (nada)...
        print("Não encontrado.")
        return

    # Aqui é o truque: Mostra o valor antigo. Se der ENTER vazio, mantém o antigo.
    novo_cli = input(f"Cliente ({compra['cliente']}): ")
    if novo_cli: # "Se a pessoa digitou algo..."
        compra['cliente'] = novo_cli # ...atualiza. Se não digitou, não faz nada.

    novo_prod = input(f"Produtos ({compra['produtos']}): ")
    if novo_prod: compra['produtos'] = novo_prod

    novo_val = input(f"Valor ({compra['valor_total']}): ")
    if novo_val:
        try:
            compra['valor_total'] = float(novo_val) # Tenta virar número
        except ValueError:
            pass # Se der erro, finge que nada aconteceu e mantém o valor velho.

    salvar_dados(compras) # Salva as mudanças.
    print("Atualizado!")

def excluir_compra():
    print("\n--- Excluir Compra ---")
    listar_compras()
    try:
        id_op = int(input("ID para excluir: "))
    except ValueError:
        return

    compras = carregar_dados()
    
    # Aqui a gente cria uma NOVA lista copiando todo mundo, MENOS o cara que a gente quer excluir.
    # É tipo: "Quem tem o ID diferente desse numero chato, entra na lista nova".
    nova_lista = [c for c in compras if c['id'] != id_op]

    # Se o tamanho da lista nova for igual da velha, significa que ninguém saiu (não achou o ID).
    if len(compras) == len(nova_lista):
        print("Não encontrado.")
    else:
        salvar_dados(nova_lista) # Salva a lista nova (sem o excluído).
        print("Excluído!")

def filtrar_compras():
    print("\n--- Filtrar ---")
    termo = input("Nome do cliente: ").lower() # Transforma tudo em minúsculo pra facilitar a busca.
    compras = carregar_dados()
    
    # Cria uma lista só com quem tem o 'termo' dentro do nome.
    filtradas = [c for c in compras if termo in c['cliente'].lower()]
    
    if not filtradas:
        print("Nenhum registro encontrado.")
    else:
        # Reutiliza a função de listar, mas agora só passa a lista filtrada.
        listar_compras(filtradas)