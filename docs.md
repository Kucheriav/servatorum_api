# Документация API

## Пользователи (Users)

Базовый префикс: `/users`

### `POST /users/create_user`

* **Описание:** Создает нового пользователя в системе.
* **Тело запроса:** Объект JSON, соответствующий схеме `UserCreate`.
    * `login` (string, required): Логин пользователя.
    * `email` (string, format: email, required): Email пользователя (должен быть уникальным).
    * `first_name` (string, optional): Имя.
    * `surname` (string, optional): Отчество.
    * `last_name` (string, optional): Фамилия.
    * `date_of_birth` (string, format: date, optional): Дата рождения.
    * `gender` (string, optional): Пол.
    * `city` (string, optional): Город.
    * `phone` (string, required): Телефон в формате "7XXXXXXXXXX".
    * `password` (string, required): Пароль (минимум 8 символов).
* **Успешный ответ (`201 Created`):** Объект JSON, соответствующий схеме `UserResponse` (созданный пользователь, включая `user_id`, но без прямого доступа к хешу пароля).
* **Ошибки:**
    * `422 Unprocessable Entity`: Ошибка валидации данных (неверный формат email, телефона, короткий пароль и т.д.).
    * `400 Bad Request`: Email уже существует.
    * `500 Internal Server Error`: Внутренняя ошибка сервера.

### `GET /users/get_user/{user_id}`

* **Описание:** Получает информацию о пользователе по его ID.
* **Параметры пути:**
    * `user_id` (integer, required): Уникальный идентификатор пользователя.
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `UserResponse` (данные пользователя).
* **Ошибки:**
    * `404 Not Found`: Пользователь с указанным `user_id` не найден.

### `PATCH /users/patch_user/{user_id}`

* **Описание:** Обновляет указанные поля пользователя по его ID.
* **Параметры пути:**
    * `user_id` (integer, required): Уникальный идентификатор пользователя для обновления.
* **Тело запроса:** Объект JSON, соответствующий схеме `UserPatch`.
    * `params` (object, required): Словарь, где ключи - это имена полей для обновления (например, `email`, `phone`, `city`), а значения - новые значения. Применяются правила валидации из `UserCreate` для соответствующих полей (`phone`, `password`).
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `UserResponse` (обновленные данные пользователя).
* **Ошибки:**
    * `404 Not Found`: Пользователь с указанным `user_id` не найден.
    * `422 Unprocessable Entity`: Ошибка валидации данных в поле `params`.
    * `500 Internal Server Error`: Внутренняя ошибка сервера (например, при попытке обновить поле, которого не существует).

### `DELETE /users/delete_user/{user_id}`

* **Описание:** Удаляет пользователя по его ID.
* **Параметры пути:**
    * `user_id` (integer, required): Уникальный идентификатор пользователя для удаления.
* **Успешный ответ (`200 OK`):** Объект JSON `{"message": "User deleted"}`.
* **Ошибки:**
    * `404 Not Found`: Пользователь с указанным `user_id` не найден.

---

## Юридические лица (Legal Entities)

Базовый префикс: `/legal_entity`

### `POST /legal_entity/create_legal_entity`

* **Описание:** Создает новое юридическое лицо.
* **Тело запроса:** Объект JSON, соответствующий схеме `LegalEntityCreate`.
    * `name` (string, required): Название.
    * `description` (string, required): Описание.
    * `logo` (string, required): Ссылка на логотип (или путь).
    * `photo` (string, required): Ссылка на фото (или путь).
    * `inn` (string, required): ИНН (10 цифр, должен быть уникальным).
    * `bik` (string, required): БИК (9 цифр).
    * `cor_account` (string, required): Корр. счет (20 цифр).
    * `address` (string, required): Фактический адрес.
    * `address_reg` (string, required): Юридический адрес.
    * `phone` (string, required): Телефон в формате "7XXXXXXXXXX".
    * `phone_helpdesk` (string, required): Телефон поддержки в формате "7XXXXXXXXXX".
    * `entity_type` (string, required): Тип ('company' или 'foundation').
* **Успешный ответ (`201 Created`):** Объект JSON, соответствующий схеме `LegalEntityResponse` (созданное юр. лицо, включая `legal_entity_id`).
* **Ошибки:**
    * `422 Unprocessable Entity`: Ошибка валидации данных (неверный формат ИНН, БИК, корр. счета, телефона, типа).
    * `400 Bad Request`: ИНН уже существует.
    * `500 Internal Server Error`: Внутренняя ошибка сервера.

