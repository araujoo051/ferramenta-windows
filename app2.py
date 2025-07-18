import customtkinter as ctk
import subprocess
import threading
import os
import sys

def resource_path(relative_path):
    """Retorna o caminho absoluto, funciona com PyInstaller e script normal."""
    try:
        base_path = sys._MEIPASS  # Pasta temporária do PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Utilitário de Manutenção do Windows")
        self.geometry("700x400")

        icon_path = resource_path("icons/logo.ico")
        self.iconbitmap(icon_path)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=150)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(self.sidebar, text="Menu", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)

        ctk.CTkButton(self.sidebar, text="Limpeza de Disco", command=self.limpeza_disco).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Limpeza Temp", command=self.iniciar_limpeza).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Teste de Conexão", command=self.teste_rede).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Reset de rede", command=self.reset_rede).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Reparar arquivos corrompidos", command=self.reparar_corrompidos).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Sair", command=self.quit).pack(pady=20, fill="x", padx=10)

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.content, text="Ferramentas de Manutenção do Windows", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

    def iniciar_limpeza(self):
        if not hasattr(self, 'progress'):
            self.progress = ctk.CTkProgressBar(self.content)
            self.progress.set(0)
            self.progress.pack(pady=10, padx=20)

        if not hasattr(self, 'label_status'):
            self.label_status = ctk.CTkLabel(self.content, text="Pronto", font=ctk.CTkFont(size=14))
            self.label_status.pack(pady=10)

        self.label_status.configure(text="Iniciando limpeza de arquivos temporários...")
        self.progress.set(0)
        thread = threading.Thread(target=self.executar_limpeza_temporarios)
        thread.start()

    def executar_limpeza_temporarios(self):
        if not hasattr(self, 'text_output'):
            self.text_output = ctk.CTkTextbox(self.content, width=500, height=200)
            self.text_output.pack(pady=10)
        else:
            self.text_output.delete("1.0", "end")
            self.text_output.pack()

        bat_path = resource_path("scripts/limpeza_temps.bat")

        processo = subprocess.Popen(
            [bat_path],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for linha in processo.stdout:
            linha = linha.strip()
            print(f"[BAT] {linha}")

            self.after(0, lambda l=linha: self.text_output.insert("end", l + "\n"))
            self.after(0, lambda: self.text_output.see("end"))

            if linha.startswith("[") and "]" in linha:
                try:
                    progresso_str = linha.split("]")[0].strip("[")
                    progresso = int(progresso_str)
                    status_msg = linha.split("]")[1].strip()
                    self.after(0, lambda p=progresso / 100: self.progress.set(p))
                    self.after(0, lambda msg=status_msg: self.label_status.configure(text=msg))
                except Exception:
                    pass

        processo.wait()
        self.after(0, lambda: self.label_status.configure(text="Limpeza finalizada!"))

    def limpeza_disco(self):
        if not hasattr(self, 'label_status'):
            self.label_status = ctk.CTkLabel(self.content, text="", font=ctk.CTkFont(size=14))
            self.label_status.pack(pady=10)

        bat_path = resource_path("scripts/limpeza_disco.bat")
        subprocess.call([bat_path], shell=True)
        self.label_status.configure(text="Limpeza de disco finalizada!")

    def teste_rede(self):
        if not hasattr(self, 'label_status'):
            self.label_status = ctk.CTkLabel(self.content, text="", font=ctk.CTkFont(size=14))
            self.label_status.pack(pady=10)

        if not hasattr(self, 'progress'):
            self.progress = ctk.CTkProgressBar(self.content)
            self.progress.set(0)
            self.progress.pack(pady=10, padx=20)

        if not hasattr(self, 'text_output'):
            self.text_output = ctk.CTkTextbox(self.content, width=500, height=200)
            self.text_output.pack(pady=10)
        else:
            self.text_output.delete("1.0", "end")

        self.text_output.pack()
        self.label_status.configure(text="Iniciando testes de rede...")
        self.progress.set(0)

        thread = threading.Thread(target=self.executar_teste_rede)
        thread.start()

    def executar_teste_rede(self):
        bat_path = resource_path("scripts/teste_rede.bat")

        processo = subprocess.Popen(
            [bat_path],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for i, linha in enumerate(processo.stdout, start=1):
            linha = linha.strip()
            print(linha)

            progresso = min(i * 10, 100)
            self.after(0, lambda p=progresso / 100: self.progress.set(p))

            self.after(0, lambda l=linha: self.text_output.insert("end", l + "\n"))
            self.after(0, lambda: self.text_output.see("end"))

        processo.wait()
        self.after(0, lambda: self.label_status.configure(text="Teste de rede finalizado!"))

    def reset_rede(self):
        if not hasattr(self, 'label_status'):
            self.label_status = ctk.CTkLabel(self.content, text="", font=ctk.CTkFont(size=14))
            self.label_status.pack(pady=10)
        if not hasattr(self, 'progress'):
            self.progress = ctk.CTkProgressBar(self.content)
            self.progress.set(0)
            self.progress.pack(pady=10, padx=20)
        if not hasattr(self, 'text_output'):
            self.text_output = ctk.CTkTextbox(self.content, width=500, height=200)
            self.text_output.pack(pady=10)
        else:
            self.text_output.delete("1.0", "end")

        self.text_output.pack()
        self.label_status.configure(text="Iniciando reset de rede...")
        self.progress.set(0)

        thread = threading.Thread(target=self.executar_reset_rede)
        thread.start()

    def executar_reset_rede(self):
        bat_path = resource_path("scripts/resetar_rede.bat")

        processo = subprocess.Popen(
            [bat_path],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for i, linha in enumerate(processo.stdout, start=1):
            linha = linha.strip()
            print(linha)

            progresso = min(i * 15, 100)
            self.after(0, lambda p=progresso / 100: self.progress.set(p))

            self.after(0, lambda l=linha: self.text_output.insert("end", l + "\n"))
            self.after(0, lambda: self.text_output.see("end"))

        processo.wait()
        self.after(0, lambda: self.label_status.configure(text="Reset de rede finalizado!"))

    def reparar_corrompidos(self):
        if not hasattr(self, 'label_status'):
            self.label_status = ctk.CTkLabel(self.content, text="", font=ctk.CTkFont(size=14))
            self.label_status.pack(pady=10)
        if not hasattr(self, 'progress'):
            self.progress = ctk.CTkProgressBar(self.content)
            self.progress.set(0)
            self.progress.pack(pady=10, padx=20)
        if not hasattr(self, 'text_output'):
            self.text_output = ctk.CTkTextbox(self.content, width=500, height=200)
            self.text_output.pack(pady=10)
        else:
            self.text_output.delete("1.0", "end")
        
        self.text_output.pack()
        self.label_status.configure(text="Iniciando reparo de arquivos corrompidos...")
        self.progress.set(0)
        thread = threading.Thread(target=self.executar_reparo_corrompidos)
        thread.start()
    
    def executar_reparo_corrompidos(self):
        bat_path = resource_path("scripts/reparar_corrompidos.bat")

        processo = subprocess.Popen(
            [bat_path],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        total_lines_estimada = 100  # Ajuste se souber o número aproximado de linhas/etapas
        linhas_lidas = 0

        for linha in processo.stdout:
            linha = linha.strip()
            print(f"[REPARO] {linha}")

            linhas_lidas += 1
            progresso = min(linhas_lidas / total_lines_estimada, 1.0)

            # Atualiza a caixa de texto com a saída do .bat
            self.after(0, lambda l=linha: self.text_output.insert("end", l + "\n"))
            self.after(0, lambda: self.text_output.see("end"))

            # Atualiza a barra de progresso
            self.after(0, lambda p=progresso: self.progress.set(p))

            # Atualiza o label de status se a linha tiver algum indicativo (opcional)
            # Exemplo: se o script imprime algo tipo "[50] Reparando arquivo..."
            if linha.startswith("[") and "]" in linha:
                try:
                    progresso_str = linha.split("]")[0].strip("[")
                    progresso_num = int(progresso_str)
                    status_msg = linha.split("]")[1].strip()
                    self.after(0, lambda p=progresso_num / 100: self.progress.set(p))
                    self.after(0, lambda msg=status_msg: self.label_status.configure(text=msg))
                except Exception:
                    pass

        processo.stdout.close()
        processo.wait()

        self.after(0, lambda: self.label_status.configure(text="Reparo de arquivos corrompidos finalizado!"))
        self.after(0, lambda: self.progress.set(1.0))




if __name__ == "__main__":
    app = App()
    app.mainloop()
