from utils.mensagem_inicial_manager import MensagemInicialManager
from utils.palavra_manager import PalavraManager

class StartMenuManager:
    def __init__(self):
        self.mensagem_manager = MensagemInicialManager()
        self.palavra_manager = PalavraManager()
        
    def mostrar_menu(self):
        while True:
            print("\n=== Menu Inicial ===")
            print("1. Configurar Mensagem Inicial")
            print("2. Configurar Palavra")
            print("3. Continuar")
            print("\nDigite o número da opção ou pressione Enter para continuar")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if not opcao:  # Se pressionar Enter
                return None, None  # Continua sem configurar nada
                
            if opcao == "1":
                mensagem = self._menu_mensagem()
                if mensagem == "voltar":
                    continue
                if mensagem:
                    return "mensagem", mensagem
                    
            elif opcao == "2":
                palavra = self._menu_palavra()
                if palavra == "voltar":
                    continue
                if palavra is not None:  # Pode ser 0 (índice válido)
                    return "palavra", palavra
                    
            elif opcao == "3":
                return None, None
                
            else:
                print("Opção inválida!")
                
    def _menu_mensagem(self):
        print("\n=== Configuração de Mensagem ===")
        print('Digite "voltar" para retornar ao menu principal')
        
        if not self.mensagem_manager.listar_mensagens():
            return None
            
        while True:
            slug = input("\nDigite o slug da mensagem inicial desejada (ou Enter para pular): ").strip().lower()
            
            if not slug:  # Se pressionar Enter
                return None
                
            if slug == "voltar":
                return "voltar"
                
            if slug in self.mensagem_manager.mensagens:
                return self.mensagem_manager.mensagens[slug]
                
            print("Slug inválido. Por favor, escolha um slug da lista")
            
    def _menu_palavra(self):
        print("\n=== Configuração de Palavra ===")
        print('Digite "voltar" para retornar ao menu principal')
        
        print("\nPalavras disponíveis:")
        for i, palavra in enumerate(self.palavra_manager.palavras):
            print(f"{i}: {palavra}")
            
        while True:
            entrada = input("\nDigite o número da palavra (ou Enter para manter a atual): ").strip().lower()
            
            if not entrada:  # Se pressionar Enter
                return None
                
            if entrada == "voltar":
                return "voltar"
                
            try:
                indice = int(entrada)
                if 0 <= indice < len(self.palavra_manager.palavras):
                    return indice
                print("Número fora do intervalo válido")
            except ValueError:
                print("Entrada inválida, por favor digite um número válido")