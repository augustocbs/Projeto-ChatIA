from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from utils.keyboard_handler import KeyboardHandler
from utils.palavra_manager import PalavraManager
from utils.driver_manager import DriverManager
from utils.mensagem_inicial_manager import MensagemInicialManager

def main():
    # Configurações do Chrome
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    # Inicializa os gerenciadores
    driver = webdriver.Chrome(options=chrome_options)
    keyboard_handler = KeyboardHandler()
    palavra_manager = PalavraManager()
    driver_manager = DriverManager(driver)
    mensagem_inicial_manager = MensagemInicialManager()
    
    # Seleciona e envia a mensagem inicial
    mensagem_inicial = mensagem_inicial_manager.selecionar_mensagem()
    if mensagem_inicial:
        print("\nEnviando mensagem inicial...")
        driver_manager.enviar_mensagem(mensagem_inicial)
        time.sleep(5)  # Pequena pausa após enviar a mensagem inicial
    
    # Inicia o monitoramento do teclado
    keyboard_handler.iniciar_monitoramento()
    
    print(f"\nPalavras carregadas: {palavra_manager.palavras}")
    print("\nPressione * a qualquer momento para trocar a palavra")
    
    try:
        while keyboard_handler.continuar_execucao:
            if keyboard_handler.trocar_palavra:
                print("\nTrocando palavra...")
                palavra_manager.mostrar_menu()
                keyboard_handler.trocar_palavra = False
                print(f"\nUsando a palavra: {palavra_manager.obter_palavra_atual()}")
            
            palavra_atual = palavra_manager.obter_palavra_atual()
            driver_manager.enviar_mensagem(palavra_atual)
            
    except KeyboardInterrupt:
        print("\nScript interrompido pelo usuário.")
        
    finally:
        keyboard_handler.finalizar()
        driver_manager.finalizar()

if __name__ == "__main__":
    main()