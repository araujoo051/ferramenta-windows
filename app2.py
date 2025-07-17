import customtkinter as ctk
import subprocess
import threading

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Utilitário de Manutenção do Windows")
        self.geometry("700x400")
        self.iconbitmap(r"C:\Users\gabriel.araujo\Documents\App Limpeza\icons\fundatec.ico")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Layout principal com 2 colunas
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=150)
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        self.sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(self.sidebar, text="Menu", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)

        ctk.CTkButton(self.sidebar, text="Limpeza de Disco", command=self.limpeza_disco).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Limpeza Temp", command=self.iniciar_limpeza).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Teste de Conexão", command=self.teste_rede).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Atualizar Sistema", command=self.executar_bat4).pack(pady=5, fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="Sair", command=self.quit).pack(pady=20, fill="x", padx=10)

        # Conteúdo principal
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
        processo = subprocess.Popen(
            [r"C:\Users\gabriel.araujo\Documents\App Limpeza\scripts\limpeza_temp.bat"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for linha in processo.stdout:
            linha = linha.strip()
            print(f"[BAT] {linha}")

            if linha.startswith("["):
                try:
                    progresso_str = linha.split("]")[0].strip("[")
                    progresso = int(progresso_str)
                    status_msg = linha.split("]")[1].strip()
                    self.after(0, lambda p=progresso / 100: self.progress.set(p))
                    self.after(0, lambda msg=status_msg: self.label_status.configure(text=msg))
                except Exception:
                    pass  # ignora erros de formatação

        processo.wait()
        self.after(0, lambda: self.label_status.configure(text="Limpeza finalizada!"))
        self.after(0, lambda: self.btn.configure(state="normal"))

    def limpeza_disco(self):
        if not hasattr(self, 'label_status'):
            self.label_status = ctk.CTkLabel(self.content, text="", font=ctk.CTkFont(size=14))
            self.label_status.pack(pady=10)

        subprocess.call([r"C:\Users\gabriel.araujo\Documents\App Limpeza\scripts\limpeza_disco.bat"], shell=True)
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
            self.text_output.delete("1.0", "end")  # limpa se já existe

        self.text_output.pack()  # mostra
        self.label_status.configure(text="Iniciando testes de rede...")
        self.progress.set(0)

        thread = threading.Thread(target=self.executar_teste_rede)
        thread.start()


    def executar_teste_rede(self):
        processo = subprocess.Popen(
            [r"C:\Users\gabriel.araujo\Documents\App Limpeza\scripts\teste_rede.bat"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for i, linha in enumerate(processo.stdout, start=1):
            linha = linha.strip()
            print(linha)

            # Simula progresso
            progresso = min(i * 10, 100)
            self.after(0, lambda p=progresso / 100: self.progress.set(p))

            # Mostra no Textbox
            self.after(0, lambda l=linha: self.text_output.insert("end", l + "\n"))
            self.after(0, lambda: self.text_output.see("end"))  # scroll automático

        processo.wait()
        self.after(0, lambda: self.label_status.configure(text="Teste de rede finalizado!"))


    def executar_bat4(self):
        subprocess.call([r"C:\Users\gabriel.araujo\Documents\App Limpeza\scripts\atualizar_sistema.bat"], shell=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
