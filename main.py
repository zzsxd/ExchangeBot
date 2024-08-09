import telebot
import os
import platform
from threading import Lock
from config_parser import ConfigParser
from frontend import Bot_inline_btns
from backend import TempUserData, DbAct
from db import DB

config_name = 'secrets.json'


def main():
    @bot.message_handler(commands=['start', 'admin'])
    def start(message):
        command = message.text.replace('/', '')
        user_id = message.from_user.id
        buttons = Bot_inline_btns()
        db_actions.add_user(user_id, message.from_user.first_name, message.from_user.last_name,
                            f'@{message.from_user.username}')
        if command == 'start':
            temp_user_data.temp_data(user_id)[user_id][5] = message.from_user.username
            bot.send_message(user_id,
                             '<b>Привет! 👋</b>\n\n'
                             '🤖Я бот для <u>приобритения Юаней 💴, а так же пополнения Alipay! ✅</u>\n\n'
                             f'<b>Актуальный курс на покупку: {config.get_config()["coursesell"]} рублей</b>\n\n',
                             parse_mode='HTML',
                             reply_markup=buttons.start_btns())
        elif db_actions.user_is_admin(user_id):
            if command == 'admin':
                bot.send_message(user_id, '✅Вы успешно зашли в админ-панель ✅', reply_markup=buttons.admin_btns())

    @bot.message_handler(content_types=['text'])
    def text_msg(message):
        user_id = message.chat.id
        user_input = message.text
        buttons = Bot_inline_btns()
        code = temp_user_data.temp_data(user_id)[user_id][0]
        if db_actions.user_is_existed(user_id):
            if code == 0:
                try:
                    cost = float(message.text) * float(config.get_config()["coursesell"])
                    temp_user_data.temp_data(user_id)[user_id][3] = cost
                    bot.send_message(user_id, f'Сумма к оплате: {cost} рублей',
                                     reply_markup=buttons.go_chat_with_admin_buy())
                except ValueError:
                    bot.send_message(user_id, '❌Неправильный ввод! ❌')
            elif code == 1:
                try:
                    cost = float(message.text) * float(config.get_config()["coursebuy"])
                    temp_user_data.temp_data(user_id)[user_id][3] = cost
                    bot.send_message(user_id, f'Сумма к получению: {cost} рублей',
                                     reply_markup=buttons.go_chat_with_admin_sell())
                except ValueError:
                    bot.send_message(user_id, '❌ Неправильный ввод! ❌')
            elif code == 2:
                try:
                    course = float(message.text)
                    config.change_course_buy(course)
                    bot.send_message(user_id, '✅ Новый курс установлен ✅')
                    all_users = db_actions.get_user_id()
                    for user in all_users:
                        try:
                            bot.send_message(user[0], '💸 Установлен новый курс на продажу! 💸\n\n'
                                                      f'Актуальный курс: {config.get_config()["coursebuy"]}')
                        except:
                            bot.send_message(message.chat.id, 'Ошибка!')
                except ValueError:
                    bot.send_message(user_id, '❌ Неправильный ввод! ❌')
            elif code == 3:
                try:
                    course = float(message.text)
                    config.change_course_sell(course)
                    bot.send_message(user_id, '✅ Новый курс установлен ✅')
                    all_users = db_actions.get_user_id()
                    for user in all_users:
                        try:
                            bot.send_message(user[0], '💸 Установлен новый курс на покупку! 💸\n\n'
                                                      f'Актуальный курс: {config.get_config()["coursesell"]}')
                        except:
                            bot.send_message(message.chat.id, 'Ошибка!')
                except ValueError:
                    bot.send_message(user_id, '❌ Неправильный ввод! ❌')
            elif code == 4:
                if user_input is not None:
                    all_users = db_actions.get_user_id()
                    for user in all_users:
                        try:
                            bot.send_message(user[0], user_input)
                        except:
                            bot.send_message(message.chat.id, 'Ошибка рассылки!')
        else:
            bot.send_message(user_id, 'Введите /start для запуска бота')

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        user_id = call.message.chat.id
        if call.data == 'buy':
            bot.send_message(user_id, 'Какую сумму в Юанях Вы хотите пополнить?')
            temp_user_data.temp_data(user_id)[user_id][0] = 0
        elif call.data == 'sell':
            bot.send_message(user_id, 'Какую сумму в Юанях Вы хотите продать?')
            temp_user_data.temp_data(user_id)[user_id][0] = 1
        elif call.data == 'givecoursesell':
            bot.send_message(user_id, 'Введите новый курс на продажу.\n\n'
                                      f'Актуальный курс {config.get_config()["coursebuy"]}')
            temp_user_data.temp_data(user_id)[user_id][0] = 2
        elif call.data == 'givecoursebuy':
            bot.send_message(user_id, 'Введите новый курс на покупку.\n\n'
                                      f'Актуальный курс {config.get_config()["coursesell"]}')
            temp_user_data.temp_data(user_id)[user_id][0] = 3
        elif call.data == 'chatadminbuy':
            for admin in config.get_config()["admins"]:
                bot.send_message(admin, 'Покупка юаней/Пополнение Alipay\n\n'
                                             f'Сумма: {temp_user_data.temp_data(user_id)[user_id][3]} рублей\n\n'
                                             f'Пользователь: @{temp_user_data.temp_data(user_id)[user_id][5]}')
            bot.send_message(user_id, 'Перейти в чат с администратором - @obmen_CNY_RUS')
        elif call.data == 'chatadminsell':
            for admin in config.get_config()["admins"]:
                bot.send_message(admin, 'Покупка юаней/Пополнение Alipay\n\n'
                                             f'Сумма: {temp_user_data.temp_data(user_id)[user_id][3]} рублей\n\n'
                                             f'Пользователь: @{temp_user_data.temp_data(user_id)[user_id][5]}')
            bot.send_message(user_id, 'Перейти в чат с администратором - @obmen_CNY_RUS')
        elif call.data == 'export':
            db_actions.db_export_xlsx()
            bot.send_document(call.message.chat.id, open(config.get_config()['xlsx_path'], 'rb'))
            os.remove(config.get_config()['xlsx_path'])
        elif call.data == 'newsletter':
            bot.send_message(user_id, 'Введите текст для рассылки')
            temp_user_data.temp_data(user_id)[user_id][0] = 4

    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    temp_user_data = TempUserData()
    db = DB(config.get_config()['db_file_name'], Lock())
    db_actions = DbAct(db, config, config.get_config()['xlsx_path'])
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()
