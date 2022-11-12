
# импортируем библиотеки
import logging 
# from controller import*
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler,Filters,MessageHandler, Updater
import random
# создаём кнопки для начала игры и выхода из бота
reply_keyboard = [['/play', '/info', '/close']]

# создаём кнопку стоп для выхода из игры
stop_keyboard = [['/stop']]

#  создаем переменную клавиатур
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
stop_markup = ReplyKeyboardMarkup(stop_keyboard, one_time_keyboard=False)

#вводим логер 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

TOKEN = '5648685451:AAHmXJ365bBNWrQWq0XdNqHHOQTw7O6K0UU'

# вводим переменную количество конфет(изначально =0), потом данные приходят из функции player_1
# пока количество конфет будет > 28 
candy = 0

# функция старта( начала запуска бота)
def start(update, context):
    update.message.reply_text(
        "Привет! Давай играть!",
        reply_markup=markup #показать клавиатуру
    )

# функция для начала игры ввод количества конфет и закрытие первой клавиатуры 
# и переходу к play_get_candy через return 1
def play(update, context):
    # ввод в консоль количество конфет , скрытие первой клавиатуры и вывод второй клавиатуры
    update.message.reply_text('Введите колличество конфет в игре', reply_markup=markup)
    
    return 1

# функция принимает введенное значени конфет , принимает сколько возьмет конфет игрок 
#  и переходит к def player_1 по return 2
def play_get_candy(update, context):
    global candy
    # Вывод ботом требования на экран (update.message.reply_text)
    update.message.reply_text('Сколько конфет Вы возьмете?', reply_markup=markup)
    # получение числа ботом  (update.message.text)
    candy = int(update.message.text)
    return 2


def player_1(update, context):
    global candy
    try:#проверка на ввод чисел, а не букв
        caunt = int(update.message.text)
        if  (caunt > 28 or caunt <=0):
            update.message.reply_text('Вы ввели неверное число. Введите число в диапазоне 1 до 28')
            return 2
        candy1 = candy - int(update.message.text) 
        update.message.reply_text(f'Конфет осталось: {candy1}', reply_markup=markup)
        # пока остаток конфет > 28 происходит вычитание количества(произвольного)
        #  конфет которые взял бот и передача остатка в начало программы     
        if candy1 > 28:            
            temp = random.randint(1,28)
            candy = candy1 - temp
            update.message.reply_text(f'Бот взял {temp} конфет. Конфет осталось: {candy}', reply_markup=stop_markup)
            # если конфет еще >28, то возврат к player_1 через return 2
            if candy > 28:
                update.message.reply_text('Сколько конфет вы возьмете?', reply_markup=stop_markup)

            #если <28 , то вывод вы победили со смайликом и гифкой с последующим закрытием бота 
            else:
                update.message.reply_text( f'Вы победили 👍', reply_markup=markup)
                context.bot.send_document(
                    chat_id=update.effective_chat.id, document='https://i.yapx.ru/Gz08d.gif')
                return ConversationHandler.END
            return 2

        # если < 28 конфет, то последний ход у бота и он победил и тоже закрытие бота через ConversationHandler
        else:
            update.message.reply_text('Победил бот 😝', reply_markup=markup)
            context.bot.send_document(
                chat_id=update.effective_chat.id, document='https://i.yapx.ru/Gz08n.gif')
            return ConversationHandler.END
    except ValueError:  # проверка на ввод чисел, а не букв
        update.message.reply_text('Введите число')
        return 2


def stop(update, context):
    update.message.reply_text("Всего доброго!", reply_markup=markup)
    return ConversationHandler.END


def info(update, context):
    update.message.reply_text(
        'Условие игры: На столе лежит 2021 конфета.\n'
        'Играют два игрока делая ход друг после друга.\n'
        'Первый ход определяется жеребьёвкой.\n'
        'За один ход можно забрать не более чем 28 конфет.\n'
        'Все конфеты оппонента достаются сделавшему последний ход.'
        )


def close(update, context):
    update.message.reply_text(
        "Спасибо за игру!",
        reply_markup=ReplyKeyboardRemove())

# запуск бота
play_handler = ConversationHandler(entry_points=[CommandHandler('play', play)],

    # Состояние внутри диалога.
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, play_get_candy)],
        2: [MessageHandler(Filters.text & ~Filters.command, player_1)],
    },

    # Точка прерывания диалога. В данном случае — команда /stop.
    fallbacks=[CommandHandler('stop', stop)]
    )


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(play_handler)
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", close))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
