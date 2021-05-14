# Скрипт flask сервера для предикта
from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd


app = Flask(__name__)

MODEL_FILE = '_webinar_model.pkl'
FEATURE_ORDER_FILE = '_feature_order.pkl'
TEST_DATA_FILE = '_test_data.pkl'

# Загружаем сериализованные объекты
# Обученная модель
# Лист с порядком признаков
# Признаки для тестового датасета

# ******** НИЖЕ НАПИШИТЕ КОД ЗАГРУЗКИ ТРЕХ СЕРИАЛИЗОВАННЫХ ОБЪЕКТОВ
# model
with open(MODEL_FILE, 'rb') as pkl_file:
    model = pickle.load(pkl_file)

# featurer_order
with open(FEATURE_ORDER_FILE, 'rb') as pkl_file:
    feature_order = pickle.load(pkl_file)

# test_data
with open(TEST_DATA_FILE, 'rb') as pkl_file:
    test_data_df = pickle.load(pkl_file)



# Flask метод для проверки работы сервера, требования:
# Ендпойнт: "/hello"
# На вход: GET запрос со строковым параметром "param"
# На выходе: json с 2мя полями 'result'
#   'result': str, содержащий "SERVER OK"
#   'param': str, содержащий значение параметра "param" (переданного на вход)
#
# Для проверки корректности используем следующие запросы
# (можно через браузер, можно запустить проверочный скрипт "python test_hello.py"):
#
# url = http://localhost:8000/hello?param=
# response = {'param': '', 'result': 'SERVER OK'}
#
# url = http://localhost:8000/hello?param=42
# response = {'param': '42', 'result': 'SERVER OK'}
#
# url = http://localhost:8000/hello?param=python
# response = {'param': 'python', 'result': 'SERVER OK'}


# ******** НИЖЕ НАПИШИТЕ КОД FLASK МЕТОДА ДЛЯ ПРОВЕРКИ РАБОТЫ СЕРВЕРА
@app.route('/hello', methods=['GET'])
def hello_check():
    param = request.args.get('param')
    
    return jsonify({'param': param,
                    'result': 'SERVER OK'}), 200


# Flask Метод для предикта обученной моделью, требования:
# Ендпойнт: "/predict"
# На вход: GET запрос со строковым параметром "obj_id"
#   obj_id - айди объекта из тестовой выборки
# На выходе: json с 3мя полями
#   'prediction': float округленный до 4 знака "round(prediction, 4)", предсказание модели на объекте obj_id
#       или -1 если произошла любая ошибка
#   'obj_id': str, айди объекта поступившего на вход АПИ
#   'response_status': str, содержащий 'OK' если в ответе предсказание и 'ERROR' если произошла любая ошибка
#
# ОБРАТИТЕ ВНИМАНИЕ: в методе должна быть предусмотрена обработка ошибок,
# чтобы запросы с некорректными входными данными отрабатывали и возвращали HTTP статус код 200
# (например можно использовать try-except)
#
# Для проверки корректности используем следующие запросы
# (можно через браузер, можно запустить проверочный скрипт "python test_predict.py"):

# url = http://localhost:8000/predict?obj_id=8740
# response = {'obj_id': '8740', 'prediction': 2.478, 'response_status': 'OK'}
#
# url = http://localhost:8000/predict?obj_id=162
# response = {'obj_id': '162', 'prediction': 2.4255, 'response_status': 'OK'}
#
# url = http://localhost:8000/predict?obj_id=
# response = {'obj_id': '', 'prediction': -1.0, 'response_status': 'ERROR'}
#
# url = http://localhost:8000/predict?obj_id=python
# response = {'obj_id': 'python', 'prediction': -1.0, 'response_status': 'ERROR'}
#
# url = http://localhost:8000/predict?obj_id=-1
# response = {'obj_id': '-1', 'prediction': -1.0, 'response_status': 'ERROR'}
#
# url = http://localhost:8000/predict?obj_id=168
# response = {'obj_id': '168', 'prediction': -1.0, 'response_status': 'ERROR'}


# ******** НИЖЕ НАПИШИТЕ КОД FLASK МЕТОДА ДЛЯ ПРЕДИКТА ОБУЧЕННОЙ МОДЕЛЬЮ
@app.route('/predict', methods=['POST',])
def predict():
    numbers = request.json
    pred = model.predict(numbers)[0]
    return jsonify({'prediction': pred}), 200




    # obj_id = request.args.get('obj_id')
    # try:
    #     obj_id = int(obj_id)
    #     data = test_data_df[test_data_df['obj_id'] == obj_id].drop(labels='obj_id', axis=1).to_numpy().reshape((1, -1))
    #     print(f"DATA= {data}\n")
    #     pred = np.round(model.predict(data)[0], 4)
    #     print(f"PREDICTION= {pred}\n")

    #     return jsonify({'obj_id': str(obj_id),
    #                     'prediction': pred,
    #                     'response_status': 'OK'}), 200
    # except:
    #     return jsonify({'obj_id': str(obj_id),
    #                     'prediction': -1.0,
    #                     'response_status': 'ERROR'}), 200
     


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
