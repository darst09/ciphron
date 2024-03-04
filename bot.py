import telebot;
from telebot import types
from lib.keygen import Keygen
from lib.crypt import Crypt

bot = telebot.TeleBot('6663713919:AAGhtjtQBEmYXAUNqQuAt8yJxbM0PvrPwKM')
crypt = Crypt()

@bot.message_handler(content_types=['text'])
def start(message):
    keyboard = menu()    
    bot.send_message(message.from_user.id, 'Привет, я Шифробот!', reply_markup=keyboard)

#обработчики событий
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'keygen':
        keygen = Keygen()
        pk = keygen.getPublicKey()
        sk = keygen.getSecretKey()
        bot.send_message(call.message.chat.id, f'Публичный ключ\n{pk}')      
        bot.send_message(call.message.chat.id, f'Приватный ключ\n{sk}')
    elif call.data == 'encode':
        bot.send_message(call.message.chat.id, 'Введите публичный ключ')
        bot.register_next_step_handler(call.message, get_public_key)
    elif call.data == 'decode':
        bot.send_message(call.message.chat.id, 'Введите секретный ключ')
        bot.register_next_step_handler(call.message, get_secret_key)
    elif call.data == 'start':
        keyboard = menu()    
        bot.send_message(call.message.chat.id, 'Попробуй еще раз', reply_markup=keyboard)
        
#меню
def menu():
    #объявляем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    #определяем кнопки
    keyGen = types.InlineKeyboardButton(text='Сгенерировать ключи', callback_data='keygen')
    keyEncode = types.InlineKeyboardButton(text='Шифровать', callback_data='encode')
    keyDecode = types.InlineKeyboardButton(text='Расшифровать', callback_data='decode')    
    #добавляем кнопки в клавиатуру
    keyboard.add(keyGen)
    keyboard.add(keyEncode)
    keyboard.add(keyDecode)
    
    return keyboard  
      
#запросить публичный ключ      
def get_public_key(message):
    global pKey
    pKey = message.text
    if crypt.isKeyValid(pKey):
        bot.send_message(message.from_user.id, 'Введите сообщение')
        bot.register_next_step_handler(message, get_encoded)
    else:
        on_error(message, 'Некорректный публичный ключ')        

#зашифровать и вывести      
def get_encoded(message):
    msg = message.text
    encoded = crypt.encode(pKey, msg)
    bot.send_message(message.from_user.id, f'Зашифровал!')
    bot.send_message(message.from_user.id, f'{encoded}')
    
#запросить приватный ключ 
def get_secret_key(message):
    global sKey    
    sKey = message.text
    
    if crypt.isKeyValid(sKey):
        bot.send_message(message.from_user.id, 'Введите шифровку')
        bot.register_next_step_handler(message, get_decoded)
    else:
        on_error(message, 'Некорректный секретный ключ')
        
#расшифровать и вывести    
def get_decoded(message):
    msg = message.text
    decoded = crypt.decode(sKey, msg)
    bot.send_message(message.from_user.id, f'Расшифровал!')
    bot.send_message(message.from_user.id, f'{decoded}')

#в случае ошибки вернуться в меню      
def on_error(message, error):
    #объявляем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    #определяем кнопки
    keyBack = types.InlineKeyboardButton(text='Вернуться в меню', callback_data='start')    
    #добавляем кнопки в клавиатуру
    keyboard.add(keyBack)
    
    bot.send_message(message.from_user.id, text=error, reply_markup=keyboard)    

#прослушивание событий бота        
bot.polling(none_stop=True, interval=0)        