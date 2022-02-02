import requests
import random

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
http_methods = ["POST", "GET", "PUT", "DELETE"]
methods = ["POST", "GET", "PUT", "DELETE"]


def send_request(http_method="any", url=url, method="no method"):
    if http_method == "any":
        http_method = random.choice(http_methods)

    match method:
        case "no method":
            params = None
        case "any":
            params = {"method": f"{http_method}"}
        case _:
            params = {"method": f"{method}"}

    match http_method:
        case "GET":
            return requests.get(url, params=params)
        case "POST":
            return requests.post(url, data=params)
        case "PUT":
            return requests.put(url, data=params)
        case "DELETE":
            return requests.delete(url)
        case _:
            return requests.head(url)


'''
1
Expected status code: 200
Expected text: "Wrong method provided"
'''
print("STEP 1")
response_on_random_request_with_no_method = send_request()
print(response_on_random_request_with_no_method.status_code)
print(response_on_random_request_with_no_method.text)

'''
2
Expected status code: 400
Expected text: Empty
'''
print("STEP 2")
response_on_request_with_type_out_of_the_list = send_request(http_method="head")
print(response_on_request_with_type_out_of_the_list.status_code)
print(response_on_request_with_type_out_of_the_list.text)

'''
3
Expected status code: 200
Expected text: {"success":"!"}
'''
print("STEP 3")
response_on_correct_request = send_request(method="any")
print(response_on_correct_request.status_code)
print(response_on_correct_request.text)

'''
4
Expected output: "DELETE-request with method DELETE in params returns wrong response!"
'''
print("STEP 4")
for http_method in http_methods:
    for method in methods:
        response = send_request(http_method=http_method, method=method)
        if http_method != method and response.text == '{"success":"!"}':
            print(f'{http_method}-request with method {method} in params returns wrong response!')
        elif http_method == method and response.text == "Wrong method provided":
            print(f'{http_method}-request with method {method} in params returns wrong response!')