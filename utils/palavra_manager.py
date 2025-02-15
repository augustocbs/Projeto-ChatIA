class PalavraManager:
    def __init__(self, arquivo='palavras.txt'):
        self.palavras = self._carregar_palavras(arquivo)
        self.indice_atual = 0
        self.arquivo = arquivo
        
    def _carregar_palavras(self, arquivo):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                palavras = [linha.strip() for linha in f.readlines() if linha.strip()]
                return palavras if palavras else ["continue"]  # Palavra padrão se arquivo estiver vazio
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado. Usando palavra padrão.")
            return ["continue"]
        except Exception as e:
            print(f"Erro ao carregar palavras: {e}")
            return ["continue"]
            
    def obter_palavra_atual(self):
        if not self.palavras:
            return "continue"
        return self.palavras[self.indice_atual % len(self.palavras)]
    
    def obter_palavras(self):
        return self.palavras
        
    def mostrar_menu(self):
        print("\nPalavras disponíveis:")
        for i, palavra in enumerate(self.palavras):
            print(f"{i}: {palavra}")
        
        max_tentativas = 3
        for tentativa in range(max_tentativas):
            try:
                entrada = input("\nDigite o número da palavra (ou Enter para manter a atual): ").strip()
                if not entrada:  # Se pressionar Enter, mantém a palavra atual
                    return True
                    
                novo_indice = int(entrada)
                if 0 <= novo_indice < len(self.palavras):
                    self.indice_atual = novo_indice
                    return True
                print("Número fora do intervalo válido")
            except ValueError:
                print(f"Entrada inválida, por favor digite um número válido (tentativa {tentativa + 1}/{max_tentativas})")
        
        print("Número máximo de tentativas excedido. Mantendo palavra atual.")
        return False
        
    def recarregar_palavras(self):
        """Recarrega as palavras do arquivo"""
        self.palavras = self._carregar_palavras(self.arquivo)
        self.indice_atual = 0  # Reset do índice ao recarregar