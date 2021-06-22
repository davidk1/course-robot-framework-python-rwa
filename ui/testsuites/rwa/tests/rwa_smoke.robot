*** Settings ***
Documentation    Zakladni testy aplikace Real World Application

Library    ../../../../_common/
Resource    ../../../keywords/_common/browser.resource
Resource    ../../../keywords/rwa/auth.resource
Resource    ../../../keywords/rwa/transactions.resource


Suite Setup    open browser to application    rwa    ${browser}
Suite Teardown    close all browsers

Variables    ../testdata/rwa_smoke_testdata.py


*** Variables ***
${selenium_command_delay}    0.3
${browser}    ff


*** Test Cases ***
Successful login to application
    [Documentation]    Uspesne prihlaseni do aplikace rwa
    [Tags]    login
    login to rwa    ${login_data}[username]    ${login_data}[password]
    logout from rwa

Send money to recipient
  [Documentation]  Send money to account of some recipient
  [Tags]  Area : payments, Priority : High
  [Setup]  login to rwa
  get actual account balance    # Nactu aktualni stav uctu a ulozim do promenne
  send money   ${transaction_data}[recipient]  ${transaction_data}[amount]  ${transaction_data}[description]
  #check account balance change   # Porovnam puvodni stav s aktualnim a odeslanymi penezi, musi platit puvodni = novy + send
  [Teardown]  logout from rwa