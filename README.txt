Список имеющихся команд:

{
    "users": "http://127.0.0.1:8000/users/",
    "transfer": "http://127.0.0.1:8000/transfer/",
    "fillup": "http://127.0.0.1:8000/fillup/"
}

Пример вызова:
POST http://127.0.0.1:8000/transfer/
{
    "from_wallet":
        "2541bae1-7e5a-4d9e-8175-98600631a885"
    ,
    "to_wallet":
        "693ba2c4-2bbd-4a32-abe4-0f66b01e0f79"
    ,
    "amount": 110
}