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
Library     ../../../keywords/rwa/Auth.py

Suite Setup         setup
Suite Teardown      teardown

*** Variables ***
${API_NAME}              rwa_api
${TD_LOGIN_TO_RWA}       api.testsuites.rwa.testdata.td_login_to_rwa
${TD_LOGOUT_FROM_RWA}    api.testsuites.rwa.testdata.td_logout_from_rwa


*** Test Cases ***
#Login to RWA
#    login to rwa   $TD_LOGIN_TO_RWA
#   sleep   5
#    logout from rwa
Test run
    pass execution    testovaci beh
