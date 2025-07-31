import requests
# получить пользователя, использовать его старые токены, попробовать патч и удаление

BASE_URL = "https://217.171.146.249:8000"
phone = "71231231212"
ROUTER_BRANCH = '/users'
WORK_URL = BASE_URL + ROUTER_BRANCH
user_id = 1
refresh_token = '7aa95dd2-5263-46d0-a9c3-6f769554141a'
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NTM5MDk0NDR9.ljN50glvZPTAZaL8L_aDz1q-Txzh_RVxkb-EnjY6W98'


print("Шаг 1: Получение пользователя")
resp = requests.get(f"{WORK_URL}/get_user/{user_id}", verify=False)
print("Ответ:", resp.status_code, resp.json())
assert resp.ok, "Ошибка при запросе пользователя"


print("Шаг 2: PATCH пользователя")
patch_payload = {"params": {"city": "ФФФФ"}}
headers = {"Authorization": f"Bearer {access_token}"}
patch_resp = requests.patch(f"{WORK_URL}/patch_user/{user_id}", json=patch_payload, headers=headers, verify=False)
print("Ответ:", patch_resp.status_code, patch_resp.json())
if patch_resp.status_code == 401:
    print("Пробуем обновить токен")
    refresh_payload = {'refresh_token_in': refresh_token}
    refresh_resp = requests.post(f"{WORK_URL}/token/refresh", json=refresh_payload, verify=False)
    print("Ответ:", refresh_resp.status_code, refresh_resp.json())
    assert refresh_resp.ok, "Ошибка обновления токена"
    access_token = refresh_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    patch_resp = requests.patch(f"{WORK_URL}/patch_user/{user_id}", json=patch_payload, headers=headers, verify=False)
    print("Ответ:", patch_resp.status_code, patch_resp.json())
    assert patch_resp.ok, "Токен не получилось обновить"


print("Шаг 3: DELETE пользователя")
delete_resp = requests.delete(f"{WORK_URL}/delete_user/{user_id}", headers=headers, verify=False)
print("Ответ:", patch_resp.status_code, patch_resp.json())