from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DriverManager:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Timeout de 10 segundos
        self.limpar_textarea()  # Limpa o textarea ao inicializar
        
    def verificar_icone_play(self):
        try:
            botao = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Enviar mensagem…"]'))
            )
            svg_path = botao.find_element(By.TAG_NAME, 'path').get_attribute('d')
            
            # Path do ícone play
            path_play = "M3.113 6.178C2.448 4.073 4.64 2.202 6.615 3.19l13.149 6.575c1.842.921 1.842 3.55 0 4.472l-13.15 6.575c-1.974.987-4.166-.884-3.501-2.99L4.635 13H9a1 1 0 1 0 0-2H4.635z"
            
            return svg_path == path_play
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
            print(f"Erro ao limpar textarea: {e}")
            return False
            
    def enviar_mensagem(self, mensagem):
        try:
            # Limpa o textarea antes de inserir nova mensagem
            if not self.limpar_textarea():
                print("Aviso: Não foi possível limpar o textarea")
            
            textarea = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea'))
            )
            textarea.send_keys(mensagem)
            
            max_tentativas = 12  # 1 minuto (5s * 12)
            tentativas = 0
            
            while not self.verificar_icone_play():
                print("Ícone de stop detectado. Aguardando 5 segundos...")
                time.sleep(5)
                tentativas += 1
                if tentativas >= max_tentativas:
                    print("Tempo máximo de espera excedido. Pulando mensagem...")
                    return False
            
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