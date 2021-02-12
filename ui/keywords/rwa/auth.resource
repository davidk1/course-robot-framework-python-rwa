*** Settings ***
Library    ../../pageobjects/rwa/LoginPage.py
Library    ../../pageobjects/rwa/SharedComponents.py


*** Keywords ***
Login to rwa
    [Arguments]    ${username}=${login_data}[username]    ${password}=${login_data}[password]
    [Documentation]    Prihlasi se do aplikace rwa
# todo: misto sleep nastavit selenium speed
    sleep    1s
    enter username    ${username}
    sleep    1s
    enter password    ${password}
    sleep    1s
    click sign in button
    sleep    1s

Logout from rwa
    [Documentation]    Odhlasi se z aplikace rwa
    click logout button
