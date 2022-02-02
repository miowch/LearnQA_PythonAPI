import time
import requests

url = "https://playground.learnqa.ru/ajax/api/longtime_job"


def create_task():
    response = requests.get(url)
    return response.json()


def is_ready(token):
    response = requests.get(url, params={"token": f"{token}"})
    match response.json()['status']:
        case "Job is ready":
            return True
        case "Job is NOT ready":
            return False
        case _:
            print(f"Received status differs from expected ones: {response.json()['status']}")


def wait_for_sec(sec):
    time.sleep(sec)


def get_result(token):
    response = requests.get(url, params={"token": f"{token}"})
    try:
        return response.json()['result']
    except KeyError:
        print("There is not the result key.")


task = create_task()
assert not is_ready(task["token"])
wait_for_sec(task["seconds"])
print(get_result(task["token"]))
