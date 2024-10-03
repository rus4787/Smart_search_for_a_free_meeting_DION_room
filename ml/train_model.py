# ml/train_model.py

'''
Файл данных: room_usage_data.csv — это CSV-файл, в котором хранится информация о загруженности комнат.

Модель с использованием CatBoost. Это позволит улучшить предсказания благодаря использованию бустинга 
на деревьях решений, который хорошо справляется с временными рядами и категориальными признаками.
Параметры CatBoostRegressor:
    - iterations: 500 — количество итераций (можно настроить для ускорения обучения или повышения точности).
    - learning_rate: 0.1 — темп обучения (баланс скорости обучения и качества).
    - depth: 6 — глубина деревьев (параметр, влияющий на сложность модели).
    - cat_features: указание категориальных признаков (room_id).
    - verbose: 100 — вывод промежуточных результатов каждые 100 итераций.

Сохранение модели: Модель сохраняется в файл room_usage_model_catboost.pkl, который позже будет использоваться для предсказаний.
'''


import pandas as pd
from catboost import CatBoostRegressor, Pool
import pickle
import os

# Файл с данными (в будущем заменим на реальные данные)
DATA_FILE = 'room_usage_data.csv'

# Функция для обучения модели
def train_model():
    if not os.path.exists(DATA_FILE):
        print("Data file not found.")
        return

    # Загружаем данные
    df = pd.read_csv(DATA_FILE)

    # Преобразование временных данных
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60

    # Преобразование категориальных данных (room_id)
    df['room_id'] = df['room_id'].astype('category')

    # Подготовка данных для модели
    X = df[['room_id']]
    y = df['duration']

    # Определение категориальных признаков
    cat_features = ['room_id']

    # Создание CatBoostRegressor модели
    model = CatBoostRegressor(iterations=500,
                              learning_rate=0.1,
                              depth=6,
                              cat_features=cat_features,
                              verbose=100)

    # Обучение модели
    model.fit(X, y)

    # Сохранение модели
    with open('room_usage_model_catboost.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    print("CatBoost model trained and saved successfully.")

if __name__ == "__main__":
    train_model()
