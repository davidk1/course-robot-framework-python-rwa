*** Settings ***

Library     ../../../../_common/
Library     ../../../keywords/rwa/SuiteMgmt.py
Library     ../../../keywords/rwa/Notifications.py
Suite Setup  setup
Suite Teardown  teardown

*** Variables ***
${API_NAME}              rwa_api
${TD_LOGIN_TO_RWA}       api.testsuites.rwa.testdata.td_login_to_rwa
${TD_LOGOUT_FROM_RWA}    api.testsuites.rwa.testdata.td_logout_from_rwa
${TD_GET_NOTIFS_LIST}    api.testsuites.rwa.testdata.td_get_notifs_list

*** Test Cases ***
Get notifications list
    [Documentation]  Test vrati seznam notifikovanych uzivatelu
    [Tags]  smoke
    get notifications list
