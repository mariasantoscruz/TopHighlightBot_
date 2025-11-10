# Bot Buscador de Highlights no YouTube

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4-green?style=for-the-badge&logo=selenium)

Este projeto é um script de automação em Python desenhado para encontrar rapidamente os melhores highlights de times no YouTube.

Em vez de pesquisar manualmente e adivinhar qual vídeo tem o melhor conteúdo, este bot automatiza o processo. Ele pesquisa pelo nome do time, analisa os resultados, e abre o vídeo com o **maior número de visualizações** para você assistir.

## 🤖 Como Funciona

O bot simula as ações de um usuário comum diretamente no navegador Google Chrome:

1.  **Inicialização**: O script inicia o Google Chrome usando o Selenium. Ele aplica `ChromeOptions` especiais (como `--disable-blink-features=AutomationControlled`) para que o YouTube não o identifique como um bot.
2.  **Pesquisa**: Ele acessa `youtube.com`, lida com o pop-up de cookies (se aparecer) e digita a consulta de busca (ex: "Real Madrid highlights") na barra de pesquisa.
3.  **Análise (Parsing)**: Após a página de resultados carregar, o bot utiliza o `VideoParser` para:
    * Encontrar todos os elementos de vídeo na página.
    * Extrair o texto de visualizações de cada um (ex: "1.2M views", "10K views").
    * Converter esse texto em um número inteiro (ex: `1200000`, `10000`) para permitir uma comparação precisa.
4.  **Seleção**: O script compara os números de visualizações e identifica qual vídeo da lista é o mais popular.
5.  **Navegação**: O bot navega para a URL do vídeo com mais visualizações.
6.  **Espera**: O script principal (`main.py`) fica em modo de espera, permitindo que o usuário assista ao vídeo. Para encerrar o programa, basta que o usuário **feche a janela do navegador manualmente**.

## ✨ Características Principais

* **Automação com Selenium**: Utiliza a biblioteca Selenium e o `webdriver-manager` para controlar o navegador Chrome de forma robusta.
* **Modo Anti-Detecção**: O navegador é iniciado com flags especiais para evitar ser identificado como um bot, permitindo o acesso à versão padrão do YouTube.
* **Parsing Inteligente**: Capaz de ler e converter o texto de visualizações (como "1.2M views", "10K views", "808 views") em números inteiros para uma comparação precisa.
* **Fluxo Interativo**: O bot conclui sua tarefa e devolve o controle ao usuário, aguardando que ele feche o navegador para finalizar o script de forma limpa.

## ⚙️ Instalação e Execução: Passo a Passo

Siga estes passos para configurar o ambiente e rodar o projeto.

### 1. Pré-requisitos

* **Python 3.10** ou superior instalado.
* **Google Chrome** instalado (o bot usará este navegador).

### 2. Clonar o Repositório

Primeiro, clone este repositório para sua máquina local e entre na pasta do projeto:

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

### 3\. Criar Ambiente Virtual

É uma boa prática usar um ambiente virtual (`.venv`) para isolar as dependências do projeto.

```bash
# Crie o ambiente virtual
python -m venv .venv
```

### 4\. Ativar o Ambiente Virtual

Você precisa ativar o ambiente antes de instalar os pacotes.

**No Windows (PowerShell):**

```bash
.\.venv\Scripts\Activate.ps1
```

**No macOS ou Linux:**

```bash
source .venv/bin/activate
```

Você saberá que funcionou pois o nome do ambiente (ex: `(.venv)`) aparecerá no início do seu prompt de comando.

### 5\. Instalar as Dependências

Este projeto usa `selenium` para automação e `webdriver-manager` para baixar e gerenciar o driver do Chrome automaticamente.

Instale o arquivo requirements.txt para obter as bibliotecas necessárias.

```bash
pip install -r requirements.txt
```

### 6\. Executar o Bot

Com o ambiente ativado e os pacotes instalados, execute o script `main.py`:

```bash
python main.py
```

### 7\. Interagir com o Bot

1.  O terminal solicitará: `Enter the team name to search for:`
2.  Digite o nome do time (ex: `Corinthians`) e pressione `Enter`.
3.  Uma nova janela do Chrome será aberta. O bot fará a pesquisa e abrirá o vídeo com mais visualizações.
4.  O terminal exibirá a mensagem:
    > `The browser will remain open. Close the browser window to exit.`
5.  Quando terminar de assistir, **simplesmente feche a janela do Chrome**. O script no terminal detectará isso e será encerrado automaticamente.
