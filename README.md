# 🛠️ Utilitário de Manutenção do Windows

Este é um aplicativo desktop com interface gráfica desenvolvido em **Python** usando a biblioteca `customtkinter`, que centraliza ferramentas básicas de manutenção para sistemas Windows. É ideal para laboratórios, computadores compartilhados ou uso pessoal.

---

## 🚀 Funcionalidades

- **Limpeza de Disco**  
  Executa a ferramenta nativa de limpeza de disco do Windows (`cleanmgr`).

- **Limpeza de Arquivos Temporários**  
  Roda um script `.bat` personalizado que limpa a pasta `Temp` do usuário. Acompanhe o progresso da limpeza com uma **barra visual**.

- **Teste de Conectividade de Rede**  
  Executa comandos como `ping`, `tracert`, `nslookup` e `flushdns`, com exibição **em tempo real** dos resultados na interface.

- **Atualização do Sistema**  
  Executa comandos de atualização do Windows via script `.bat` (ex: `winget upgrade`, `sfc /scannow`, etc).

---

## 🖼 Interface

A interface é construída com `customtkinter` no estilo moderno, lembrando o **design do Windows 11**, com menu lateral e painel central dinâmico.

---

## ⚙️ Requisitos

- Python 3.11 ou superior  
- Bibliotecas:
  - `customtkinter`
  - `PyInstaller` (para empacotar em `.exe`)

Instale com:

```bash
pip install customtkinter pyinstaller
```
No terminal:
```bash
pyinstaller --noconsole --onefile --add-data "scripts\\*.bat;scripts" --add-data "icons\\logo.ico;icons" app2.py
```
Isso gerará um executável na pasta dist/.

---

## 📝 Observações

Certifique-se de que os scripts .bat tenham permissões adequadas.

O executável pode precisar ser executado como administrador, especialmente para ações como limpeza e atualizações.

O app pode travar se o .bat demorar e não for executado em uma thread separada (já tratado no código atual).

---

## 📌 Licença

Este projeto é open-source.

## 🙋‍♂️ Autores
Desenvolvido por Gabriel Araujo e Luiz Felipe Borges.
