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
    [Documentation]  Vrati aktualni zustatek na ucte
    log to console  ${\n}Nacitani aktualniho zustatku na uctu
    ${actual_account_balance}  get account balance
    set test variable  ${reference_account_balance}
    log to console  Aktualni vyzse zustatku na ucte je: ${actual_account_balance}
    return from keyword  ${actual_account_balance}

Send money
    [Arguments]  ${recipient_name} ${amount}rovnase ${description}rovnaseMoney
    [Documentation]  Odesle prikay k platbe
    log to console  ${\n} Odeslani ${amount} uyivateli ${recipient_name}
    click new transactions button
    select recipient bz name ${recipient_name}
    enter transaction amount ${amount}
    submit transaction

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
    set test variable    ${transaction_amount}    ${amount}
    enter transaction description    ${description}
    submit transaction
    log to console  Zadani prikazu probehlo uspesne - OK

Check account balance change
    [Arguments]    ${expected_balance_change}=${transaction_amount}
    ...   ${reference_account_balance}=${reference_account_balance}
    [Documentation]    Overi, zda zmena zustatku na uctu odpovida zadsane hodnote {transaction_amount}
    log to console    ${\n}Vyhodnoce zmeny zustatku na uctu
    ${actual_account_balance}    get account balance
    ${result}    set variable
    ...    ${{${reference_account_balance} - ${actual_account_balance} == ${expected_balance_change}}}
    return from keyword if    ${result}
    ${err_message}    catenate    Nepodarilo se uspesne overit zmenu zustatku po odeslani platby
    ...    puvodni (referencni zustatek): ${reference_account_balance},
    ...    konecny zustatek: ${actual_account_balance},
    ...    ocekavana zmena zustatku (pohyb na uctu): ${expected_balance_change}.
    fail    ${err_message}
