# Custom Auth & Access Control

Модульный backend-проект с собственной системой аутентификации и авторизации.

## Цель проекта

Реализация кастомной системы:
- аутентификации пользователей (login / logout / JWT)
- авторизации на основе ролей и правил доступа
- разграничения прав на бизнес-ресурсы

Проект спроектирован модульно и может быть использован как основа
для интеграции в другие backend-приложения.

## Технологии

- Python 3.11
- Django 4.2
- Django REST Framework 3.16.1
- bcrypt 4.1.2 (хеширование паролей)
- PyJWT 2.8.0 (JWT токены для аутентификации)

## Установка и настройка

### Требования

- Python 3.11 или выше
- pip

### Шаги установки

1. **Клонируйте репозиторий** (если используете git):
   ```bash
   git clone <repository-url>
   cd custom_auth_access_control
   ```

2. **Создайте виртуальное окружение**:
   ```bash
   python -m venv venv
   ```

3. **Активируйте виртуальное окружение**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Примените миграции**:
   ```bash
   python manage.py migrate
   ```

6. **Создайте тестовые данные**:
   ```bash
   python manage.py create_test_data
   ```

   Это создаст:
   - Роли: admin, manager, user, guest
   - Бизнес-элементы: users, products, orders, shops, access_rules
   - Правила доступа для каждой роли
   - Тестовых пользователей с разными ролями
   - Суперпользователя для админки: `admin@admin.com` / `admin`

7. **Создайте директорию для логов** (опционально):
   ```bash
   mkdir logs
   ```

8. **Запустите сервер разработки**:
   ```bash
   python manage.py runserver
   ```

   Сервер будет доступен по адресу: `http://127.0.0.1:8000/`

## Структура проекта

```
custom_auth_access_control/
├── access/              # Модуль управления доступом
│   ├── models.py       # Модели: Role, BusinessElement, AccessRule
│   ├── views.py        # API для управления ролями, элементами, правилами
│   ├── permissions.py  # Permission classes для проверки доступа
│   ├── utils.py        # Утилиты проверки прав доступа
│   └── urls.py         # URL маршруты для access API
├── users/              # Модуль пользователей
│   ├── models.py       # Модель User
│   ├── views.py        # API: регистрация, логин, профиль
│   ├── authentication.py  # JWT и Bcrypt authentication backends
│   ├── middleware.py   # Middleware для JWT аутентификации
│   ├── utils.py        # Утилиты для работы с JWT
│   └── urls.py         # URL маршруты для users API
├── core/               # Модуль бизнес-ресурсов (mock)
│   ├── models.py       # Модели: Product, Order, Shop
│   ├── views.py        # Mock views для демонстрации системы доступа
│   └── urls.py         # URL маршруты для core API
└── config/             # Конфигурация Django
    ├── settings.py     # Настройки проекта
    └── urls.py         # Главный URL конфиг
```

## API Документация

### Базовый URL

Все API endpoints доступны по адресу: `http://127.0.0.1:8000/api/`

### Аутентификация

API использует JWT токены для аутентификации. Токен передается в заголовке:
```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints: Пользователи (`/api/users/`)

### 1. Регистрация

**POST** `/api/users/register/`

Создает нового пользователя и возвращает JWT токен.

**Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "first_name": "Иван",
  "last_name": "Иванов",
  "middle_name": "Иванович",
  "role": 3
}
```

**Ответ (201 Created):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "middle_name": "Иванович",
    "is_active": true,
    "role": 3,
    "role_name": "user",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "Пользователь успешно зарегистрирован"
}
```

---

### 2. Вход в систему

**POST** `/api/users/login/`

Аутентифицирует пользователя и возвращает JWT токен.

**Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Ответ (200 OK):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "is_active": true,
    "role": 3,
    "role_name": "user"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "Успешный вход в систему"
}
```

**Ошибки:**
- `400 Bad Request` - неверный email или пароль
- `400 Bad Request` - аккаунт деактивирован

---

### 3. Получение профиля

**GET** `/api/users/profile/`

Возвращает данные текущего пользователя.

