# Bima Calc API

MVP backend для страхового калькулятора.  
Реализован на **Django REST Framework** + **JWT аутентификация**.  
Позволяет пользователю:
- Авторизоваться по токену.
- Создавать расчёты (`quotes`) стоимости страховки (OSAGO/KASKO).
- Создавать заявки (`applications`) на основе расчётов.
- Смотреть только свои расчёты и заявки.
- Получать документацию API (Swagger/OpenAPI).

---

## 📦 Стек технологий
- Python 
- Django 
- Django REST Framework
- SimpleJWT (аутентификация)
- drf-spectacular (Swagger/OpenAPI)
- django-cors-headers
- SQLite для dev)

---
## 📑 Сводная таблица маршрутов

| Метод | Путь                         | Описание                                | Авторизация |
|-------|------------------------------|-----------------------------------------|-------------|
| POST  | `/api/v1/auth/token/`        | Получение access/refresh токенов (логин)| ❌          |
| POST  | `/api/v1/auth/token/refresh/`| Обновление access-токена                | ❌          |
| POST  | `/api/v1/quotes/`            | Создать расчёт (OSAGO/KASKO)            | ✅          |
| GET   | `/api/v1/quotes/`            | Список своих расчётов                   | ✅          |
| GET   | `/api/v1/quotes/{id}/`       | Детали конкретного расчёта              | ✅          |
| POST  | `/api/v1/applications/`      | Создать заявку                          | ✅          |
| GET   | `/api/v1/applications/`      | Список своих заявок                     | ✅          |
| GET   | `/api/v1/applications/{id}/` | Детали конкретной заявки                | ✅          |
| GET   | `/api/v1/docs/`              | Swagger UI                              | ❌          |
| GET   | `/api/v1/schema/`            | OpenAPI схема (JSON)                    | ❌          |


## ⚙️ Установка и запуск
python manage.py runserver

## перейди по пути 
http://127.0.0.1:8000/api/v1/docs/ - переход на swagger 


## 1) Логин и получение токена

POST /api/v1/auth/token/ -  получения токена 

Content-Type: application/json
Body:
{
  "username": "admin",
  "password": "yourpassword"
}

## Успех (200):

{ "refresh": "…", "access": "…" }


2) Обновление access-токена

POST /api/v1/auth/token/refresh/ - обновления токена 

Content-Type: application/json
Body:
{ "refresh": "<refresh_token>" }


Ответ (200):

{ "access": "…" }


В Swagger: открой /api/v1/docs/ → Authorize → вставь Bearer <access>

## Quotes (расчёты)
## Создать расчёт

POST /api/v1/quotes/ -  путь для создания расчета 

Authorization: Bearer <access>
Content-Type: application/json
Body:
{
  "tariff": "OSAGO",          // или "KASKO"
  "driver_age": 24,           // 18..100
  "driver_experience": 2,     // 0..80 и <= age-18
  "car_type": "suv"           // sedan|suv|truck|sport
}


Успех (201):

{
  "id": "67e00dc8-bd9b-42ee-a1c6-531e6fa0ee0e",
  "tariff": "OSAGO",
  "driver_age": 24,
  "driver_experience": 2,
  "car_type": "suv",
  "base_amount": 1000.0,
  "coef_age": 1.3,
  "coef_exp": 1.2,
  "coef_car": 1.15,
  "total_amount": 1794.0,
  "currency": "TJS",
  "ruleset_version": "v1",
  "valid_until": "2025-09-02T15:30:00Z",
  "status": "ACTIVE",
  "created_at": "2025-09-02T15:30:00Z"
}


## Ошибки (400):

{
  "error": {
    "code": 400,
    "message": "driver_experience: не может быть > age-18",
    "details": { "driver_experience": "не может быть > age-18" }
  }
}

## Получить список своих расчётов

GET /api/v1/quotes/
Authorization: Bearer <access>


Ответ (200): массив ваших объектов; только ваши, в порядке created_at desc.

## Получить расчёт по id

GET /api/v1/quotes/{id}/
Authorization: Bearer <access>


## Чужой или несуществующий id → 404/403.


## Создать заявку

POST /api/v1/applications/

Authorization: Bearer <access>
Content-Type: application/json


Тело:

{
  "full_name": "Ivan Ivanov",
  "phone": "+992900000000",
  "email": "ivan@example.com",
  "tariff": "OSAGO",
  "quote": "67e00dc8-bd9b-42ee-a1c6-531e6fa0ee0e"
}


Успех (201):

{
  "id": "a1f3…",
  "quote": "67e00dc8-bd9b-42ee-a1c6-531e6fa0ee0e",
  "full_name": "Ivan Ivanov",
  "phone": "+992900000000",
  "email": "ivan@example.com",
  "tariff": "OSAGO",
  "total_amount_snapshot": 1794.0,
  "status": "NEW",
  "created_at": "2025-09-02T15:35:00Z"
}


Ошибки (400):

{"quote": "чужой расчёт"} — если расчёт принадлежит другому пользователю.

{"quote": "недопустимый статус USED"} — если расчёт уже использован.



## Получить список своих заявок

GET /api/v1/applications/

Authorization: Bearer <access>


Ответ (200): массив ваших заявок.

## Получить заявку по id

GET /api/v1/applications/{id}/

Authorization: Bearer <access>


Своя → 200 OK.

Чужая или несуществующая → 404 Not Found.
