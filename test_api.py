import requests

BASE_URL = "http://127.0.0.1:8000/api"

print("1. Тест регистрации...")
response = requests.post(f"{BASE_URL}/users/register/", json={
    "email": "testuser@test.com",
    "password": "test123",
    "password_confirm": "test123",
    "first_name": "Test",
    "last_name": "User",
    "role": 3
})
print(f"Статус: {response.status_code}")
if response.status_code == 201:
    token = response.json()['token']
    print(f"✓ Регистрация успешна, токен получен")
else:
    print(f"✗ Ошибка: {response.json()}")

print("\n2. Тест входа...")
response = requests.post(f"{BASE_URL}/users/login/", json={
    "email": "user@example.com",
    "password": "user123"
})
print(f"Статус: {response.status_code}")
if response.status_code == 200:
    token = response.json()['token']
    print(f"✓ Вход успешен, токен получен")
else:
    print(f"✗ Ошибка: {response.json()}")
    exit()

headers = {"Authorization": f"Bearer {token}"}

print("\n3. Тест получения профиля...")
response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
print(f"Статус: {response.status_code}")
if response.status_code == 200:
    print(f"✓ Профиль получен: {response.json()['email']}")
else:
    print(f"✗ Ошибка: {response.json()}")

print("\n4. Тест доступа без токена (должна быть 401)...")
response = requests.get(f"{BASE_URL}/users/profile/")
print(f"Статус: {response.status_code}")
if response.status_code == 401:
    print("✓ Правильно возвращается 401")
else:
    print(f"✗ Ожидалась 401, получен {response.status_code}")

print("\n5. Тест получения товаров...")
response = requests.get(f"{BASE_URL}/core/products/", headers=headers)
print(f"Статус: {response.status_code}")
if response.status_code in [200, 403]:
    print(f"✓ Запрос обработан (статус: {response.status_code})")
else:
    print(f"✗ Неожиданный статус: {response.status_code}")

print("\n6. Тест админ API (должна быть 403 для обычного пользователя)...")
response = requests.get(f"{BASE_URL}/access/roles/", headers=headers)
print(f"Статус: {response.status_code}")
if response.status_code == 403:
    print("✓ Правильно возвращается 403 для не-админа")
else:
    print(f"✗ Ожидалась 403, получен {response.status_code}")

print("\n✓ Все основные проверки завершены!")