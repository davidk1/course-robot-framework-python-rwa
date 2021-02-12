*** Settings ***
Documentation    Obecna klicova slova pro oraci s aplikaci

Library    ../../pageobjects/rwa/SharedComponents.py


*** Keywords ***
Get actual bank account
    [Documentation]    Vrati aktualni zustatek na uctu
    ${actual_account_balance}    get account balance
    log to console    ${actual_account_balance}