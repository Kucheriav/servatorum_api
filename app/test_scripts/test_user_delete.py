import requests
#

BASE_URL = "https://217.171.146.249:8000"
phone = "71231231212"
ROUTER_BRANCH = '/users'
WORK_URL = BASE_URL + ROUTER_BRANCH
user_id = 1
print("Шаг 1: Получение пользователя")
resp = requests.get(f"{WORK_URL}/get_user/{user_id}", verify=False)
print("Ответ:", resp.status_code, resp.json())
assert resp.ok, "Ошибка при запросе пользователя"


print("Шаг 2: PATCH пользователя")
patch_payload = {"params": {"city": "КККККК"}}
refresh_token = ''
cookies = {"refresh_token": refresh_token}
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NTM5MDk0NDR9.ljN50glvZPTAZaL8L_aDz1q-Txzh_RVxkb-EnjY6W98'
headers = {"Authorization": f"Bearer {access_token}"}
patch_resp = requests.patch(f"{WORK_URL}/patch_user/{user_id}", json=patch_payload, headers=headers, cookies=cookies, verify=False)
print("Ответ:", patch_resp.status_code, patch_resp.json())
