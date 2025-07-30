import requests

BASE_URL = "https://217.171.146.249:8000"
phone = "71231231212"
ROUTER_BRANCH = '/users'
WORK_URL = BASE_URL + ROUTER_BRANCH
print("Шаг 1: Запрос кода подтверждения")
resp = requests.post(f"{WORK_URL}/request_code", json={"phone": phone}, verify=False)
print("Ответ:", resp.status_code, resp.json())
assert resp.ok, "Ошибка при запросе кода"


code = input("Введи код из телеграм-бота: ")


print("Шаг 2: Проверка кода")
verify_resp = requests.post(f"{WORK_URL}/verify_code", json={"phone": phone, "code": code}, verify=False)
print("Ответ:", verify_resp.status_code, verify_resp.json())
assert verify_resp.ok, "Ошибка при проверке кода"

data = verify_resp.json()
if data.get("is_new"):
    print("Шаг 3: Создание пользователя")
    user_info = {
        "login": "testuser",
        "email": "testuser@example.com",
        "first_name": "Ivan",
        "surname": "Ivanovich",
        "last_name": "Ivanov",
        "phone": phone,
        "role": "getting help"
    }
    create_resp = requests.post(f"{WORK_URL}/create_user", json=user_info, verify=False)
    print("Ответ:", create_resp.status_code, create_resp.json())
    assert create_resp.ok, "Ошибка при создании пользователя"
    user_id = create_resp.json()["id"]
    access_token = create_resp.json().get("access_token")
    refresh_token = create_resp.json().get("refresh_token")
else:
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    user_id = data["user"]["id"]
print("Полученный access_token:", access_token)
print("Полученный refresh_token:", refresh_token)
cookies = {"refresh_token": refresh_token}

# 5. Патчим пользователя (нужно предъявить токен)
print("Шаг 4: PATCH пользователя")
patch_payload = {
    "params": {"city": "Москва"}
}
headers = {"Authorization": f"Bearer {access_token}"}
patch_resp = requests.patch(f"{WORK_URL}/patch_user/{user_id}", json=patch_payload, headers=headers, cookies=cookies, verify=False)
print("Ответ:", patch_resp.status_code, patch_resp.json())