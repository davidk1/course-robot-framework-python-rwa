*** Settings ***
Library    SeleniumLibrary
Library    ../../../_common/libraries/dataprovider/dataprovider.py


*** Variables ***


*** Keywords ***
Open browser to application
    [Documentation]    Otevre prohlizec na strance dane aplikace
    [Arguments]    ${application_name}    ${browser}=gc
    log to console    Oteviram prohlizec ${browser} na strance aplikace ${application_name}
    ${url}     get base url    ${application_name}
    open browser    ${url}    browser=${browser}
    maximize browser window
    set selenium speed    ${selenium_command_delay}
    log to console    Prohlizec otevren - OK