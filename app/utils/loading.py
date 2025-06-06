import sys
import time
import threading
from typing import Optional


class Loading:
    def __init__(self, message: str = "Processando"):
        """
        Inicializa o loading

        Args:
            message: Mensagem exibida antes da animacao
        """
        self.message = message
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()  # Lock para sincronização
        self._last_length = 0  # Controla o tamanho da última linha

        self._frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

    def _clear_line(self):
        """Limpa a linha atual do terminal."""
        sys.stdout.write('\r' + ' ' * self._last_length + '\r')
        sys.stdout.flush()

    def _animate(self):
        """Metodo privado que controla a animacao"""

        frame_index = 0
        while self._running:
            with self._lock:  # Protege a seção crítica
                frame = self._frames[frame_index % len(self._frames)]
                line = f"\r{self.message} {frame}"
                sys.stdout.write(line)
                sys.stdout.flush()
                self._last_length = len(line)
            time.sleep(0.1)
            frame_index += 1
        with self._lock:
            self._clear_line()

    def start(self):
        """Inicia a animação de loading"""
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._animate)
            self._thread.start()

    def stop(self):
        """Para a animação de loading"""
        if self._running:
            self._running = False
            if self._thread:
                self._thread.join()

    def print_protected(self, *args, **kwargs):
        """Metodo seguro para print durante o loading"""
        with self._lock:
            self._clear_line()
            print(*args, **kwargs)
            # Re-exibe o loading se ainda estiver ativo
            if self._running:
                frame = self._frames[0]  # Frame simples para retomar
                line = f"\r{self.message} {frame}"
                sys.stdout.write(line)
                sys.stdout.flush()
                self._last_length = len(line)


    def __enter__(self):
        """Permite uso com context manager (with)"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garante que o loading sera parado ao sair do contexto"""
        self.stop()
