*** Settings ***
Documentation    Testovaci sada obsahuje vybrane testy pro validaci sluzeb rwa api. Pro prihlaseni do aplikace se
...              pouziva vychozi uzivatel: Katharina_Bernier

Library    ../../../../_common/
Library    ../../../keywords/rwa/SuiteMgmt.py


Suite Setup       setup
Suite Teardown    teardown
Documentation       testovací sada obsahuje vybrane testz pro validaci služeb

Library     ../../../../_common/
Library     ../../../keywords/rwa/SuiteMgmt.py
#Library     ../../../keywords/rwa/Auth.py
Library     ../../../keywords/rwa/Notifications.py

Suite Setup         setup
Suite Teardown      teardown

*** Variables ***
${API_NAME}              rwa_api
${TD_LOGIN_TO_RWA}       api.testsuites.rwa.testdata.td_login_to_rwa
${TD_LOGOUT_FROM_RWA}    api.testsuites.rwa.testdata.td_logout_from_rwa
${TD_GET_NOTIFS_LIST}    api.testsuites.rwa.testdata.td_get_notifs_list


*** Test Cases ***
#Login to RWA
#    login to rwa   $TD_LOGIN_TO_RWA
#   sleep   5
#    logout from rwa
#Test run
#    pass execution    testovaci beh

Get notifications list
    [Documentation]    Test vrati seznam vsech notifikaci prihlaseneho uzivatele
    [Tags]    Smoke
    get notifications list