FROM python:3.8

WORKDIR /usr/app/

# Копируем файл requirements.txt в контейнер и установим python зависимости
# копируем папку src в контейнер
# Обучаем модель, сериализуем объекты запуском скрипта model_train.py

# ******** НИЖЕ НАПИШИТЕ КОД ВЫПОЛНЯЮЩИЙ 3 ДЕЙСТВИЯ ОПИСАННЫЕ ВЫШЕ
# Копируем файл requirements.txt в контейнер и установим python зависимости
COPY requirements.txt ./app_requirements/requirements.txt
RUN pip install --no-cache-dir -r ./app_requirements/requirements.txt

# Копирует папку src в контейнер
COPY src ./src

# Обучаем модель, сериализуем объекты запуском скрипта model_train.py
RUN python ./src/model_train.py

# Запускаем Flask приложение через uwsgi
CMD uwsgi --http 0.0.0.0:5000 --wsgi-file ./src/server.py --callable app --processes 2 --master

# 1. Move to app directory
# cd <project_directory>/app/

# 2. Build  Docker-container
# sudo docker build -t webinar_app_uwsgi -f uwsgi.Dockerfile .

# 3. Run the Docker-container
# sudo docker run -p 8000:8000 -it --rm --name webinar_app_uwsgi webinar_app_uwsgi