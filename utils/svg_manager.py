import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SvgManager:
    def __init__(self, arquivo='svg_play_paths.txt', auxiliares=['svg_stop_paths.txt']):
        self.svgs = self._carregar_svgs(arquivo)
        self.arquivo = arquivo
        self.auxiliares = auxiliares

    def _carregar_svgs(self, arquivo):
        svgs = {}
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha and '|' in linha:
                        try:
                            slug, texto = linha.split('|', 1)
                            slug = slug.strip()
                            texto = texto.strip()
                            if slug and texto:  # Verifica se ambos não estão vazios
                                svgs[slug] = texto
                        except Exception as e:
                            print(f"Erro ao processar linha: {linha}. Erro: {e}")
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado.")
        except Exception as e:
            print(f"Erro ao carregar svgs: {e}")
        return svgs
            
    def validar_e_obter_svgs_auxiliares(self, slug):
        svgs_validos = {}
        regex_pattern = re.compile(r'svg_(.*?)_paths\.txt')
        
        for auxiliar in self.auxiliares:
            match = regex_pattern.search(auxiliar)
            if match:
                middle_text = match.group(1)
                try:
                    with open(auxiliar, 'r', encoding='utf-8') as f:
                        for linha in f:
                            linha = linha.strip()
                            if linha.startswith(slug + '|'):
                                _, texto = linha.split('|', 1)
                                svgs_validos[middle_text] = texto.strip()
                except FileNotFoundError:
                    print(f"Arquivo auxiliar {auxiliar} não encontrado.")
                except Exception as e:
                    print(f"Erro ao processar arquivo auxiliar {auxiliar}: {e}")

        return svgs_validos
    
    def listar_svgs(self):
        if not self.svgs:
            print("\nNenhum svg disponível.")
            return False
            
        print("\nSvgs disponíveis:")
        for slug, texto in self.svgs.items():
            preview = texto[:50] + "..." if len(texto) > 50 else texto
            print(f"\nSlug: {slug}")
            print(f"Preview: {preview}")
        return True
    
    def obter_svg(self, slug):
        return self.svgs.get(slug)
    
    def selecionar_svg(self):
        if not self.listar_svgs():
            return None
            
        max_tentativas = 3
        for tentativa in range(max_tentativas):
            slug = input("\nDigite o slug do svg desejado (ou Enter para pular): ").strip()
            
            if not slug:  # Se pressionar Enter, pula o svg
                print("Svg ignorado.")
                return None
                
            if slug in self.svgs:
                svgs = self.validar_e_obter_svgs_auxiliares(slug)
                svgs["play"] = self.svgs[slug]
                return svgs
                
            print(f"Slug inválido. Por favor, escolha um slug da lista (tentativa {tentativa + 1}/{max_tentativas})")
        
        print("Número máximo de tentativas excedido. Escolhendo svg padrão (Char).")
        return None

    def recarregar_svgs(self):
        """Recarrega os svgs do arquivo"""
        self.svgs = self._carregar_svgs(self.arquivo)