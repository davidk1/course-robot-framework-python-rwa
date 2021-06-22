*** Settings ***
Documentation    Klicova slova pro odeslani trasakci
Library    ../../pageobjects/rwa/TopNavBar.py
Library    ../../pageobjects/rwa/SideNavBar.py
Library    ../../pageobjects/rwa/NewTransactionPage.py


*** Variables ***
${reference_account_balance}    ${0}
${transaction_amount}    12

*** Keywords ***
Get actual account balance
    [Documentation]    Vrati aktualni zustatek na uctu a tuto hodnotu ulozi do globalni promenne reference_account_balance
    log to console    ${\n}Nacitani aktualniho zustatku na uctu
    ${actual_account_balance}    get account balance
    set test variable      ${reference_account_balance}    ${actual_account_balance}
    log to console    Aktualni vyse zustatku na uctu je: ${actual_account_balance}
    return from keyword    ${actual_account_balance}

Send money
    [Arguments]    ${recipient_name}    ${amount}=12    ${description}=Money
    [Documentation]    Odesle prikaz k platbe pro s=zadaneho prijemce
    log to console    ${\n} Odeslani ${amount}$ uzivateli ${recipient_name}
    click new transaction button
    select recipient by name    ${recipient_name}
    enter transaction amount    ${amount}
    enter transaction description    ${description}
    submit transaction
    log to console  Zadani prikazu probehlo uspesne - OK

