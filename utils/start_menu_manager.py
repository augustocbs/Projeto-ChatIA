from utils.mensagem_inicial_manager import MensagemInicialManager
from utils.palavra_manager import PalavraManager
from utils.svg_manager import SvgManager
from utils.env import POS_PALAVRA_PADRAO, SVG_PADRAO

class StartMenuManager:
    def __init__(self):
        self.mensagem_manager = MensagemInicialManager()
        self.palavra_manager = PalavraManager()
        self.svg_manager = SvgManager()

    def main(self):
        mensagem_inicial = None
        palavra_atual = None
        slug_svg = None

        while palavra_atual is None or slug_svg is None:
            result = self.mostrar_menu()
            if result is None:
                print("\nContinuando com configuração padrão...")
                palavra_atual = palavra_atual if palavra_atual is not None else POS_PALAVRA_PADRAO
                slug_svg = slug_svg if slug_svg is not None else SVG_PADRAO
                return mensagem_inicial, palavra_atual, slug_svg
            
            tipo_config, valor = result
            
            if tipo_config == "mensagem" and valor:
                mensagem_inicial = valor
                print("\nMensagem inicial configurada: ", valor)
            elif tipo_config == "palavra" and valor is not None:
                palavra_atual = valor
                print(f"\nPalavra inicial configurada: {valor}")
            elif tipo_config == "svg" and valor:
                slug_svg = valor
                print(f"\nSVG inicial configurado, tipo de botão: {valor}")

        return mensagem_inicial, palavra_atual, slug_svg
    
    def mostrar_menu(self):
        while True:
            print("\n=== Menu Inicial ===")
            print("1. Configurar Mensagem Inicial")
            print("2. Configurar Palavra")
            print("3. Configurar SVG")
            print("\nDigite o número da opção ou pressione Enter para continuar")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                mensagem = self._menu_mensagem()
                if mensagem:
                    return "mensagem", mensagem
                    
            elif opcao == "2":
                palavra = self._menu_palavra()
                if palavra is not None:  # Pode ser 0 (índice válido)
                    return "palavra", palavra
                    
            elif opcao == "3":
                svg = self._menu_svg()
                if svg is not None:
                    return "svg", svg
                
            elif opcao == "4" or not opcao:
                return None
                
            else:
                print("Opção inválida!")
                
    def _menu_mensagem(self):
        print("\n=== Configuração de Mensagem ===")
        
        if not self.mensagem_manager.listar_mensagens():
            return None
            
        while True:
            slug = input("\nDigite o slug da mensagem inicial desejada (ou Enter para pular): ").strip().lower()
            
            if not slug:  # Se pressionar Enter
                return None
                
            if slug in self.mensagem_manager.mensagens:
                return self.mensagem_manager.mensagens[slug]
                
            print("Slug inválido. Por favor, escolha um slug da lista")
            
    def _menu_palavra(self):
        print("\n=== Configuração de Palavra ===")
        
        print("\nPalavras disponíveis:")
        for i, palavra in enumerate(self.palavra_manager.palavras):
            print(f"{i}: {palavra}")
            
        while True:
            entrada = input("\nDigite o número da palavra (ou Enter para manter a atual): ").strip().lower()
            
            if not entrada:  # Se pressionar Enter
                return None
                
            try:
                indice = int(entrada)
                if 0 <= indice < len(self.palavra_manager.palavras):
                    return indice
                print("Número fora do intervalo válido")
            except ValueError:
                print("Entrada inválida, por favor digite um número válido")
    
    def _menu_svg(self):
        print("\n=== Configuração de SVG ===")
        
        if not self.svg_manager.listar_svgs():
            return None
            
        while True:
            slug = input("\nDigite o slug do SVG desejado (ou Enter para pular): ").strip().lower()
            
            if not slug:  # Se pressionar Enter
                return None
                
            if slug in self.svg_manager.svgs:
                return slug
                
            print("Slug inválido. Por favor, escolha um slug da lista")