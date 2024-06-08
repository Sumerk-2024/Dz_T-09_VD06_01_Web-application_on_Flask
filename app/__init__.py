from flask import Flask  # Импортируем класс Flask

app = Flask(__name__)  # Создаем экземпляр Flask
app.config['SECRET_KEY'] = 'your_secret_key'  # Настраиваем секретный ключ для защиты данных

from app import routes  # Импортируем маршруты из пакета app
