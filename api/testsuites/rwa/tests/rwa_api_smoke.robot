*** Settings ***
Documentation    Testovaci sada obsahuje vybrane testy pro validaci sluzeb rwa api. Pro prihlaseni do aplikace se
...             pouziva vychozi uzivatel: Katharina_Bernier

Library     ../../../../_common/
Library     ../../../keywords/rwa/SuiteMgmt.py
Library     ../../../keywords/rwa/Notifications.py
Library     ../../../keywords/rwa/BankAccounts.py

Suite Setup     setup
Suite Teardown  teardown

*** Variables ***
${API_NAME}              rwa_api
${TD_LOGIN_TO_RWA}       api.testsuites.rwa.testdata.td_login_to_rwa
${TD_LOGOUT_FROM_RWA}    api.testsuites.rwa.testdata.td_logout_from_rwa
${TD_GET_NOTIFS_LIST}    api.testsuites.rwa.testdata.td_get_notifs_list
${TD_GET_BANK_ACC}       api.testsuites.rwa.testdata.td_get_bank_acc

*** Test Cases ***
Get notifications list
    [Documentation]    Test vrati seznam vsech notifikaci prihlaseneho uzivatele. Nevim, jestli jsem dala commit
    [Tags]   smoke
    get notifications list

Get bank accounts
    [Documentation]    Test overi detail vzchoziho bankovniho uctu prihlaseneho uzivatele
    [Tags]    smoke    account
    get bank accounts