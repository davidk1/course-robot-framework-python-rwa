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
  [Documentation]  Vrati aktualni zustatek a tuto hodnotu ulozi do globalni promenne
  log to console  ${\n} Nacitani aktualniho zustatku
  ${actual_account_balance}    get account balance
  set test variable  ${reference_account_balance}  ${actual_account_balance}
  log to console    Aktualni vyse zustatku na uctu je: ${actual_account_balance}
  return from keyword  ${actual_account_balance}

Send money
  [Arguments]  ${recipient_name}  ${amount}=12  ${description}=money
  [Documentation]  Odesle prikaz k platbe pro zadaneho prijemce
   log to console    Odeslani ${amount} uzivateli
   click new transaction button
   select recepient by name  ${recipient_name}
   enter transaction amount  ${amount}
   set test variable  ${transaction_amount}    ${amount}
   enter_transaction_description  ${description}
   submit transaction
   log to console  Zadani prikazu probehlo uspesne - OK

check account balance change
    [Arguments]   ${expected_balance_change}=${transaction_amount}
    ...    ${reference_account_balance}=${reference_account_balance}
    [Documentation]    Overi, zda zmena zustatku na uctu odpovida
    log to console     ${\n}Vzhodnoceni ymenz na uctu
    ${actual_account_balance}    get account balance
    ${result}    set variable
    ...    ${{${reference_account_balance} - ${actual_account_balance} == 30}}  #${expected_balance_change}
    return from keyword if  ${result}
    ${err_message}    catenate  Nepodarilo se uspesne overit zmenu zustatku po odeslani platby
    ...    puvodni  (referencni zustatek): ${reference_account_balance}
    ...    konecny zustatek:  ${actual_account_balance}
    ...    ocekavana zmena yustatku:  ${expected_balance_change}.
    fail    ${err_message}
