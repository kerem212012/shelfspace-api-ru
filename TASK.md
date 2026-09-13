# Задание

- Создай таблицу `Book` и отдельные схемы создания, обновления и ответа.
- Настрой SQLite, создание таблиц в lifespan и сессию через dependency с `yield`.
- Реализуй CRUD, фильтр `finished`, поиск и пагинацию.
- Используй `model_validate`, `model_dump(exclude_unset=True)` и `sqlmodel_update`.
- Не возвращай ORM-поля, которых нет в публичной схеме.
- Проверь перезапуск сервера и `uv run pytest`.
