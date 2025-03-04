from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
from utils.keyboard_handler import KeyboardHandler
from utils.palavra_manager import PalavraManager
from utils.driver_manager import DriverManager
from utils.svg_manager import SvgManager
from utils.start_menu_manager import StartMenuManager
    

def main():
    try:
        # Configurações do Chrome
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        
        # Inicializa os gerenciadores
        svg_manager = SvgManager()
        driver = webdriver.Chrome(options=chrome_options)
        keyboard_handler = KeyboardHandler()
        palavra_manager = PalavraManager()
        start_menu_manager = StartMenuManager()
        
        # Mostra o menu inicial
        mensagem_inicial, palavra_atual, slug_svg = start_menu_manager.main()

        driver_manager = DriverManager(driver, slug_svg)
        palavra_manager.indice_atual = palavra_atual
        if mensagem_inicial is not None:
            driver_manager.enviar_mensagem(mensagem_inicial)
        
        # Inicia o monitoramento do teclado
        keyboard_handler.iniciar_monitoramento()
        
        print(f"\nPalavras carregadas: {palavra_manager.palavras}")
        print("\nPressione * a qualquer momento para trocar a palavra")
        print("Pressione Ctrl+C para encerrar o script")
        
        falhas_consecutivas = 0
        max_falhas = 3
        
        while keyboard_handler.continuar_execucao:
            try:
                if keyboard_handler.trocar_palavra:
                    print("\nTrocando palavra...")
                    palavra_manager.mostrar_menu()
                    keyboard_handler.trocar_palavra = False
                    print(f"\nUsando a palavra: {palavra_manager.obter_palavra_atual()}")
                
                palavra_atual = palavra_manager.obter_palavra_atual()
                if driver_manager.enviar_mensagem(palavra_atual):
                    falhas_consecutivas = 0  # Reset do contador de falhas
                else:
                    falhas_consecutivas += 1
                    print(f"Falha ao enviar mensagem ({falhas_consecutivas}/{max_falhas})")
                    
                    if falhas_consecutivas >= max_falhas:
                        print("Número máximo de falhas consecutivas atingido. Encerrando script...")
                        break
                        
                    time.sleep(5)  # Espera um pouco antes de tentar novamente
                
            except Exception as e:
                print(f"\nErro durante a execução: {e}")
                falhas_consecutivas += 1
                if falhas_consecutivas >= max_falhas:
                    print("Número máximo de falhas consecutivas atingido. Encerrando script...")
                    break
                time.sleep(5)
        
    except KeyboardInterrupt:
        print("\nScript interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro fatal: {e}")
        sys.exit(1)
    finally:
        print("\nFinalizando script...")
        keyboard_handler.finalizar()
        driver_manager.finalizar()

if __name__ == "__main__":
    main()