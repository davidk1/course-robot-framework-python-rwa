*** Settings ***
Documentation
# misto setup.resource importuju rovnou knihovnu, pokud by resource delal jen jednu vec
Library    ../../../../_common/libraries/SetProjectRoot.py
#Resource    ../../../keywords/_common/setup.resource
Resource    ../../../keywords/_common/browser.resource
Resource    ../../../keywords/rwa/auth.resource
Resource    ../../../Keywords/rwa/transactions.resource
Resource    ../../../Keywords/rwa/general.resource

# testovaci data pro testovaci sadu
Variables    ../testdata/rwa_smoke_testdata.py
# todo: puvodni suite setup byl pouzit jen pro nastaveni cesty ke korenovemu adresari, pokud nedela nic jineho tak staci import knihovy ktera to zaridi
#Suite Setup    ui_suite_setup


*** Variables ***


*** Test Cases ***
Successful login to application
    [Documentation]    Prihlaseni do aplikace - uspesne
    [Tags]    login
    [Setup]    open browser to application    rwa
    login to rwa    ${login_data}[username]    ${login_data}[password]
    logout from rwa
    [Teardown]    close browser

Send money to recipient
    [Documentation]    Odeslani platby - uspesne
    [Tags]    transaction
    [Setup]    open browser to application    rwa
    login to rwa
    #get balance
    send money    ${transaction_data}[recipient]    ${transaction_data}[amount]    ${transaction_data}[description]
    #chek balance
    logout from rwa
    [Teardown]    close browser
