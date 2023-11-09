
import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types

# TODO: 
TOKEN = '6829267222:AAHO-kCpCl8Hmc7yvl2Bdh3qyvZPr5a7o0o'
bot = TeleBot(TOKEN, parse_mode='html')

faker = Faker('ru_RU') 


main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

main_menu_reply_markup.row(
    types.KeyboardButton(text=" ⟦1⟧ "), types.KeyboardButton(text="⟦2⟧")
)

main_menu_reply_markup.row(
    types.KeyboardButton(text="⟦5⟧"), types.KeyboardButton(text="⟦1⟧⟦0⟧"), types.KeyboardButton(text="для настроения")
)

 '/start'
@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
   
    sti = open('welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(
        chat_id=message.chat.id,
        text="🐈 \nЭто бот для генерации тестовых пользователей. "\
        "Выбери сколько пользователей тебе нужно 👇🏻",
        reply_markup=main_menu_reply_markup)



@bot.message_handler()
def message_handler(message: types.Message):
  
    payload_len = 0
    if message.text == "⟦1⟧":
        payload_len = 1
    elif message.text == "⟦2⟧":
        payload_len = 2
    elif message.text == "⟦5⟧":
        payload_len = 5
    elif message.text == "⟦1⟧⟦0⟧":
        payload_len = 10
    elif message.text == 'для настроения':
            bot.send_message(message.chat.id, 'https://i.gifer.com/7kFr.gif')
    else:
        bot.send_message(chat_id=message.chat.id, text="Выбери одно из предлагаемых чисел! 😿")
        return

    
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

   
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )

  
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Если нужны еще данные, можешь выбрать еще раз 👇🏻",
        reply_markup=main_menu_reply_markup
    )
    


def main():
  
    bot.infinity_polling()


if __name__ == '__main__':
    main()
