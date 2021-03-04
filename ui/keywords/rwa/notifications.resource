*** Settings ***
Documentation    Obecna klicova slova pro oraci s aplikaci

Library    ../../pageobjects/rwa/SideNavBar.py
Library    ../../PageObjects/rwa/Notifications.py


*** Keywords ***
Open menu notifications
    [Documentation]    Klikne na polozku Notifications v levem menu aplikace
    log to console    Oteviram menu Notifications
    click menu notifications
    wait for notification list
    log to console    Otevreno menu Notifications

Delete notifications
    [Arguments]    ${user}=${EMPTY}    ${action}=${EMPTY}    ${max_number_to_delete}=${20}
    [Documentation]    Vymaze postupne vsechna upozorneni ktera se tykaji daneho uzivatele {user} a dane akce {action}
    ...    lze filtrovat podle uzivatele, akce, kombinace nebo smazat vsechna upozorneni (v pripade prednastavenych
    ...    vstupnich parametru - prazdych retezcu)
    ${message}    set variable    Budou smazana upozorneni
    ${message}    set variable if    '${user}'!='${EMPTY}'    ${message} pro uzivatele "${user}"    ${message}
    ${message}    set variable if    '${action}'!='${EMPTY}'    ${message} pro akci "${action}"    ${message}
    log to console    ${message}.
    FOR    ${index}    IN RANGE    ${max_number_to_delete}
        wait for notification list
        ${response}    click notification dismiss button    ${user}    ${action}
        run keyword if    '${response}' == 'None'    run keywords
        ...    log to console    Pocet odstranenych upozorneni: ${index}
        ...    AND    exit for loop
        log to console    Bylo smazano upozorneni "${response}"
    END

