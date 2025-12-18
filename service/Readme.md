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

Запустите сервер:

```
uvicorn main:app --reload
```

Приложение будет доступно по адресу http://127.0.0.1:8000

## Postman

Можно потестировать запущенное приложение с помощью Postman: [NBA Predictor App Workspace](https://www.postman.com/avoca9o/nba-workspace)
> **Важно:** Для локального тестирования API через Postman необходимо установить [Postman Desktop Agent](https://www.postman.com/downloads/postman-agent/). Без него запросы к localhost могут не работать корректно!
