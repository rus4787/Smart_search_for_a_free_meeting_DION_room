# server/room_data_collection.py

'''
Сбор данных о загруженности переговорных комнат
Для этого создана серверная часть с использованием Flask, которая получает данные о состоянии переговорных комнат. 

Данные включают в себя:
- Время начала и конца использования комнаты
- Количество участников
- Используемое оборудование
'''

'''
Создано два маршрута:
/collect_data: Принимает данные о загруженности комнат (например, room_id, start_time, end_time).
/get_room_data: Возвращает текущие собранные данные.
'''

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Временная база данных для хранения данных о переговорных комнатах
room_usage_data = []

@app.route('/collect_data', methods=['POST'])
def collect_data():
    data = request.json
    if not data or 'room_id' not in data or 'start_time' not in data or 'end_time' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    room_usage_data.append(data)
    return jsonify({'message': 'Data collected successfully'}), 200

@app.route('/get_room_data', methods=['GET'])
def get_room_data():
    return jsonify(room_usage_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
    

