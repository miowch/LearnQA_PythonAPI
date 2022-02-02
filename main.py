import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

print(str(response.history).count("301"))
print(response.url)