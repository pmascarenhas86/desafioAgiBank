# Robot Framework - Automação

Este projeto tem o objetivo de registrar os testes do Blog da instituição Agibank

## Instalação

Robot Framework precisa do [Python](https://www.python.org/downloads/) v3.10.2+ para executar.

```sh
python --version
```

```sh
pip install -r requirements.txt
```

Para verificar se as bibliotecas foram instaladas com sucesso, execute o comando:

```sh
pip list
```

## Instalando o ChromeDriver

Para rodar testes automatizados no navegador **Google Chrome**, é necessário instalar o **ChromeDriver**.

### 1. Verifique a versão do seu Google Chrome

Abra o Chrome e acesse:

```
chrome://settings/help
```

Anote a versão do navegador (exemplo: `120.0.6099.129`).

### 2. Baixe o ChromeDriver compatível

Acesse o site oficial do ChromeDriver: [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/)

Baixe a versão correspondente ao seu navegador.

### 3. Extraia e configure o caminho

1. Extraia o arquivo baixado.
2. Mova o executável `chromedriver.exe` para um diretório acessível (exemplo: `C:\chromedriver`).
3. Adicione este diretório ao **Path** do Windows:
   - Pressione `Win + R`, digite `sysdm.cpl` e pressione Enter.
   - Acesse **Avançado > Variáveis de Ambiente**.
   - Em **Variáveis do Sistema**, edite `Path` e adicione `C:\chromedriver`.
   - Clique em OK para salvar.

Para testar se está funcionando, execute no terminal:

```sh
chromedriver --version
```

Deve exibir a versão do ChromeDriver.

## Executando o projeto local

Para executar o projeto, basta abrir o CMD (prompt de comando) na pasta raiz do projeto e executar:

```sh
robot -d results automacaoweb\tests\*.robot
```

E para gerar um relatório mais detalhado utilize o Report Metrics:

```sh
cd results && robotmetrics
```

## Esteira de testes automatizados CI para Github Actions

Existe um script pronto na pasta `workflows` para utilização no **GitHub Actions**.

#### Material de apoio

- [Documentação Python](https://docs.python.org/3/)
- [Documentação Robot Framework](https://robotframework.org/)
- [Documentação Report Metrics](https://github.com/adiralashiva8/robotframework-metrics)

