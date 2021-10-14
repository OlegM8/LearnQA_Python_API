import requests

request_url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1. При запросе без передачи параметра method возвращает сообщение "Wrong method provided"
response1 = requests.get(request_url)
print(response1.text)

# 2. При отправке http-запроса не из списка возвращает 400 ошибку
response2 = requests.head(request_url, params={"method": "HEAD"})
print(response2.status_code)
print(response2.text)

# 3. При отправке запроса с правильным значением method возвращает сообщение "success":"!"
response3 = requests.get(request_url, params={"method": "GET"})
print(response3.text)


# 4. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок - delete + GET: {"success":"!"}

request_types = ["GET", "POST", "PUT", "DELETE"]

for i in request_types:
    response_get = requests.get(request_url, params={"method": i})
    response_post = requests.post(request_url, data={"method": i})
    response_put = requests.put(request_url, data={"method": i})
    response_delete = requests.delete(request_url, data={"method": i})
    print(f"get + {i}: {response_get.text}")
    print(f"post + {i}: {response_post.text}")
    print(f"put + {i}: {response_put.text}")
    print(f"delete + {i}: {response_delete.text}")