**Заголовки:**
```
Authorization: Bearer <token>
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Иван",
  "last_name": "Иванов",
  "middle_name": "Иванович",
  "is_active": true,
  "role": 3,
  "role_name": "user",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

---

### 4. Обновление профиля

**PUT/PATCH** `/api/users/profile/`

Обновляет данные текущего пользователя.

**Заголовки:**
```
Authorization: Bearer <token>
```

**Тело запроса (PUT - полное обновление):**
```json
{
  "email": "newemail@example.com",
  "first_name": "Петр",
  "last_name": "Петров",
  "middle_name": "Петрович",
  "role": 3
}
```

**Тело запроса (PATCH - частичное обновление):**
```json
{
  "first_name": "Петр"
}
```

**Ответ (200 OK):**
```json
{
  "user": {
    "id": 1,
    "email": "newemail@example.com",
    "first_name": "Петр",
    ...
  },
  "message": "Профиль успешно обновлен"
}
```

---

### 5. Выход из системы

**POST** `/api/users/logout/`

Выход из системы (для JWT токены stateless, клиент должен удалить токен).

**Заголовки:**
```
Authorization: Bearer <token>
```

**Ответ (200 OK):**
```json
{
  "message": "Успешный выход из системы"
}
```

---

### 6. Удаление аккаунта (мягкое)

**DELETE** `/api/users/profile/`

Деактивирует аккаунт пользователя (устанавливает `is_active=False`).

**Заголовки:**
```
Authorization: Bearer <token>
```

**Ответ (200 OK):**
```json
{
  "message": "Аккаунт успешно удален. Вы больше не можете войти в систему."
}
```

---

## Endpoints: Управление доступом (`/api/access/`)

**Требуется роль:** `admin`

Все endpoints требуют аутентификации и роль администратора.

### Роли (`/api/access/roles/`)

#### Список ролей
**GET** `/api/access/roles/`

#### Детали роли
**GET** `/api/access/roles/{id}/`

#### Создание роли
**POST** `/api/access/roles/`
```json
{
  "name": "new_role",
  "description": "Описание роли"
}
```

#### Обновление роли
**PUT/PATCH** `/api/access/roles/{id}/`

#### Удаление роли
**DELETE** `/api/access/roles/{id}/`

---

### Бизнес-элементы (`/api/access/elements/`)

#### Список элементов
**GET** `/api/access/elements/`

#### Детали элемента
**GET** `/api/access/elements/{id}/`

#### Создание элемента
**POST** `/api/access/elements/`
```json
{
  "name": "new_element",
  "description": "Описание элемента"
}
```

#### Обновление элемента
**PUT/PATCH** `/api/access/elements/{id}/`

#### Удаление элемента
**DELETE** `/api/access/elements/{id}/`

---

### Правила доступа (`/api/access/rules/`)

#### Список правил
**GET** `/api/access/rules/`

#### Детали правила
**GET** `/api/access/rules/{id}/`

#### Создание правила
**POST** `/api/access/rules/`
```json
{
  "role": 1,
  "element": 2,
  "read_permission": true,
  "read_all_permission": false,
  "create_permission": true,
  "update_permission": true,
  "update_all_permission": false,
  "delete_permission": false,
  "delete_all_permission": false
}
```

#### Обновление правила
**PUT/PATCH** `/api/access/rules/{id}/`

#### Удаление правила
**DELETE** `/api/access/rules/{id}/`

---

## Endpoints: Бизнес-ресурсы (`/api/core/`)

Mock endpoints для демонстрации системы доступа.

### Товары (`/api/core/products/`)

#### Список товаров
**GET** `/api/core/products/`

Возвращает список товаров с учетом прав доступа:
- Если `read_all_permission = True` → все товары
- Если `read_permission = True` → только свои товары (где `owner = user`)

#### Создание товара
**POST** `/api/core/products/`
```json
{
  "name": "Новый товар",
  "description": "Описание товара",
  "price": 1000.00
}
```

**Требуется:** `create_permission = True`

#### Детали товара
**GET** `/api/core/products/{id}/`

#### Обновление товара
**PUT/PATCH** `/api/core/products/{id}/`

**Требуется:**
- `update_all_permission = True` ИЛИ
- `update_permission = True` И товар принадлежит пользователю

#### Удаление товара
**DELETE** `/api/core/products/{id}/`

**Требуется:**
- `delete_all_permission = True` ИЛИ
- `delete_permission = True` И товар принадлежит пользователю

---

### Заказы (`/api/core/orders/`)

Аналогично товарам:
- **GET** `/api/core/orders/` - список
- **POST** `/api/core/orders/` - создание
- **GET** `/api/core/orders/{id}/` - детали
- **PUT/PATCH** `/api/core/orders/{id}/` - обновление
- **DELETE** `/api/core/orders/{id}/` - удаление

---

### Магазины (`/api/core/shops/`)

Аналогично товарам:
- **GET** `/api/core/shops/` - список
- **POST** `/api/core/shops/` - создание
- **GET** `/api/core/shops/{id}/` - детали
- **PUT/PATCH** `/api/core/shops/{id}/` - обновление
- **DELETE** `/api/core/shops/{id}/` - удаление

---

## Примеры использования

### Пример 1: Регистрация и получение токена

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "password_confirm": "test123",
    "first_name": "Тест",
    "last_name": "Тестов",
    "role": 3
  }'
```

