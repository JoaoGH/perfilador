from app.document_manager import DocumentManager
from app.pre_processor import PreProcessor

def show_menu():
    print("\n=== MENU PRINCIPAL ===")
    print("1 - Carregar arquivos PDF")
    print("2 - Coleta de informações")
    print("3 - Pré-processamento")
    print("4 - Visualizar documentos carregados")
    print("5 - Executar pipeline completo em um documento")
    print("6 - Sair")

def main():
    manager = DocumentManager()

    while True:
        show_menu()
        opc = input("Escolha uma opção: ")
        if opc == "1":
            manager.load_pdf()
        elif opc == "2":
            print("Não implementado")
        elif opc == "3":
            preprocessor = PreProcessor()
            preprocessor.execute()
        elif opc == "4":
            manager.list_documents()
        elif opc == "5":
            print("Não implementado")
        elif opc == "6":
            print("Saindo")
            break
        else:
            print("Opção Invalida")


if __name__ == '__main__':
    main()

