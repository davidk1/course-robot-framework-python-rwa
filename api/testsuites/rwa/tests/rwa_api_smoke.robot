*** Settings ***
Documentation    Testovaci sada obsahuje vybrane testy pro validaci rwa api. Pro prihlaseni do api se pouziva
...              uzivatel: Katharina_Bernier.1234567890

Library    ../../../../_common/
Library    ../../../keywords/rwa/SuiteSetup.py
Library    ../../../keywords/rwa/Auth.py
Library    ../../../keywords/rwa/BankAccounts.py
Library    ../../../keywords/rwa/Notifications.py
Library    ../../../keywords/rwa/Transactions.py
Library    ../../../keywords/rwa/SuiteTeardown.py

Suite Setup       setup
Suite Teardown    teardown


*** Variables ***
${API_NAME}               rwa_api
${LOGIN}                  api.testsuites.rwa.testdata.login
${LOGOUT}                 api.testsuites.rwa.testdata.logout
${GET_BANK_ACC}           api.testsuites.rwa.testdata.get_bank_acc
${DEL_NOTIF}              api.testsuites.rwa.testdata.del_notif
${SEND_MONEY}             api.testsuites.rwa.testdata.send_money


*** Test Cases ***
Get bank account
    [Documentation]    Test overi spravnost detailu vychoziho bankovniho uctu prihlaseneho uzivatele.
    [Tags]             get_bank_acc    smoke
    get bank account

Get notifications
    [Documentation]    Test vrati seznam vsech notifikaci prihlaseneho uzivatele.
    [Tags]             get_notif    smoke
    get notification list

Delete n notifications
    [Documentation]    Test smaze n anebo vsechny notifikace prihlaseneho uzivatele podle vybraneho jmena v notifikaci.
    [Tags]             del_notif    smoke
    get notification list
    delete notifications    name=Edgar     cnt=${1}    #cnt=all

Send money
    [Documentation]    Test odesle platbu vybranemu prijemci ze seznamu pratel.
    [Tags]             send_money    smoke
    get receiver id    name=Tavares_Barrows
    send money    name=Tavares_Barrows    amount=${1}
