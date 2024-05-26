import telebot
from telebot import types
import sqlite3

API_TOKEN = '6982122619:AAHzs0IsEqrXScesZSli1OBwlybV3qec4iM'

bot = telebot.TeleBot(API_TOKEN)


def create_connection():
    return sqlite3.connect('schedule.db')


def get_schedule_by_ids(start_id, end_id):
    conn = create_connection()
    cursor = conn.cursor()

    query = '''
        SELECT day, time, subject, room, teacher FROM schedule 
        WHERE id BETWEEN ? AND ? 
        ORDER BY id
    '''

    cursor.execute(query, (start_id, end_id))
    schedule = cursor.fetchall()
    conn.close()
    return schedule


def format_schedule_by_ids(start_id, end_id):
    schedule = get_schedule_by_ids(start_id, end_id)
    if not schedule:
        return "Расписание не найдено."

    formatted = ""
    current_day = ""
    for day, time, subject, room, teacher in schedule:
        if day != current_day:
            if current_day:
                formatted += "\n"
            current_day = day
            formatted += f"{day.capitalize()}:\n"
        formatted += f"{time} - {subject} {room} - {teacher}\n"
    return formatted


def get_current_week_schedule():
    return format_schedule_by_ids(1, 15)


def get_next_week_schedule():
    return format_schedule_by_ids(16, 27)


def get_schedule_by_day(day):
    conn = create_connection()
    cursor = conn.cursor()

    query = '''
        SELECT time, subject, room, teacher FROM schedule 
        WHERE day = ? AND id BETWEEN 1 AND 15 
        ORDER BY id
    '''

    cursor.execute(query, (day,))
    schedule = cursor.fetchall()
    conn.close()
    return schedule


def format_schedule_by_day(day):
    schedule = get_schedule_by_day(day)
    if not schedule:
        return f"Расписание на {day.capitalize()} не найдено."

    formatted = f"{day.capitalize()}:\n"
    for time, subject, room, teacher in schedule:
        formatted += f"{time} - {subject} {room} - {teacher}\n"
    return formatted


# Keyboards
main_keyboard = (
    types.ReplyKeyboardMarkup(resize_keyboard=True)
    .add(types.KeyboardButton("Расписание на текущую неделю"))
    .add(types.KeyboardButton("Расписание на следующую неделю"))
    .add(types.KeyboardButton("Расписание по дням"))
)

days_keyboard = (
    types.ReplyKeyboardMarkup(resize_keyboard=True)
    .add(types.KeyboardButton("Понедельник"))
    .add(types.KeyboardButton("Вторник"))
    .add(types.KeyboardButton("Среда"))
    .add(types.KeyboardButton("Четверг"))
    .add(types.KeyboardButton("Пятница"))
    .add(types.KeyboardButton("Назад"))
)


# Bot Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Чем могу вам помочь? Используйте /help если у вас возникли вопросы?", reply_markup=main_keyboard)


@bot.message_handler(func=lambda message: message.text.lower() == "назад")
def handle_back(message):
    bot.send_message(message.chat.id, "Чем могу вам помочь? Используйте /help если у вас возникли вопросы?", reply_markup=main_keyboard)


@bot.message_handler(func=lambda message: message.text.lower() == "расписание на текущую неделю")
def handle_current_week_schedule(message):
    schedule = get_current_week_schedule()
    bot.send_message(message.chat.id, schedule)


@bot.message_handler(func=lambda message: message.text.lower() == "расписание на следующую неделю")
def handle_next_week_schedule(message):
    schedule = get_next_week_schedule()
    bot.send_message(message.chat.id, schedule)


@bot.message_handler(func=lambda message: message.text.lower() == "расписание по дням")
def handle_day_schedule(message):
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=days_keyboard)

@bot.message_handler(func=lambda message: message.text.lower() in ["понедельник", "вторник", "среда", "четверг", "пятница"])
def handle_specific_day_schedule(message):
    day = message.text.lower()
    schedule = format_schedule_by_day(day)
    bot.send_message(message.chat.id, schedule)


@bot.message_handler(commands=['help'])
def handle_help(message):
    help_message = """
Привет! Я бот для удобного просмотра расписания в институте.

/start - начать взаимодействие с ботом
/help - получить справку о боте и доступных командах
/kstu - получить ссылку на официальный сайт КНИТУ
/week - узнать какая сейчас неделя чётная или нечётная
/vk - получить ссылку на группу VK
/list - вывести список группы в документе
/dekanat - получить график работы деканата

    """

    bot.send_message(message.chat.id, help_message)

@bot.message_handler(commands=['vk'])
def handle_vk_group(message):
    bot.send_message(message.chat.id, "Группа КНИТУ в VK: https://vk.com/knitu")

@bot.message_handler(commands=['list'])
def send_file(message):
    # Путь к файлу
    file_path = "список группы 4311-22.docx"  # Замените на реальный путь к вашему файлу

    # Отправка файла
    with open(file_path, 'rb') as document:
        bot.send_document(message.chat.id, document)

@bot.message_handler(commands=['kstu'])
def kstu_handler(message):
    bot.send_message(message.chat.id, 'https://www.kstu.ru/')

@bot.message_handler(commands=['dekanat'])
def send_dean_office_schedule(message):
    # Путь к изображению
    image_path = "IMG-20240521-WA0000.jpg"

    # Отправка изображения
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['week'])
def kstu_handler(message):
    bot.send_message(message.chat.id, 'Сейчас чётная неделя')

@bot.message_handler(func=lambda message: message.text.lower() == "график деканата")
def send_dean_office_schedule(message):
    # Путь к изображению
    image_path = "IMG-20240521-WA0000.jpg"

    # Отправка изображения
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text.lower() == "справки")
def send_dean_office_schedule(message):
    # Путь к изображению
    image_path = "IMG_20240518_144635.jpg"

    # Отправка изображения
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text.lower() == "матпомощь")
def send_file(message):
    # Путь к файлу
    file_path = "Бланк_заявления_на_РЕКТОРСКУЮ_МП_ВО_1.docx"

    # Отправка файла
    with open(file_path, 'rb') as document:
        bot.send_document(message.chat.id, document)


@bot.message_handler(func=lambda message: message.text.lower() == "привет")
def greet_user(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Создание персонализированного сообщения
    greeting = f"Привет, {first_name} {last_name}! Как я могу помочь вам сегодня?"

    # Отправка персонализированного сообщения
    bot.reply_to(message, greeting)


@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id, "Извините, я вас не понял. Попробуйте снова.")

bot.infinity_polling()

