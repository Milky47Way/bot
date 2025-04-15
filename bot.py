from email.headerregistry import MessageIDHeader
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from gpt import *
from util import *

tok = '7624424149:AAHyEg7oSY9JAKYzv-2N0aBCUhLLYuQo7Oo'

#menu
async def start(update, context):
    msg = load_message("main")
    await send_photo(update, context, name= "main")
    await send_text(update, context, msg)
    await show_main_menu(update, context, {
        "start": "Головне меню",
        "profile": "Генерація профіля 🪪",
        "opener": "Повідолення для знайомства \u2764", #emodji
        "message": "Переписка від вашого імені \U0001F339",
        "date": "Спілкування з зірками \u2B50",
        "gpt": "Задати питання ChatGPT"
    })
#reaction gpt
async def gpt(update, context):
    dialog.mode = 'gpt'
    await send_photo(update, context, name= '-2147483648_-212159')
    msg = load_message('gpt')
    await send_text(update, context, msg)


async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt('gpt')
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)


async def date(update, context):
    dialog.mode = 'date'
    msg = load_message('date')
    await send_photo(update, context, name= '-2147483648_-212176')
    await send_text_buttons(update, context, msg, buttons={
        'date_grande': 'Аріана Гранде',
        'date_robbie': 'Марго Роббі',
        'date_zendaya': 'Зендея',
        'date_gosling': 'Райан Гослінг',
        'date_hardy': 'Том Харді',

    })


async def date_button(update, context):
    query = update.callback_query.data
    print(query)
    await update.callback_query.answer()
    await send_photo(update, context, query)
    await send_text(update, context, 'Чудовий вибір! Ваша задача запросити дівчину/хлопця на побачення за 5 повідомлень.')
    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)

async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, text="Пише повідомлення..")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


#message
async def message(update, context):
    dialog.mode = 'message'
    msg = load_message('message')
    await send_photo(update, context, "cd96dfe72365c3be8eedd110542ca6f5")
    await send_text_buttons(update, context, msg, {
        "message_next": "Написати повідомлення",
        'message_date': 'Запросити на побачення'
    })

    dialog.list.clear()
async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)

async def message_button(update, context):
    query = update.callback_query.data
    await  update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = '\n\n'.join(dialog.list)

    my_message  = await send_text(update, context,  'Думаю над варіантами..')
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)

#gpt
async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    elif dialog.mode == 'date':
        await date_dialog(update, context)
    elif dialog.mode == 'message':
        await message_dialog(update, context)

dialog = Dialog()
dialog.mode = None
dialog.list = []
chatgpt = ChatGptService(token="gpt:AU54YW8RRi4TXANWp060hfjiJxU6btLIvPmqxAgYF0QLgPDwmNfdLT5NyC9Y8r_u4QZeQmwhzFJFkblB3T4yhgCdA9W2KZIQwDchnwN-SRJKHph3pqraKQNsAmcDeSXdm_4aNY-8_3oiLFalGXckzNJlfA-T")



app = ApplicationBuilder().token(tok).build()
app.add_handler(CommandHandler(command="start", callback=start))
app.add_handler(CommandHandler(command="gpt", callback=gpt))
app.add_handler(CommandHandler(command="date", callback=date))
app.add_handler(CommandHandler(command="message", callback=message))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, pattern= '^date_.*'))
app.add_handler(CallbackQueryHandler(message_button, pattern= '^message_.*'))
app.run_polling()
