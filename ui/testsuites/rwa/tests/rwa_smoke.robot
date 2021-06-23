*** Settings ***
Documentation    Zakladni testy aplikace Real World Application

Library    ../../../../_common/
Resource    ../../../keywords/_common/browser.resource
Resource    ../../../keywords/rwa/auth.resource
Resource    ../../../keywords/rwa/transactions.resource
Resource    ../../../keywords/rwa/notifications.resource


Suite Setup    open browser to application    rwa    ${browser}
Suite Teardown    close all browsers

Variables    ../testdata/rwa_smoke_testdata.py


*** Variables ***
${selenium_command_delay}    0.3
${browser}    gc


*** Test Cases ***
Successful login to application
    [Documentation]    Uspesne prihlaseni do aplikace rwa
    [Tags]    login
    login to rwa    ${login_data}[username]    ${login_data}[password]
    logout from rwa


Send money to recipient
    [Documentation]     Odeslat platby
    [Tags]     trans
    [Setup]    login to rwa
    get actual account balance
    send money      ${transaction_data}[recipient]    ${transaction_data}[amount]    ${transaction_data}[description]
    check account balance change
    # hashtag je pro koment

    [Teardown]    logout from rwa

Delete notification
    [Documentation]  Smaze upozorneni
    [Tags]  notif
    [Setup]   login to rwa
    open menu notifications
    delete notifications    ${notification_data}[related_user]    ${notification_data}[related_action]
    [Teardown]

