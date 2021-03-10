*** Settings ***
Library    OperatingSystem
Library    ../../libraries/PythonSetting.py

# todo: pokud nebude nic delat, soubor setup.resource bude smazan
*** Keywords ***
UI suite setup
    [Documentation]    Nastaveni prostredi pro beh UI testu
    ...    Nastaveni cesty ke korenovemu adresari
    ${result}    set variable    tralala    #check pythonpath
    log to console    Nastaveni cest: ${result}
