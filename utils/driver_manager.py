from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DriverManager:
    def __init__(self, driver, svgs):
        self.driver = driver
        self.svgs = svgs
        self.wait = WebDriverWait(driver, 10)  # Timeout de 10 segundos
        self.limpar_textarea()  # Limpa o textarea ao inicializar
        # self.limpar_prompt_textarea()  # Limpa o prompt-textarea ao inicializar

    def verificar_icone(self, type):
        try:
            botao = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label^="Enviar"]'))
            )

            svg_path = botao.find_element(By.TAG_NAME, 'path').get_attribute('d')

            # Path do ícone
            path = self.svgs[type]
            return svg_path == path
        except Exception as e:
            print(f"Erro ao verificar ícone: {e}")
            return False
                
    def limpar_textarea(self):
        """Limpa qualquer texto existente no textarea"""
        try:
            textarea = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea'))
            )
            textarea.clear()
            # Garante que o textarea está realmente vazio enviando CTRL+A e DELETE
            textarea.send_keys(Keys.CONTROL + "a")
            textarea.send_keys(Keys.DELETE)
            return True
        except Exception as e:
            if e == "Message: element not interactable":
                return False
            else:
                print(f"Erro ao limpar textarea: {e}")
                return False
            
    def enviar_mensagem(self, mensagem):
        try:
            # Limpa o textarea antes de inserir nova mensagem
            if not self.limpar_textarea():
                print("Aviso: Não foi possível limpar o textarea")

            # if not self.limpar_prompt_textarea():
            #     print("Aviso: Não foi possível limpar o prompt-textarea")
            
            textarea = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea'))
            )
            textarea.send_keys(mensagem)
            
            max_tentativas = 12  # 1 minuto (5s * 12)
            tentativas = 0
            
            while self.verificar_icone("stop"):
                print("Ícone de stop detectado. Aguardando 5 segundos...")
                time.sleep(5)
                tentativas += 1
                if tentativas >= max_tentativas:
                    print("Tempo máximo de espera excedido. Pulando mensagem...")
                    return False
            
            while self.verificar_icone("play"):
                print("Ícone de play detectado. Enviando mensagem...")
                textarea.send_keys(Keys.RETURN)
                time.sleep(6)  # Aguarda 6 segundos após enviar a mensagem para evitar bugs
                return True
            
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return False
        
    def finalizar(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Erro ao finalizar driver: {e}")