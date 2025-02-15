import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.svg_manager import SvgManager

class DriverManager:
    def __init__(self, driver, slug_svg, arquivo='text_areas.txt'):
        self.driver = driver
        self.text_areas = self.load_env(arquivo)
        self.area, self.html_type = self.text_areas[slug_svg]
        self.svgs = SvgManager().obter_svg_list(slug_svg)
        self.wait = WebDriverWait(driver, 10)  # Timeout de 10 segundos

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
                
    def load_env(self, arquivo):
        env_data = {}
        with open(arquivo, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        key, value, html_type = parts
                        env_data[key] = (value, html_type)
                    else:
                        print(f"Linha inválida no arquivo de configuração: {line}")
        
        return env_data

    def limpar_textarea(self):
        """Limpa qualquer texto existente"""
        try:
            element = self.valida_tipo_html()

            element.clear()
            # Garante que o textarea está realmente vazio enviando CTRL+A e DELETE
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            return True
        except Exception as e:
            if e == "Message: element not interactable":
                return False
            else:
                print(f"Erro ao limpar caixa de texto: {e}")
                return False
            
    def valida_tipo_html(self):
        try:
            if self.html_type == 'CSS_SELECTOR':
                element = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.area))
                )
            elif self.html_type == 'XPATH':
                element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, self.area))
                )
            elif self.html_type == 'ID':
                element = self.wait.until(
                    EC.presence_of_element_located((By.ID, self.area))
                )
            else:
                raise ValueError(f"Tipo de HTML não suportado: {self.html_type}")
            
            return element
        except Exception as e:
            if e == "Message: element not interactable":
                return False
            else:
                print(f"Erro ao validar campo html: {e}")
                return False
            
    def clicar_botao_enviar(self):
        try:
            botao_enviar = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label^="Enviar"]'))
            )
            botao_enviar.click()
            return True
        except Exception as e:
            print(f"Erro ao clicar no botão de enviar: {e}")
            return False

    def enviar_mensagem(self, mensagem):
        try:
            # Limpa o textarea antes de inserir nova mensagem
            if not self.limpar_textarea():
                print("Aviso: Não foi possível limpar a caixa de texto")

            textarea = self.valida_tipo_html()
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
                if not self.clicar_botao_enviar():
                    textarea.send_keys(Keys.ENTER)
                time.sleep(6)
                return True
            
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            return False
        
    def finalizar(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Erro ao finalizar driver: {e}")