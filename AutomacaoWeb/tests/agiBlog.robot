*** Settings ***
Documentation       Suite dos testes - AgiBlog
Resource            ../resources/main.robot
Test Teardown       Close Browser


*** Test Cases ***
Redirecionar para endereço correto
    [Tags]    Redirect    Sucesso
    Dado que acesso AgiBank pela url antiga
    Então serei redirecionado ao endereço correto

Validar menus principais via header
    Dado que estou endereço correto do agiblog
    Quando eu clicar no menu "O Agibank"
    Então o título da página será "O Agibank"
    Quando eu clicar no menu "Produtos"
    Então o título da página será "Produtos"
    Quando eu clicar no menu "Serviços"
    Então o título da página será "Serviços"
    Quando eu clicar no menu "Suas finanças"
    Então o título da página será "Suas finanças"
    Quando eu clicar no menu "Seus benefícios"
    Então o título da página será "Seus benefícios"
    Quando eu clicar no menu "Sua segurança"
    Então o título da página será "Sua segurança"
    Quando eu clicar no menu "Stories"
    Então o título da página será "Story"


Pesquisa por post específico
    [Tags]  Busca    Sucesso
    Dado que estou endereço correto do agiblog
    Quando pesquiso o termo 'Empréstimo para Aposentado: o que é, como fazer e qual a taxa de juros?'
    Então deve exibir o resultado da busca com sucesso


Pesquisa por post inexistente
    [Tags]  Busca    Falha
    Dado que estou endereço correto do agiblog
    Quando pesquiso o termo 'Isso nao funciona'
    Então deve exibir o resultado da busca sem successo


Voltar para HomePage via Logo - tela cheia
  Dado que estou endereço correto do agiblog
  Quando eu clicar no menu "O Agibank"
  E volto para home via logo
  Então serei redirecionado ao endereço correto