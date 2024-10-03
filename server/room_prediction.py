# server/room_prediction.py

'''
Загрузка обученной модели CatBoost:
    - Модель CatBoost загружается из файла room_usage_model_catboost.pkl.
Предсказание для списка переговорных комнат:
    - Предполагаем, что у есть несколько переговорных комнат, идентификаторы которых известны (room_ids = [1, 2, 3, 4, 5]).
    - Пакетное предсказание используется для всех комнат одновременно, чтобы определить их прогнозируемую загруженность.
Определение свободных комнат:
    - Добавили простую логику, чтобы определить свободные комнаты: Если прогнозируемая загруженность комнаты 
    (например, продолжительность в минутах) меньше порогового значения (< 60 минут), то комната считается свободной и добавляется в список. 
    Этот подход можно улучшить в зависимости от реальных условий использования и порогов.
Возвращаем результат пользователю:
    - Если свободные комнаты найдены, возвращается список комнат с указанием их идентификаторов и прогнозируемой длительности использования.
    - Если свободных комнат нет, возвращается сообщение о том, что на выбранное время нет доступных комнат.
'''

from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Загрузка обученной модели CatBoost
with open('ml/room_usage_model_catboost.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/search_room', methods=['POST'])
def search_room():
    data = request.json
    if not data or 'time' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    time = data['time']

    # Создаем фиктивные данные для предсказания (например, для всех переговорных)
    # Предполагается, что у нас есть несколько комнат с разными room_id, например: [1, 2, 3, 4, 5]
    room_ids = [1, 2, 3, 4, 5]

    # Подготовка данных для предсказания
    input_data = pd.DataFrame({'room_id': room_ids})

    # Предсказание продолжительности загруженности для каждой комнаты
    predicted_durations = model.predict(input_data)

    # Создание списка свободных комнат на основе предсказания
    free_rooms = []
    for room_id, predicted_duration in zip(room_ids, predicted_durations):
        # Условие, чтобы определить свободную комнату (например, если прогнозируемая загрузка меньше определенного порога)
        if predicted_duration < 60:  # Простое условие: если комната будет занята менее 60 минут, считаем её свободной
            free_rooms.append({'room_id': room_id, 'predicted_duration': predicted_duration})

    if not free_rooms:
        return jsonify({'message': 'No available rooms at the selected time.'}), 200

    return jsonify({'rooms': free_rooms}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
