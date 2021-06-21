*** Settings ***
Documentation    Klicova slova pro odeslani trasakci
Library    ../../pageobjects/rwa/TopNavBar.py
Library    ../../pageobjects/rwa/SideNavBar.py
Library    ../../pageobjects/rwa/NewTransactionPage.py


*** Variables ***
${reference_account_balance}    ${0}
${transaction_amount}    12

*** Keywords ***