**Python (requests):**
```python
import requests

url = "http://127.0.0.1:8000/api/users/register/"
data = {
    "email": "test@example.com",
    "password": "test123",
    "password_confirm": "test123",
    "first_name": "Тест",
    "last_name": "Тестов",
    "role": 3
}

response = requests.post(url, json=data)
result = response.json()
token = result['token']
print(f"Token: {token}")
```

---

### Пример 2: Вход в систему

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "user123"
  }'
```

**Python:**
```python
import requests

url = "http://127.0.0.1:8000/api/users/login/"
data = {
    "email": "user@example.com",
    "password": "user123"
}

response = requests.post(url, json=data)
result = response.json()
token = result['token']
```

---

### Пример 3: Получение профиля с токеном

**cURL:**
```bash
curl -X GET http://127.0.0.1:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Python:**
```python
import requests

url = "http://127.0.0.1:8000/api/users/profile/"
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)
profile = response.json()
print(profile)
```

---

### Пример 4: Создание товара (требуется доступ)

**cURL:**
```bash
curl -X POST http://127.0.0.1:8000/api/core/products/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новый товар",
    "description": "Описание",
    "price": 1000.00
  }'
```

**Python:**
```python
import requests

url = "http://127.0.0.1:8000/api/core/products/"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "name": "Новый товар",
    "description": "Описание",
    "price": 1000.00
}

response = requests.post(url, headers=headers, json=data)
product = response.json()
print(product)
```

---

### Пример 5: Полный цикл работы с API

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# 1. Регистрация
register_data = {
    "email": "newuser@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Новый",
    "last_name": "Пользователь",
    "role": 3
}
response = requests.post(f"{BASE_URL}/users/register/", json=register_data)
token = response.json()['token']

# 2. Получение профиля
headers = {"Authorization": f"Bearer {token}"}
profile = requests.get(f"{BASE_URL}/users/profile/", headers=headers).json()

# 3. Создание товара
product_data = {
    "name": "Мой товар",
    "description": "Описание товара",
    "price": 500.00
}
product = requests.post(
    f"{BASE_URL}/core/products/",
    headers=headers,
    json=product_data
).json()

# 4. Получение списка товаров
products = requests.get(
    f"{BASE_URL}/core/products/",
    headers=headers
).json()

print(f"Создан товар: {product['name']}")
print(f"Всего товаров: {len(products)}")
```

---

## Обработка ошибок

### HTTP Статусы

- `200 OK` - успешный запрос
- `201 Created` - успешное создание ресурса
- `400 Bad Request` - ошибка валидации
- `401 Unauthorized` - не аутентифицирован (нет токена или токен невалиден)
- `403 Forbidden` - нет доступа к ресурсу
- `404 Not Found` - ресурс не найден
- `500 Internal Server Error` - ошибка сервера

### Примеры ошибок

**401 Unauthorized:**
```json
{
  "detail": "Требуется аутентификация."
}
```

**403 Forbidden:**
```json
{
  "detail": "У вас нет прав на выполнение действия \"create\" с элементом \"products\"."
}
```

**400 Bad Request (валидация):**
```json
{
  "email": ["Пользователь с таким email уже существует."],
  "password_confirm": ["Пароли не совпадают."]
}
```

---

## Тестовые пользователи

После выполнения `python manage.py create_test_data` доступны:

| Email | Пароль | Роль | Описание |
|-------|--------|------|----------|
| `admin@admin.com` | `admin` | admin | Суперпользователь (для админки) |
| `admin@example.com` | `admin123` | admin | Администратор |
| `manager@example.com` | `manager123` | manager | Менеджер |
| `user@example.com` | `user123` | user | Обычный пользователь |
| `guest@example.com` | `guest123` | guest | Гость |

---

## Статус проекта

Проект полностью реализован и готов к использованию.

**Реализовано:**
- ✅ Регистрация, логин, логаут
- ✅ Обновление и удаление профиля
- ✅ JWT аутентификация
- ✅ Ролевая авторизация с правилами доступа
- ✅ Mock бизнес-ресурсы для демонстрации
- ✅ Административные API для управления правами
- ✅ Логирование всех операций
- ✅ Полная документация

---

## Лицензия

Проект создан в рамках тестового задания.

## 👤 Автор

**[Ndk985](https://github.com/Ndk985)**
