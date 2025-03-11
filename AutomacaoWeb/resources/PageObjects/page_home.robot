*** Settings ***
Documentation       Aqui temos o mapeamento dos elementos e localizadores separado por telas


*** Variables ***
${SEARCH_ICON}   xpath=//*[@id="ast-desktop-header"]/div/div/div/div/div[3]/div[2]/div/div
${TXT_BUSCAR}   id=search-field
${MENU_ITEM_XPATH}    xpath=//a/span[2][contains(text(),'{MENU_NAME}')]
${logo}                    xpath=//*[@id="ast-desktop-header"]/div/div/div/div/div[1]/div[1]/div