request_method = 'post'
endpoint = 'transactions'

request_headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

request_body = {
    "amount": 10,                                 # castka k odeslani v [$]
    "description": 'Vracim za obed...',           # popis transakce
    "senderId": None,                             # vyplni test
    "receiverId": None,                           # vyplni test
    "transactionType": "payment"
}

expected_response = {                             # hodnoty "" se v odpovedi z api nekontroluji, None vyplni test
    "transaction": {
        "id": "",
        "uuid": "",
        "amount": None,
        "description": None,
        "receiverId": None,
        "senderId": None,
        "privacyLevel": "public",
        "status": "complete",
        "createdAt": "",
        "modifiedAt": ""
    }
}
