class MensagemInicialManager:
    def __init__(self, arquivo='mensagens_iniciais.txt'):
        self.arquivo = arquivo
        self.mensagens = self._carregar_mensagens(arquivo)
        
    def _carregar_mensagens(self, arquivo):
        mensagens = {}
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
                                mensagens[slug] = texto
                        except Exception as e:
                            print(f"Erro ao processar linha: {linha}. Erro: {e}")
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado.")
        except Exception as e:
            print(f"Erro ao carregar mensagens: {e}")
        return mensagens
        
    def listar_mensagens(self):
        if not self.mensagens:
            print("\nNenhuma mensagem inicial disponível.")
            return False
            
        print("\nMensagens disponíveis:")
        for slug, texto in self.mensagens.items():
            preview = texto[:50] + "..." if len(texto) > 50 else texto
            print(f"\nSlug: {slug}")
            print(f"Preview: {preview}")
        return True
        
    def obter_mensagem(self, slug):
        return self.mensagens.get(slug)
        
    def selecionar_mensagem(self):
        if not self.listar_mensagens():
            return None
            
        max_tentativas = 3
        for tentativa in range(max_tentativas):
            slug = input("\nDigite o slug da mensagem inicial desejada (ou Enter para pular): ").strip()
            
            if not slug:  # Se pressionar Enter, pula a mensagem inicial
                print("Mensagem inicial ignorada.")
                return None
                
            if slug in self.mensagens:
                return self.mensagens[slug]
                
            print(f"Slug inválido. Por favor, escolha um slug da lista (tentativa {tentativa + 1}/{max_tentativas})")
        
        print("Número máximo de tentativas excedido. Pulando mensagem inicial.")
        return None
        
    def recarregar_mensagens(self):
        """Recarrega as mensagens do arquivo"""
        self.mensagens = self._carregar_mensagens(self.arquivo)