*** Settings ***
Documentation    Testovaci sada obsahuje vybrane testy pro validaci sluzeb rwa api. Pro prihlaseni do aplikace se
...              pouziva vychozi uzivatel: Katharina_Bernier

Library    ../../../../_common/
Library    ../../../keywords/rwa/SuiteMgmt.py


Suite Setup       setup
Suite Teardown    teardown


*** Variables ***
${API_NAME}              rwa_api
${TD_LOGIN_TO_RWA}       api.testsuites.rwa.testdata.td_login_to_rwa
${TD_LOGOUT_FROM_RWA}    api.testsuites.rwa.testdata.td_logout_from_rwa


*** Test Cases ***
Test run
    pass execution    testovaci beh
