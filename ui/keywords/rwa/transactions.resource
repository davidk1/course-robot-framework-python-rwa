*** Settings ***
Documentation    Klicova slova pro odeslani trasakci
Library    ../../pageobjects/rwa/TopNavBar.py
Library    ../../pageobjects/rwa/SideNavBar.py
Library    ../../pageobjects/rwa/NewTransactionPage.py


*** Variables ***
${reference_account_balance}    ${0}
${transaction_amount}    12
${actual_account_balance}

*** Keywords ***
save account balance
    [Documentation]  Provede zjisteni a ulozeni zustatku do promenne reference_account_balance
    log to console  ${\n}Nacitani aktualniho zustatk
    ${actual_account_balance}           get account balance
    set test variable   ${reference_account_balance}    ${actual_account_balance}
    log to console  Aktualni vyse zustatku je ${actual_account_balance}
    return from keyword  ${actual_account_balance}

send money
    [Arguments]  ${recepient_name}  ${amount}=12  ${note}=Money
    [Documentation]  Provede odeslani transakce
    log to console  ${\n} Odeslani ${amount}$ uzivateli ${recepient_name}
    click new transaction button
    select recipient by name  ${recepient_name}
    enter transaction amount  ${amount}
    set test variable   ${transaction_amount}   ${amount}
    enter transaction note  ${note}
    submit transaction
    log to console  zadani prikazu probehlo uspesne - OK

check account balance change
    [Arguments]  ${expected_balance_change}=${transaction_amount}
    ...     ${reference_account_balance}=${reference_account_balance}
    [Documentation]  Overeni zmeny zustatku po zaslani penez
    log to console  ${\n} Vyhodnoceni zmeny zustatku
    ${actual_account_balance}   get account balance
    ${result}   set variable    ${{${reference_account_balance} - ${actual_account_balance} == ${expected_balance_change}}}
    return from keyword if      ${result}
    ${err_message}  catenate    Nepodarilo se uspesne overit zmenu zustatku po odeslani platby
    ...     puvodni (referencni zustatek):  ${reference_account_balance}
    ...     konecny zustatek:   ${actual_account_balance}
    ...     ocekavana zmena zustatku:   ${expected_balance_change}.
    fail    ${err_message}


