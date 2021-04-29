FROM python:3.8

WORKDIR /usr/app/

# Копируем файл requirements.txt в контейнер и установим python зависимости
# Копируем папку src в контейнер
# Обучаем модель, сериализуем объекты запуском скрипта model_train.py
# Запускаем Flask приложение напрямую (запускаем скрипт server.py)


# ******** НИЖЕ НАПИШИТЕ КОД ВЫПОЛНЯЮЩИЙ 4 ДЕЙСТВИЯ ОПИСАННЫЕ ВЫШЕ
# копируем файл requirements.txt в контейнер и установим python зависимости
COPY requirements.txt ./app_requirements/requirements.txt
RUN pip install --no-cache-dir -r ./app_requirements/requirements.txt


# Копирует папку src в контейнер
COPY src ./src

# Обучаем модель, сериализуем объекты запуском скрипта model_train.py
RUN python ./src/model_train.py

# Запускаем Flask приложение запуском скрипта server.py
CMD python ./src/server.py