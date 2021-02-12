receiver_name = 'Jessyca.Kuhic'  # nazev prijemce, kteremu se odeslou [$]
body = {
    "transactionType": "payment",
    "amount": 10,  # castka k odeslani v [$]
    "description": f'Penize od {receiver_name}',  # popis transakce
    "senderId": "",  # vyplni test nactenim suite variable ulozene v ramci loginu: ${USER_ID}
    "receiverId": ""  # vyplni test pomoci instancni promenne receiver_id
}
expected_response = {
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
