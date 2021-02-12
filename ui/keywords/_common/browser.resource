*** Settings ***
Library    SeleniumLibrary
Library    ../../../_common/libraries/dataprovider/dataprovider.py


*** Variables ***


*** Keywords ***
Open browser to application
    [Documentation]    Otevre prohlizec na strance dane aplikace
    [Arguments]    ${application_name}    ${browser}=gc
    ${url}     get base url    ${application_name}
    open browser    ${url}    browser=${browser}