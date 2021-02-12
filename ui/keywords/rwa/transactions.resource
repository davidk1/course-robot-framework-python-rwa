*** Settings ***
Documentation    Klicova slova pro odeslani trasakci
Library    ../../pageobjects/rwa/SharedComponents.py
Library    ../../pageobjects/rwa/NewTransactionPage.py


*** Keywords ***
Send money
    [Arguments]    ${recipient_name}    ${amount}=12    ${description}=Money
    [Documentation]    Odesle prikaz k platbe pro zadaneho prijemce
    click new transaction button
    select_recipent by name    ${recipient_name}
    enter transaction amount    ${amount}
    enter transaction description    ${description}
    click transaction submit button