*** Settings ***
Documentation    Testovaci sada obsahuje vybrane testy pro validaci sluzeb rwa api. Pro prihlaseni do aplikace se
...              pouziva uzivatel: Katharina_Bernier

Library    ../../../../_common/
Library    ../../../keywords/rwa/SuiteMgmt.py
Library    ../../../keywords/rwa/BankAccounts.py
Library    ../../../keywords/rwa/Notifications.py
Library    ../../../keywords/rwa/Transactions.py
Library    ../../../keywords/rwa/UserDetail.py

Suite Setup       setup
Suite Teardown    teardown


*** Variables ***
${API_NAME}              rwa_api
${TD_DEL_NOTIFS}         api.testsuites.rwa.testdata.td_del_notifs
${TD_GET_BANK_ACC}       api.testsuites.rwa.testdata.td_get_bank_acc
${TD_GET_MATE_DETAIL}    api.testsuites.rwa.testdata.td_get_mate_detail
${TD_GET_NOTIFS_LIST}    api.testsuites.rwa.testdata.td_get_notifs_list
${TD_GET_RECEIVER_ID}    api.testsuites.rwa.testdata.td_get_receiver_id
${TD_GET_USER_DETAIL}    api.testsuites.rwa.testdata.td_get_user_detail
${TD_LOGIN_TO_RWA}       api.testsuites.rwa.testdata.td_login_to_rwa
${TD_LOGOUT_FROM_RWA}    api.testsuites.rwa.testdata.td_logout_from_rwa
${TD_SEND_MONEY}         api.testsuites.rwa.testdata.td_send_money


*** Test Cases ***
Get user detail
    [Documentation]    Test vrati detail prihlaseneho uzivatele
    [Tags]             get_user_detail    smoke
    get user detail    email

Get bank accounts
    [Documentation]    Test overi detail vychoziho bankovniho uctu prihlaseneho uzivatele
    [Tags]             get_bank_acc    smoke
    get bank accounts

Get notifications list
    [Documentation]    Test vrati seznam vsech notifikaci prihlaseneho uzivatele
    [Tags]             get_notif    smoke
    get notifications list

Delete n notifications
    [Documentation]    Test smaze n anebo vsechny notifikace prihlaseneho uzivatele podle vybraneho jmena v notifikaci
    [Tags]             del_notif    smoke
    get notifications list
    delete notifications    name=Edgar     cnt=${1}    #cnt=all

Send money
    [Documentation]    Test odesle platbu vybranemu prijemci ze seznamu pratel
    [Tags]             send_money    smoke
    send money         name=Tavares_Barrows    amount=${1}
