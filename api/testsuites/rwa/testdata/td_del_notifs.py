name = 'Edgar'             # jmeno, jehoz notifikace se smazou
cnt = 'all'                # pocet notifikaci ke smazani: vsechny / jednotlive: [int] / 'all'[str]

request_method = 'patch'
endpoint = 'notification_id'

request_headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

request_body = {
    "id": None,            # id notifikace ke smazani, vyplni test
    "isRead": True
}
