*** Settings ***
Resource    main.robot

*** Variables ***

${LBL_RESULTADO_FALHO}    Lamentamos, mas nada foi encontrado para sua pesquisa, tente novamente com outras palavras.


*** Keywords ***
Dado que acesso AgiBank pela url antiga
    Open Browser    ${URL_BASE}    chrome
    Maximize Browser Window


Dado que estou endereço correto do agiblog
    Open Browser    ${URL_BASE_REDIR}    chrome
    Maximize Browser Window

Quando pesquiso o termo '${texto}'
    Wait Until Keyword Succeeds    5x    1s    Execute JavaScript    return document.readyState === 'complete'
    E aguardo surgir o campo Busca
    Input Text   ${TXT_BUSCAR}    ${texto}
    Press Keys    ${TXT_BUSCAR}    ENTER
    Set test Variable    ${termo}    ${texto}


Então deve exibir o resultado da busca com sucesso
    Wait Until Page Contains    ${termo}


Então deve exibir o resultado da busca sem successo
    Wait Until Page Contains    ${LBL_RESULTADO_FALHO}

Então serei redirecionado ao endereço correto
    Wait Until Location Is Not    ${URL_BASE}
    Location Should Be    ${URL_BASE_REDIR}


E aguardo surgir o campo Busca
    Wait Until Keyword Succeeds    5x    1s    Ativar campo Busca


Ativar campo Busca
    Wait Until Element Is Visible    ${SEARCH_ICON}
    Click Element    ${SEARCH_ICON}
    Wait Until Element Is Visible    ${TXT_BUSCAR}


Quando eu clicar no menu "${menu_name}"
    ${xpath}    Replace String    //a/span[2][contains(text(),'{MENU_NAME}')]        {MENU_NAME}    ${menu_name}
    Wait Until Element Is Visible    ${xpath}    timeout=5s
    Click Element    ${xpath}
    Wait Until Keyword Succeeds    5x    1s    Execute JavaScript    return document.readyState === 'complete'
    Wait Until Location Is Not     ${URL_BASE_REDIR}

Então o título da página será "${titulo}"
    ${titulo_pagina}    Get Text   xpath=//h1[1]
    Should Be Equal As Strings    ${titulo_pagina}    ${titulo}

E volto para home via logo
    Wait Until Element Is Visible    ${logo}    timeout=10s
    Click Element    ${logo}
    Wait Until Keyword Succeeds    5x    1s    Execute JavaScript    return document.readyState === 'complete'
    Wait Until Location Is     ${URL_BASE_REDIR}
