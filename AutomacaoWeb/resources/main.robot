*** Settings ***
Documentation
library     SeleniumLibrary
Library    OperatingSystem
Resource    keywords.resource
Library     SeleniumLibrary
Library    Screenshot
Library    String
Resource    PageObjects/page_home.robot

*** Variables ***
${URL_BASE}           https://blogdoagi.com.br/
${URL_BASE_REDIR}     https://blog.agibank.com.br/
${OUTPUT_DIR}    ..\AutomacaoWeb\output
