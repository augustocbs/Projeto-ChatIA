import keyboard
import threading
import time

class KeyboardHandler:
    def __init__(self):
        self.trocar_palavra = False
        self.continuar_execucao = True
        self._lock = threading.Lock()  # Adiciona lock para thread safety
        
    def iniciar_monitoramento(self):
        thread_tecla = threading.Thread(target=self._verificar_tecla)
        thread_tecla.daemon = True
        thread_tecla.start()
        
    def _verificar_tecla(self):
        while self.continuar_execucao:
            try:
                if keyboard.is_pressed('*'):
                    with self._lock:
                        self.trocar_palavra = True
                    time.sleep(0.5)  # Evita múltiplos registros da mesma tecla
            except Exception as e:
                print(f"Erro ao verificar tecla: {e}")
                time.sleep(1)  # Espera um pouco antes de tentar novamente
                
    def finalizar(self):
        with self._lock:
            self.continuar_execucao = False