### `GET /legal_entity/get_legal_entity/{legal_entity_id}`

* **Описание:** Получает информацию о юридическом лице по его ID.
* **Параметры пути:**
    * `legal_entity_id` (integer, required): Уникальный идентификатор юр. лица.
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `LegalEntityResponse`.
* **Ошибки:**
    * `404 Not Found`: Юр. лицо с указанным `legal_entity_id` не найдено.

### `PATCH /legal_entity/patch_legal_entity/{legal_entity_id}`

* **Описание:** Обновляет указанные поля юридического лица по его ID.
* **Параметры пути:**
    * `legal_entity_id` (integer, required): Уникальный идентификатор юр. лица для обновления.
* **Тело запроса:** Объект JSON, соответствующий схеме `LegalEntityPatch`.
    * `params` (object, required): Словарь с полями для обновления (ключ-значение). Применяются правила валидации из `LegalEntityCreate` для соответствующих полей.
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `LegalEntityResponse` (обновленные данные юр. лица).
* **Ошибки:**
    * `404 Not Found`: Юр. лицо с указанным `legal_entity_id` не найдено.
    * `422 Unprocessable Entity`: Ошибка валидации данных в поле `params`.
    * `500 Internal Server Error`: Внутренняя ошибка сервера.

### `DELETE /legal_entity/delete_legal_entity/{legal_entity_id}`

* **Описание:** Удаляет юридическое лицо по его ID.
* **Параметры пути:**
    * `legal_entity_id` (integer, required): Уникальный идентификатор юр. лица для удаления.
* **Успешный ответ (`200 OK`):** Объект JSON `{"message": "Legal entity deleted"}`.
* **Ошибки:**
    * `404 Not Found`: Юр. лицо с указанным `legal_entity_id` не найдено.

---

## Сборы средств (Fundraising)

Базовый префикс: `/fundraising`

### `POST /fundraising/create_fundraising`

* **Описание:** Создает новый сбор средств.
* **Тело запроса:** Объект JSON, соответствующий схеме `FundraisingCreate`.
    * `title` (string, required): Название сбора.
    * `description` (string, required): Описание сбора.
    * `goal_amount` (float, required): Целевая сумма.
    * `raised_amount` (float, required): Собранная сумма (вероятно, должно быть 0 при создании).
    * `start_date` (string, format: date, required): Дата начала (не раньше текущей даты).
    * `finish_date` (string, format: date, required): Дата окончания (не раньше текущей даты и позже даты начала).
* **Успешный ответ (`201 Created`):** Объект JSON, соответствующий схеме `FundraisingResponce` (созданный сбор, включая `fundraising_id`).
* **Ошибки:**
    * `422 Unprocessable Entity`: Ошибка валидации данных (некорректные даты).
    * `400 Bad Request`: Возможны ошибки уникальности (не указано в коде, но потенциально).
    * `500 Internal Server Error`: Внутренняя ошибка сервера.

### `GET /fundraising/get_fundraising/{fundraising_id}`

* **Описание:** Получает информацию о сборе средств по его ID.
* **Параметры пути:**
    * `fundraising_id` (integer, required): Уникальный идентификатор сбора.
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `FundraisingResponce`.
* **Ошибки:**
    * `404 Not Found`: Сбор с указанным `fundraising_id` не найден.

### `GET /fundraising/get_fundraisings_pages`

* **Описание:** Получает список сборов средств с пагинацией.
* **Параметры запроса (Query Parameters):**
    * `page` (integer, optional, default: 1): Номер страницы.
    * `page_size` (integer, optional, default: 10): Количество элементов на странице.
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `FundraisingPaginationResponse`.
    * `page` (integer): Текущая страница.
    * `page_size` (integer): Размер страницы.
    * `total_items` (integer): Общее количество сборов.
    * `total_pages` (integer): Общее количество страниц.
    * `has_next` (boolean): Есть ли следующая страница.
    * `has_previous` (boolean): Есть ли предыдущая страница.
    * `items` (array): Массив объектов `FundraisingResponce`.
* **Ошибки:**
    * `404 Not Found`: Если сборы не найдены (например, при запросе несуществующей страницы или если их нет вообще).

### `PATCH /fundraising/patch_fundraising/{fundraising_id}`

