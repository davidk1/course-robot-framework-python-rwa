*** Settings ***
Documentation    Zakladni testy aplikace Real World Application

Library    ../../../../_common/
Resource    ../../../keywords/_common/browser.resource
Resource    ../../../keywords/rwa/auth.resource
Resource    ../../../Keywords/rwa/transactions.resource
Resource    ../../../Keywords/rwa/notifications.resource

Suite Setup    open browser to application    rwa
Suite Teardown    close all browsers

Variables    ../testdata/rwa_smoke_testdata.py


*** Variables ***
${selenium_command_delay}    0.3


*** Test Cases ***
Successful login to application
    [Documentation]    Prihlaseni do aplikace - uspesne
    [Tags]    login
    login to rwa    ${login_data}[username]    ${login_data}[password]
    logout from rwa

Send money to recipient
    [Documentation]    Odeslani platby - uspesne
    [Tags]    transaction    trans
    [Setup]    login to rwa
    get actual account balance
    send money    ${transaction_data}[recipient]    ${transaction_data}[amount]    ${transaction_data}[description]
    check account balance change
    [Teardown]    logout from rwa

Delete notification
    [Documentation]    Smazani upozorneni
    [Tags]    notifications    notif
    [Setup]    login to rwa
    open menu notifications
    delete notifications    user=${notification_data}[related_user]    action=${notification_data}[related_action]
    [Teardown]    logout from rwa
