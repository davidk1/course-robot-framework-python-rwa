# testovaci data pro /login uzivatele Katharina_Bernier, pro jineho uzivatele je nutne data zmenit
# ocekavany vysledek je slovnik s detaily prihlaseneho uzivatele a krome "balance" se kontroluje 1:1 s odpovedi z api

request_method = 'post'
endpoint = 'login'

request_headers = {
    "Content-Type": "application/json;charset=UTF-8"
}

request_body = {
    "type": "LOGIN",
    "username": "Katharina_Bernier",
    "password": "s3cret"
}

expected_response = {
    "user": {
        "id": "t45AiwidW",
        "uuid": "6383f84e-b511-44c5-a835-3ece1d781fa8",
        "firstName": "Edgar",
        "lastName": "Johns",
        "username": "Katharina_Bernier",
        "password": "$2a$10$5PXHGtcsckWtAprT5/JmluhR13f16BL8SIGhvAKNP.Dhxkt69FfzW",
        "email": "Norene39@yahoo.com",
        "phoneNumber": "625-316-9882",
        "avatar": "https://avatars.dicebear.com/4.4/api/human/t45AiwidW.svg",
        "defaultPrivacyLevel": "public",
        "balance": "",
        "createdAt": "2019-08-27T23:47:05.637Z",
        "modifiedAt": "2020-05-21T11:02:22.857Z"
    }
}
