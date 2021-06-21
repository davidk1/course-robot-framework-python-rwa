*** Settings ***
Library    ../../pageobjects/rwa/LoginPage.py
Library    ../../pageobjects/rwa/SideNavBar.py


*** Keywords ***
Login to rwa
    [Arguments]    ${username}=${login_data}[username]    ${password}=${login_data}[password]
    [Documentation]    Prihlasi se do aplikace rwa
    log to console    ${\n}Prihlaseni se do aplikace rwa
    enter username    ${username}
    enter password    ${password}
    click sign in button
    wait for logout button
    log to console    Prihlaseni se do aplikace rwa probehlo uspesne - OK


Logout from rwa
    [Documentation]    Odhlasi se z aplikace rwa
    log to console    ${\n}Odhlaseni z aplikace rwa
    click logout button
    wait_for_sign_in_button
    log to console    Odhlaseni z aplikace rwa probehlo uspesne - OK
