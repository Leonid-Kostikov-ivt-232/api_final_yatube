Yatube API
Описание
Yatube API - это REST API для социальной сети, где пользователи могут публиковать посты, вступать в сообщества, комментировать публикации и подписываться друг на друга.
API реализован на Django REST Framework с поддержкой JWT-аутентификации.
Документация доступна по адресу: http://127.0.0.1:8000/redoc/

Возможности
1. CRUD для публикаций (постов)

2. CRUD для комментариев к постам

3. Просмотр списка сообществ и информации о них

4. Подписка на других пользователей и просмотр своих подписок

5. JWT-аутентификация (выдача, обновление, проверка токенов)

Установка и запуск
1. Клонируйте репозиторий
bash
git clone <адрес_вашего_репозитория>
cd api_final_yatube
2. Создайте и активируйте виртуальное окружение
bash
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate
3. Установите зависимости
bash
pip install -r requirements.txt
4. Выполните миграции
bash
python manage.py migrate
5. (Опционально) Создайте суперпользователя
bash
python manage.py createsuperuser
6. Запустите сервер
bash
python manage.py runserver
Примеры запросов к API
Получить JWT-токен
text
POST /api/v1/jwt/create/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
Ответ:

json
{
  "refresh": "string",
  "access": "string"
}
Публикации
Получить список публикаций
text
GET /api/v1/posts/
Ответ:
Массив объектов публикаций (без пагинации) или объект с пагинацией при использовании параметров limit и offset.

Создать публикацию
text
POST /api/v1/posts/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "text": "Текст публикации",
  "group": 1
}

Комментарии
Получить комментарии к публикации
text
GET /api/v1/posts/{post_id}/comments/
Добавить комментарий
text
POST /api/v1/posts/{post_id}/comments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "text": "Текст комментария"
}

Сообщества
Получить список сообществ
text
GET /api/v1/groups/
Получить информацию о сообществе
text
GET /api/v1/groups/{id}/
Подписки
Получить свои подписки
text
GET /api/v1/follow/
Authorization: Bearer <access_token>
Подписаться на пользователя
text
POST /api/v1/follow/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "following": "username"
}
Аутентификация
Для большинства методов записи (POST, PUT, PATCH, DELETE) требуется JWT-аутентификация.

Получить токен можно по /api/v1/jwt/create/.

Для передачи токена используйте заголовок:
Authorization: Bearer <access_token>

Документация
Подробная документация по всем эндпоинтам доступна по адресу:
http://127.0.0.1:8000/redoc/

Примечания
Неавторизованный пользователь может только просматривать публикации, комментарии и сообщества.

Создавать, изменять и удалять свой контент может только авторизованный пользователь.

Подписки доступны только авторизованным пользователям.

Добавление новых пользователей через API не предусмотрено.