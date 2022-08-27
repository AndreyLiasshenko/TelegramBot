import telebot
bot = telebot.TeleBot("5397350411:AAElGBRUyIGrBFZYIdNWPQxHmOowNuY_fyA")
admin = 1053183238
a = telebot.types.ReplyKeyboardRemove()
name = ""
city = ""
there = ""
there_city = ""
things = ""
phone = ""
email = ""
way_to_pay = telebot.types.ReplyKeyboardMarkup(True, True)
way_to_pay.row("Viber").row("У Telegram").row("на Email")
weight = ""
weight_btn = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["До 10 кг", "15кг", "20кг",  "25кг", "30кг", "Свою вагу"]
weight_btn.add(*buttons)
amount_parcel = ""
service = telebot.types.ReplyKeyboardMarkup(True, True)
service.row("Далі")



@bot.message_handler(commands=['start'])
def start(message):
        bot.send_message(message.from_user.id, "Вітаємо {0.first_name} \nМи — Transfer From Ukraine,"
                                               " доставляємо посилки українцям, які вимушено виїхали під час війни"
                                               " в країни Європи. Дайте нам всього 5-7 днів, і ми доставимо турботу"
                                               " та довгоочікуваний пакунок від ваших близьких з України в будь-яку "
                                               "точку Польщі, Чехії, Франції, Німеччини, Австрії та інших країн"
                                               " Європи.".format(message.from_user), reply_markup=service)
        bot.register_next_step_handler(message, next_step)

@bot.message_handler(content_types=['text'])
def next_step(message):
    if message.text == "Далі":
        bot.send_message(message.from_user.id, "Як Вас звати? Напишіть,"
                                               " будь ласка Ім'я та Прізвище.", reply_markup=a)
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Напишіть місто з якого буде відправлятись посилка')
    bot.register_next_step_handler(message, get_from)

def get_from(message):
    global city
    city = message.text
    bot.send_message(message.from_user.id, 'Напишіть країну в яку треба доставити посилку')
    bot.register_next_step_handler(message, get_there)


def get_there(message):
    global there
    there = message.text
    bot.send_message(message.from_user.id, 'Напишіть місто в яке треба доставити посилку')
    bot.register_next_step_handler(message, get_there_city)


def get_there_city(message):
    global there_city
    there_city = message.text
    bot.send_message(message.from_user.id, 'Напишіть речі які треба доставити')
    bot.register_next_step_handler(message, what_things)


def what_things(message):
    global things
    things = message.text
    bot.send_message(message.from_user.id, 'Оберіть вагу посилки:', reply_markup=weight_btn)
    bot.register_next_step_handler(message, get_weight)


def get_weight(message):
    global weight
    if message.text == "Свою вагу":
        bot.send_message(message.from_user.id, 'Напишіть вагу своєї посилки:', reply_markup=a)
        bot.register_next_step_handler(message, own_weight)
        return
    global weight
    weight = message.text
    bot.send_message(message.from_user.id, 'Оберіть кількість одиниць вантажу:')
    bot.register_next_step_handler(message, get_amount_parcel)


def own_weight(message):
    global weight
    weight = message.text
    bot.send_message(message.from_user.id, 'Оберіть кількість одиниць вантажу:')
    bot.register_next_step_handler(message, get_amount_parcel)


def get_amount_parcel(message):
    global amount_parcel
    amount_parcel = message.text
    bot.send_message(message.from_user.id, 'Бажаєте отримати розрахунок вартості перевезення посилки?'
                                           ' Оберіть зручний спосіб отримати інформацію.', reply_markup=way_to_pay)
    bot.register_next_step_handler(message, get_count)


def get_count(message):
    if message.text == "Viber" or message.text == "У Telegram":
        bot.send_message(message.from_user.id, 'Вкажіть ваш номер телефону', reply_markup=a)
        bot.register_next_step_handler(message, get_phone)

    elif message.text == "на Email":
        bot.send_message(message.from_user.id, 'Вкажіть ваш номер Email', reply_markup=a)
        bot.register_next_step_handler(message, get_email)


def get_phone(message):
    global phone
    if message.text[0] == '+':
        phone = message.text
        goodbye(message)
    else:
        bot.send_message(message.from_user.id, 'Ваш номер телефону має містити код країни'
                                               ' та міста та мати такий формат: +15417543010')
        bot.register_next_step_handler(message, get_phone)


def get_email(message):
    global email
    email = message.text
    goodbye(message)


def goodbye(message):
    bot.send_message(message.from_user.id, 'Дякуємо, {0.first_name} Ваше замовлення прийняте до обробки. '
                                           'Найближчим часом ми надішлемо вам відповідь.'.format(message.from_user))
    info_for_admin = "-----------------------" + \
          "\nІм'я: " + name + \
          "\nТелефон: " + phone + \
          "\nХоче відправити посилку від " + city + " до " + there + " (" + there_city + ")" + \
          "\nКількіть посилок: " + amount_parcel + \
          "\nРечі в посилці: " + things + \
          "\nВага посилки: " + weight + \
          "\nEmail: " + email + \
          "\n-----------------------"
    bot.send_message(admin, text=info_for_admin)


bot.polling(none_stop=True)
