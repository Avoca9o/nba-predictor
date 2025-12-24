# NBA Predictor App

Этот проект — NBA Predictor App, реализованный с помощью FastAPI.

## Запуск приложения
Рекомендуется работать в виртуальном окружении (venv), чтобы изолировать зависимости проекта.  
Создайте виртуальное окружение командой:

```
python3 -m venv venv
```

Активируйте его:

```
source venv/bin/activate
```

Установите зависимости:

```
pip install -r requirements.txt
```

Далее в самом проекте необходим создать `.env` файл (можно скопировать данные в него из `.env_example` файла)

### Миграции базы данных

Проект использует Alembic для управления миграциями базы данных. Перед первым запуском необходимо применить миграции:

```bash
alembic upgrade head
```

Это создаст необходимые таблицы в базе данных `predictions.db`.

### Запуск сервера

```bash
uvicorn main:app --reload
```

Приложение будет доступно по адресу http://127.0.0.1:8000

## Postman

Можно потестировать запущенное приложение с помощью Postman: [NBA Predictor App Workspace](https://www.postman.com/avoca9o/nba-workspace)
> **Важно:** Для локального тестирования API через Postman необходимо установить [Postman Desktop Agent](https://www.postman.com/downloads/postman-agent/). Без него запросы к localhost могут не работать корректно!

## CURL

Как оказалось, у коллекции постамана могут быть проблемы с доступом, поэтому осталвяем гайд, как подянть, запустить и протестировать приложения у себя лкоально:

### Тестирование

- Получение предсказания:
```bash
curl 'http://127.0.0.1:8000/forward' \
-X POST \
-d '{
  "home_over_away_wins_diff_10": -3,
  "form_5_diff": -4,
  "form_15_diff": 1,
  "last_home_matches_count_diff": 2,
  "days_off_diff": -1,
  "is_last_season_champion_diff": 1
}'
```

Ожидаемый ответ:
`{"prediction":1}`

- Получение JWT-токена:

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

Ожидаемый ответ:
`{"access_token":"YOUR_TOKEN","token_type":"bearer"}`

- Получение истории:

```bash
curl -X GET "http://localhost:8000/history" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Ожидаемый ответ:

```json
{"predictions":["Prediction(id=1, input={'home_over_away_wins_diff_10': -3, 'form_5_diff': -4, 'form_15_diff': 1, 'last_home_matches_count_diff': 2, 'days_off_diff': -1, 'is_last_season_champion_diff': 1}, prediction=1, prediction_date=2025-12-19 00:33:03.179709)",...]}
```

- Удалить историю:


```bash
curl -X DELETE "http://localhost:8000/history" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Ожидаемый ответ:
`{"message":"Predictions deleted"}`

- Просмотр статистики по запросам

```bash
curl -X GET "http://localhost:8000/stats" \     
  -H "Authorization: Bearer YOUR_TOKEN"
```

Ожидаемый результат:

```json
{
    "mean": "0.005570s",
    "50 quantile": "0.005570s",
    "95 quantile": "0.005570s",
    "99 quantile": "0.005570s",
    "mena req length" :164.0
}
```