* **Описание:** Обновляет указанные поля сбора средств по его ID.
* **Параметры пути:**
    * `fundraising_id` (integer, required): Уникальный идентификатор сбора для обновления.
* **Тело запроса:** Объект JSON, соответствующий схеме `FundraisingPatch`.
    * `params` (object, required): Словарь с полями для обновления (ключ-значение). Применяются правила валидации из `FundraisingCreate` для соответствующих полей (даты).
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `FundraisingResponce` (обновленные данные сбора).
* **Ошибки:**
    * `404 Not Found`: Сбор с указанным `fundraising_id` не найден.
    * `422 Unprocessable Entity`: Ошибка валидации данных в поле `params`.
    * `500 Internal Server Error`: Внутренняя ошибка сервера.

### `DELETE /fundraising/delete_fundraising/{fundraising_id}`

* **Описание:** Удаляет сбор средств по его ID.
* **Параметры пути:**
    * `fundraising_id` (integer, required): Уникальный идентификатор сбора для удаления.
* **Успешный ответ (`200 OK`):** Объект JSON `{"message": "Fundraising deleted"}`.
* **Ошибки:**
    * `404 Not Found`: Сбор с указанным `fundraising_id` не найден.

---

## Новости (News)

Базовый префикс: `/news`

### `POST /news/create_news`

* **Описание:** Создает новую новость.
* **Тело запроса:** Объект JSON, соответствующий схеме `NewsCreate`.
    * `title` (string, required, length 1-255): Заголовок новости.
    * `description` (string, required, length 1-1000): Текст новости.
    * `publication_date` (string, format: datetime, required): Дата и время публикации.
    * `photo` (string, optional): Ссылка на фото (или путь).
* **Успешный ответ (`201 Created`):** Объект JSON, соответствующий схеме `NewsResponse` (созданная новость, включая `news_id`).
* **Ошибки:**
    * `422 Unprocessable Entity`: Ошибка валидации данных (неверная длина полей).
    * `400 Bad Request`: Ошибка уникальности (не ясно, по какому полю).
    * `500 Internal Server Error`: Внутренняя ошибка сервера.

### `GET /news/get_news/{news_id}`

* **Описание:** Получает информацию о новости по её ID.
* **Параметры пути:**
    * `news_id` (integer, required): Уникальный идентификатор новости.
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `NewsResponse`.
* **Ошибки:**
    * `404 Not Found`: Новость с указанным `news_id` не найдена.

### `GET /news/get_news_pages`

* **Описание:** Получает список новостей с пагинацией.
* **Параметры запроса (Query Parameters):**
    * `page` (integer, optional, default: 1): Номер страницы.
    * `page_size` (integer, optional, default: 10): Количество элементов на странице.
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `NewsPaginationResponse`.
    * `page` (integer): Текущая страница.
    * `page_size` (integer): Размер страницы.
    * `total_items` (integer): Общее количество новостей.
    * `total_pages` (integer): Общее количество страниц.
    * `has_next` (boolean): Есть ли следующая страница.
    * `has_previous` (boolean): Есть ли предыдущая страница.
    * `items` (array): Массив объектов `NewsResponse`.
* **Ошибки:**
    * `404 Not Found`: Если новости не найдены.

### `PATCH /news/patch_news/{news_id}`

* **Описание:** Обновляет указанные поля новости по её ID.
* **Параметры пути:**
    * `news_id` (integer, required): Уникальный идентификатор новости для обновления.
* **Тело запроса:** Объект JSON, соответствующий схеме `NewsPatch`.
    * `params` (object, required): Словарь с полями для обновления (ключ-значение). Применяются правила валидации из `NewsCreate` для соответствующих полей (длина `title`, `description`).
* **Успешный ответ (`200 OK`):** Объект JSON, соответствующий схеме `NewsResponse` (обновленные данные новости).
* **Ошибки:**
    * `404 Not Found`: Новость с указанным `news_id` не найдена.
    * `422 Unprocessable Entity`: Ошибка валидации данных в поле `params`.
    * `500 Internal Server Error`: Внутренняя ошибка сервера.

### `DELETE /news/delete_news/{news_id}`

* **Описание:** Удаляет новость по её ID.
* **Параметры пути:**
    * `news_id` (integer, required): Уникальный идентификатор новости для удаления.
* **Успешный ответ (`200 OK`):** Объект JSON `{"message": "Новость удалена"}`.
* **Ошибки:**
    * `404 Not Found`: Новость с указанным `news_id` не найдена.