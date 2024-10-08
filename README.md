# Smart Search for Free Meeting Rooms - DION Rooms Enhancement

## Описание проекта
"Умный поиск свободной переговорной" - это проект, направленный на оптимизацию использования переговорных комнат, оборудованных DION Rooms. Цель проекта заключается в разработке механизма для автоматического сбора данных о загруженности переговорных, обучения модели для предсказания их доступности, а также создания интерфейса для предложения свободных переговорных комнат пользователям.

## Структура проекта
Проект включает в себя три основных компонента:
1. **Сбор данных о загруженности переговорных комнат**.
2. **Обучение модели машинного обучения для предсказания загруженности**.
3. **Интерфейс для поиска и бронирования переговорных комнат пользователем**.

```
project-folder/
│
├── server/
│   ├── room_data_collection.py  # Сбор данных о загруженности переговорных комнат.
│   ├── room_prediction.py       # Предсказание свободных переговорных комнат с использованием обученной модели.
│   ├── requirements.txt         # Зависимости для работы серверных частей и машинного обучения.
│   ├── Dockerfile               # Docker конфигурация для сервера.
│
├── ml/
│   ├── train_model.py           # Код для обучения модели машинного обучения с использованием CatBoost.
│   ├── room_usage_data.csv      # Данные для обучения модели (фиктивные данные).
│
├── client/
│   ├── search_room.html         # Основная HTML страница для поиска переговорных комнат.
│   ├── room-search.js           # JavaScript для взаимодействия с сервером и отображения результатов поиска.
│   ├── style.css                # Стили для веб-страницы.
│   ├── Dockerfile               # Docker конфигурация для клиентской части.
│
├── docker-compose.yml           # Docker Compose файл для сборки и развертывания всех компонентов проекта.
└── README.md                    # Документация проекта.
```

## Установка и запуск

### Требования
- **Docker** и **Docker Compose** для развертывания и управления контейнерами.
- **Python 3.10** или выше (если запускать код локально).

### Установка и запуск
Для запуска проекта выполните следующие шаги:

1. **Сборка контейнеров**:
   ```sh
   docker compose build
   ```
2. **Запуск контейнеров**:
   ```sh
   docker compose up
   ```
3. **Доступ к проекту**:
   - **Сервер сбора данных и предсказаний**: `http://localhost:5002` и `http://localhost:5003`.
   - **Клиентская часть (интерфейс поиска комнат)**: `http://localhost:8081`.

## Подробное описание файлов проекта

### 1. Серверная часть: Сбор данных о загруженности переговорных комнат (`server/room_data_collection.py`)

**Файл `room_data_collection.py`** представляет собой API на основе Flask, который отвечает за сбор данных о переговорах. 

- **Основные функции**:
  - **`/collect_data`** (`POST`): Позволяет отправить данные о начале и окончании использования комнаты, таких как `room_id`, `start_time`, `end_time`. Эти данные используются для обучения модели.
  - **`/get_room_data`** (`GET`): Возвращает все собранные данные, что может быть полезно для мониторинга и отладки.
  
- **Особенности**:
  - **Временная база данных**: Данные хранятся в памяти в виде списка, что подходит для демонстрационных целей, но в реальной среде данные должны храниться в устойчивом хранилище (например, в базе данных).

### 2. Серверная часть: Предсказание свободных переговорных комнат (`server/room_prediction.py`)

**Файл `room_prediction.py`** отвечает за предсказание свободных переговорных комнат с использованием модели машинного обучения **CatBoost**.

- **Основные функции**:
  - **`/search_room`** (`POST`): Принимает запрос от пользователя с указанием времени (`time`) и использует обученную модель для предсказания свободных комнат.
  
- **Особенности**:
  - Модель **CatBoost** загружается из файла `room_usage_model_catboost.pkl`. Она была обучена предсказывать, будет ли комната занята в указанный промежуток времени.
  - Примерный ответ сервера включает список переговорных комнат и прогнозируемую длительность их занятости. Это дает возможность пользователю видеть доступные переговорные комнаты в реальном времени.

### 3. Машинное обучение: Обучение модели (`ml/train_model.py`)

**Файл `train_model.py`** отвечает за обучение модели с использованием данных о загруженности переговорных комнат.

- **Использование CatBoost**:
  - **CatBoostRegressor** - это мощный алгоритм бустинга на деревьях решений, который подходит для работы с временными данными и категориальными признаками.
  - Данные о `room_id`, `start_time`, `end_time` преобразуются для обучения модели, где целевая переменная — `duration` (продолжительность использования комнаты).

- **Сохранение модели**:
  - Модель сохраняется в файл `room_usage_model_catboost.pkl` для последующего использования сервером предсказаний.

- **Особенности**:
  - **CatBoost** автоматизирует обработку категориальных признаков, что уменьшает объем предварительной подготовки данных и повышает качество предсказания.
  - Модель обучается на данных, сохраненных в `room_usage_data.csv`. В реальной среде данные поступали бы автоматически через API для сбора данных.

### 4. Веб-интерфейс для пользователя (`client/search_room.html`, `client/room-search.js`, `client/style.css`)

- **`search_room.html`**:
  - Основная HTML страница, предоставляющая форму для поиска переговорных комнат.
  - Пользователь может указать предпочтительное время, и форма отправит запрос на сервер для получения информации о свободных комнатах.

- **`room-search.js`**:
  - JavaScript для отправки POST-запроса на сервер предсказаний (`/search_room`) с указанным временем.
  - Обработка ответа сервера и отображение информации о доступных комнатах пользователю.

- **`style.css`**:
  - Стили для веб-страницы, чтобы сделать интерфейс более удобным и привлекательным для пользователя.

### 5. Docker и Docker Compose файлы

- **`server/Dockerfile`** и **`client/Dockerfile`**:
  - Описывают процесс создания Docker-образов для серверной и клиентской частей соответственно.
  - Включают инструкции по установке всех зависимостей и запуску приложений.

- **`docker-compose.yml`**:
  - Управляет запуском всех контейнеров (сервера для сбора данных, сервера предсказаний и клиентской части) как одной системы.
  - Определяет порты, которые будут использоваться для доступа к различным сервисам.

## Особенности проекта

- **Интеграция машинного обучения**: Проект использует алгоритм **CatBoost** для предсказания загруженности переговорных комнат, что делает его достаточно мощным для реальных сценариев использования.
- **Гибкость интерфейса**: Пользователь может ввести желаемое время и получить список доступных переговорных комнат, что позволяет оптимизировать использование ресурсов.
- **Сбор данных в реальном времени**: Сбор данных о переговорах осуществляется в режиме реального времени, и эти данные могут быть использованы для периодического обучения модели, что улучшает точность предсказаний.

## Планы на будущее
- **Интеграция с системами календарей**: Добавить интеграцию с корпоративными календарями, чтобы автоматически собирать данные о запланированных встречах и использовать их для предсказаний.
- **Улучшение модели**: В будущем можно использовать дополнительные данные (например, количество участников или тип оборудования) для повышения точности предсказаний.
- **Интерфейс бронирования**: Добавить функционал для бронирования комнат напрямую через веб-интерфейс после получения рекомендаций.

## Заключение
Проект "Умный поиск свободной переговорной" — это мощный инструмент для оптимизации использования переговорных комнат с помощью машинного обучения и анализа данных. Использование **CatBoost** и гибкий интерфейс делают проект конкурентоспособным решением, которое легко интегрируется в экосистему DION Rooms для улучшения пользовательского опыта и эффективного управления ресурсами.

``` 
