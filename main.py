# Importa o arquivo gestor.py que a gente criou. Sem isso, ele não sabe fazer nada.
import gestor 

def exibir_menu():
    """Só imprime texto na tela e pega o número que o usuário digitou."""
    print("\n--- Gestão de Compras de Clientes ---")
    print("1. Cadastrar Compra")
    print("2. Listar Todas as Compras")
    print("3. Alterar Compra")
    print("4. Excluir Compra")
    print("5. Filtrar Compras (por Cliente)")
    print("0. Sair")
    return input("Escolha uma opção: ") # Devolve o que o usuário digitou.

def loop_principal():
    """
    Essa função é um vício (recursiva).
    Ela roda, e no final, chama ela mesma de novo.
    Só para quando o usuário pede pra sair.
    """
    opcao = exibir_menu() # Chama o menu e guarda a escolha na variável 'opcao'.

    # Agora é só um monte de "Se for isso, faça aquilo".
    if opcao == '1':
        gestor.cadastrar_compra() # Chama a função lá do outro arquivo.
    elif opcao == '2':
        gestor.listar_compras()
    elif opcao == '3':
        gestor.alterar_compra()
    elif opcao == '4':
        gestor.excluir_compra()
    elif opcao == '5':
        gestor.filtrar_compras()
    elif opcao == '0':
        print("Saindo... Até logo!")
        return # O 'return' aqui sem chamar nada mata a função. É o fim do programa.
    else:
        print("Opção inválida, tente novamente.")

    # A MÁGICA RECURSIVA:
    # A função chama ela mesma de novo! Isso cria o "loop" eterno até alguém digitar 0.
    loop_principal()

# --- O BOTÃO DE START ---
# Essa linha estranha significa: "Se eu estiver rodando esse arquivo direto (dando play nele)..."
if __name__ == "__main__":
    # ...Então comece o jogo!
    loop_principal()