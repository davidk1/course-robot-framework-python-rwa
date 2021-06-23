*** Settings ***
Documentation    Zakladni testy aplikace Real World Application

Library    ../../../../_common/
Resource    ../../../keywords/_common/browser.resource
Resource    ../../../keywords/rwa/auth.resource


Suite Setup    open browser to application    rwa    ${browser}
Suite Teardown    close all browsers

Variables    ../testdata/rwa_smoke_testdata.py
Resource  ../../../keywords/rwa/transactions.resource
Resource  ../../../keywords/rwa/notifications.resource
*** Variables ***
${selenium_command_delay}    0.3
${browser}    chrome


*** Test Cases ***
Login test
   [Documentation]    Uspesne prihlaseni do aplikace rwa
    [Tags]    login
    login to rwa    ${login_data}[username]    ${login_data}[password]
    logout from rwa

Send money to recepient
    [Documentation]  Uspesne odeslani penez prijemci
    [Tags]  transaction
    [Setup]  Login to rwa
    save account balance  #toto je komentar
    send money  ${transaction_data}[recipient]    ${transaction_data}[amount]    ${transaction_data}[note]
    check account balance change
    [Teardown]  logout from rwa

Delete notifications
    [Documentation]  smazani notif
    [Tags]  notif
    [Setup]  login to rwa
    open menu notifications
    delete notifications    ${notification_data}[related_user]      ${notification_data}[related_action]
    [Teardown]  logout from rwa