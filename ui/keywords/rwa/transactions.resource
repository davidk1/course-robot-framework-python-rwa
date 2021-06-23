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
    [Documentation]   Vrati aktualni zustatek na uctu a tuto hodnotu ulozi do global promenne reference_account_balance
    log to console  ${\n}Nacitani aktualniho zustatku na uctu
    ${actual_account_balance}  get account balance
    set test variable  ${reference_account_balance}     ${actual_account_balance}
    log to console      aktualni vzse yustatku na uctu je: ${actual_account_balance}
    return from keyword  ${actual_account_balance}

Send money
    [Arguments]     ${recipient_name}  ${amount}=15  ${description}=Money
    [Documentation]     Odesle prikay k platbne pro zadaneho prijemce
    log to console   ${\n} Odeslano  ${amount}$ uzivateli  ${recipient_name}

    click new transaction button
    select recipient by name  ${recipient_name}
    enter transaction amount   ${amount}
    set test variable       ${transaction_amount}   ${amount}
    enter transaction description  ${description}
    submit transaction
    log to console   Zadani prikayu probehlo uspene - OK

Check account balance change
    [Arguments]   ${expected_balance_change}=${transaction_amount}
    ...     ${reference_account_balance}=${reference_account_balance}
     #tři tečky jsou pro robota příkaz, že text za tečkama je pokračování předchoyího řádku
    [Documentation]  ověři zda zmena zůstatku na uctu odpovida zaslane hodnote {transaction_amount}
    log to console  ${\n}vyhodnocene zmeny zustatku na uctu
    ${actual_account_balance}   get account balance
    ${result}   set variable
    ...    ${{${reference_account_balance} - ${actual_account_balance} == ${expected_balance_change}}}
    #vzorec rika, že reference minus actual by mělo být rovno expected - jde o python zápis výpočtu
    return from keyword if  ${result}
    ${err_message}  catenate  Nepodarilo se uspesne overit zmenu zustatku po odeslani platby
    ...   puvodni (referencni zustatek): ${reference_account_balance}
    ...   konecny zustatek: ${actual_account_balance}
    ...   ocekavana zmena zustatku (pohyb na uctu): ${expected_balance_change}.
    fail  ${err_message}

