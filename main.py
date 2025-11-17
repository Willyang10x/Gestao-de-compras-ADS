import gestor 

def exibir_menu():

    print("\n--- Gestão de Compras de Clientes ---")
    print("1. Cadastrar Compra")
    print("2. Listar Todas as Compras")
    print("3. Alterar Compra")
    print("4. Excluir Compra")
    print("5. Filtrar Compras (por Cliente)")
    print("0. Sair")
    return input("Escolha uma opção: ")

def loop_principal():

    opcao = exibir_menu()

    if opcao == '1':
        gestor.cadastrar_compra()
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
        return 
    else:
        print("Opção inválida, tente novamente.")

    loop_principal()

if __name__ == "__main__":
    loop_principal()