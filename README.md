# Robot Framework - Automação
Este projeto tem o objetivo registrar os testes do Blog da instituição Agibank

## Instalação
Robot framework precisa do [Python](https://www.python.org/downloads/) v3.10.2+ para executar.

#### Após esses abaixo procedimentos é necessário reiniciar a máquina
>Caso tenha que executar testes WEB, necessárioo instalar e iniciar a library BrowserLibrary [BrowserLibrary](https://chromedriver.chromium.org/downloads)

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

## Executando o projeto local

Para executar o projeto basta abrir o CMD (prompt de comando) na pasta raiz do projeto
Executar o comando
>robot -d results automacaoweb\tests\*.robot

E para gerar um relatório bonito utilize o Report do Metrics (será gerado um arquivo html na pasta):
> cd results && robotmetrics

## Esteira de testes automatizados CI para Github Actions
Existe um script pronto na pasta workflows para utilização no Actions


#### Material de apoio

[Documentação Python](https://docs.python.org/3/)
[Documentação Robot Framework](https://robotframework.org/)
[Documentação Report Metrics](https://github.com/adiralashiva8/robotframework-metrics)
