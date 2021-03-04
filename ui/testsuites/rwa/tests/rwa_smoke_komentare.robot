*** Settings ***
Documentation    Zakladni testy aplikace Real World Application

Library    ../../../../_common/libraries/SetProjectRoot.py
Resource    ../../../keywords/_common/browser.resource
Resource    ../../../keywords/rwa/auth.resource
Resource    ../../../Keywords/rwa/transactions.resource
Resource    ../../../Keywords/rwa/general.resource

# testovaci data pro testovaci sadu
Variables    ../testdata/rwa_smoke_testdata.py

# Suite Setup - neni pouzit
# Test Setup - neni pouzit
Test Teardown    close browser
# Suite Teardown - neni pouzit

*** Variables ***
# Definice globalnich parametru ktere mohou byt pouzit v testovaci sade

*** Test Cases ***
Succesfull login to application
    [Documentation]    Prihlaseni do aplikace - uspesne
    [Tags]    login
    [Setup]    open browser to application    rwa
    login to rwa    ${login_data}[username]    ${login_data}[password]
    logout from rwa
#    [Teardown] - neni pouzit

Send money to recipient
    [Documentation]    Odeslani platby - uspesne
    [Tags]    transaction
    [Setup]    open browser to application    rwa
    login to rwa
    get actual account balance
    send money    ${transaction_data}[recipient]    ${transaction_data}[amount]    ${transaction_data}[description]
    get actual account balance
    check account balance change
    logout from rwa
#    [Teardown] - neni pouzit

Delete notification
    [Documentation]    Sazani notifikace
    [Tags]    notification
    [Setup]    open browser to application    rwa
    login to rwa
#    [Teardown] - neni pouzit
