import requests
import time

request_url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Отправляем GET запрос без параметров и сохраняем токен и количество секунд в переменные
response = requests.get(request_url)
response_json = response.json()

token = response_json['token']
seconds = response_json['seconds']


# Проверяем заврос с токеном, он нам возвращает статус "Job is NOT ready"
response_with_token = requests.get(request_url, params={"token": token})
print(response_with_token.text)


# Отправляем запрос спустя нужное количество секунд и проверяем правльный статус "Job is ready"
time.sleep(seconds)
response_after_time = response_with_token = requests.get(request_url, params={"token": token, })
print(response_after_time.text)
