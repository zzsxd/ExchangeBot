import telebot
from telebot import types


class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=1)

    def start_btns(self):
        one = types.InlineKeyboardButton('💸 Покупка юаней/Пополнить Alipay 💸', callback_data='buy')
        two = types.InlineKeyboardButton('💰 Продать Юани 💰', callback_data='sell')
        self.__markup.add(one)
        return self.__markup

    def admin_btns(self):
        one = types.InlineKeyboardButton('Задать курс на продажу', callback_data='givecoursesell')
        two = types.InlineKeyboardButton('Задать курс на покупку', callback_data='givecoursebuy')
        self.__markup.add(one, two)
        return self.__markup

    def go_chat_with_admin_buy(self):
        one = types.InlineKeyboardButton('👤 Перейти к сделке 👤', callback_data='chatadminbuy')
        self.__markup.add(one)
        return self.__markup

    def go_chat_with_admin_sell(self):
        one = types.InlineKeyboardButton('👤 Перейти к сделке 👤', callback_data='chatadminsell')
        self.__markup.add(one)
        return self.__markup
