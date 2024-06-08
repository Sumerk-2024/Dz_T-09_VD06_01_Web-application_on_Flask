from flask import render_template, request, flash  # Импорт необходимых функций из Flask
from app import app  # Импорт экземпляра приложения из пакета app
import re  # Импорт модуля для работы с регулярными выражениями


MAX_AGE = 151  # Установка максимального допустимого возраста


# Функция для получения правильного суффикса для возраста
def get_age_suffix(age):
    if 11 <= age % 100 <= 14:
        return "лет"  # Возвращаем "лет" для чисел от 11 до 14 включительно
    elif age % 10 == 1:
        return "год"  # Возвращаем "год" для числа 1
    elif 2 <= age % 10 <= 4:
        return "года"  # Возвращаем "года" для чисел от 2 до 4 включительно
    else:
        return "лет"  # Возвращаем "лет" для остальных чисел


# Функция для формирования сообщения об ошибке для возраста
def get_age_flash_message():
    return f'Пожалуйста, укажите Ваш реальный возраст (до {MAX_AGE} {get_age_suffix(MAX_AGE)})'


# Функция для проверки корректности ввода (только буквы, пробелы и дефисы)
def is_valid_input(value):
    return re.match(r'^[а-яА-ЯёЁa-zA-Z\s\-]+$', value) is not None


@app.route('/', methods=['GET', 'POST'])  # Декоратор для обработки запросов на главную страницу
def index():
    if request.method == 'POST':  # Если метод запроса POST
        name = request.form.get('name')  # Получение значения поля "имя" из формы
        city = request.form.get('city')  # Получение значения поля "город" из формы
        hobby = request.form.get('hobby')  # Получение значения поля "хобби" из формы
        age_input = request.form.get('age')  # Получение значения поля "возраст" из формы

        errors = {'name': False, 'city': False, 'hobby': False, 'age': False}  # Словарь для хранения флагов ошибок

        # Проверка на заполнение всех полей формы
        if not name or not city or not hobby or not age_input:
            flash('Пожалуйста, заполните корректно все поля !', 'danger')  # Отправка сообщения об ошибке
            if not name:
                errors['name'] = True  # Установка флага ошибки для имени
            if not city:
                errors['city'] = True  # Установка флага ошибки для города
            if not hobby:
                errors['hobby'] = True  # Установка флага ошибки для хобби
            if not age_input:
                errors['age'] = True  # Установка флага ошибки для возраста
            return render_template('blog.html', name=name, city=city, hobby=hobby, age=age_input, errors=errors)  # Возвращение шаблона с текущими значениями полей и ошибками

        # Проверка корректности ввода для каждого поля
        if not is_valid_input(name):
            flash('Имя может содержать только буквы, пробелы и дефисы', 'danger')  # Отправка сообщения об ошибке
            errors['name'] = True  # Установка флага ошибки для имени
            name = ""  # Очистка поля имени

        if not is_valid_input(city):
            flash('Город может содержать только буквы, пробелы и дефисы', 'danger')  # Отправка сообщения об ошибке
            errors['city'] = True  # Установка флага ошибки для города
            city = ""  # Очистка поля города

        if not is_valid_input(hobby):
            flash('Хобби может содержать только буквы, пробелы и дефисы', 'danger')  # Отправка сообщения об ошибке
            errors['hobby'] = True  # Установка флага ошибки для хобби
            hobby = ""  # Очистка поля хобби

        # Проверка корректности введенного возраста
        if not age_input.isdigit() or int(age_input) > MAX_AGE:
            if not age_input.isdigit():
                flash('Пожалуйста, введите возраст числом', 'danger')  # Отправка сообщения об ошибке для нечислового возраста
            else:
                flash(get_age_flash_message(), 'danger')  # Отправка сообщения об ошибке для слишком большого возраста
            errors['age'] = True  # Установка флага ошибки для возраста
            age_input = ""  # Очистка поля возраста

        # Если есть ошибки, возвращаем шаблон с текущими значениями полей и ошибками
        if any(errors.values()):
            return render_template('blog.html', name=name, city=city, hobby=hobby, age=age_input, errors=errors)

        age = int(age_input)  # Преобразование возраста в целое число
        age_suffix = get_age_suffix(age)  # Получение правильного окончания для возраста
        flash(f'Имя: {name}, Город: {city}, Хобби: {hobby}, Возраст: {age} {age_suffix}', 'success')  # Отправка сообщения об успешной отправке формы

    return render_template('blog.html', name="", city="", hobby="", age="", errors={})  # Возвращение шаблона с пустыми значениями полей при GET-запросе
