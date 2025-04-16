from email.headerregistry import MessageIDHeader
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from gpt import *
from util import *

tok = '8192403172:AAHW6Lgo0F9Y9ni3JAgxoRp-YaLUT8NhONo'

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
        'happybirthday': "Привітання з днем народження",
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
    await send_photo(update, context, name= '875ea0cf864a8fd98c7b1f992fb72932')
    await send_text_buttons(update, context, msg, buttons={
        'date_grandee': 'Аріана Гранде',
        'date_robbie': 'Марго Роббі',
        'date_zendayaa': 'Зендея',
        'date_goslingg': 'Райан Гослінг',
        'date_hardyy': 'Том Харді',

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

async def profile(update, context):
    dialog.mode = 'profile'
    msg = load_message('profile')
    await send_photo(update, context, "975d9b2e9830bf363cfeecf565139740")
    await send_text(update, context, msg)
    dialog.user.clear()
    dialog.counter = 0

    await send_text(update, context, 'Як вас звати?')
    #await send_text(update, context, 'Скільки вам років?')

async def profile_dialog(update, context):
    text = update.message.text

    if dialog.counter == 0:
        dialog.user['name'] = text
        dialog.counter += 1
        await send_text(update, context, 'Скільки вам років?')
        return


    if dialog.counter == 1:
        dialog.user['age'] = text
        dialog.counter += 1
        await send_text(update, context, 'Ким ви працюєте?')
        return

    if dialog.counter == 2:
        dialog.user["occupation"] = text
        dialog.counter += 1
        await send_text(update, context, 'Яке у вас хобі?')
        return

    if dialog.counter == 3:
        dialog.user['hobby'] = text
        dialog.counter += 1
        await send_text(update, context, 'Що вас бісить у людях?')
        return

    if dialog.counter == 4:
        dialog.user['annoys'] = text
        dialog.counter += 1
        await send_text(update, context, 'Мета знайомства?')
        return

    if dialog.counter == 5:
        dialog.user['goals'] = text
        dialog.counter += 1


    prompt = load_prompt('profile')
    user_info = dialog_user_info_to_str(dialog.user)
    my_message = await send_text(update, context, text= 'ChatGPT генерує ваш профіль..')
    answer = await chatgpt.send_question(prompt, user_info)
    await my_message.edit_text(answer)



#opener
async def opener(update, context):
    text = update.message.text
    dialog.mode = 'opener'

    msg = load_message('opener')
    await send_photo(update, context, "d08dd6a58d3b1bde8a38eba1490f0b46")
    await send_text(update, context, msg)

    dialog.user.clear()
    dialog.counter = 0

    await send_text(update, context, "Ім'я вашого партнера:")

async def opener_dialog(update, context):
    text = update.message.text
    if dialog.counter == 0:
        dialog.user['name'] = text
        dialog.counter += 1
        await send_text(update, context, 'Скільки йому/їй років?')
        return

    if dialog.counter == 1:
        dialog.user['age'] = text
        dialog.counter += 1
        await send_text(update, context, 'Зовнішність від 1 до 10')
        return

    if dialog.counter == 2:
        dialog.user["handsome"] = text
        dialog.counter += 1
        await send_text(update, context, 'Ким працює?')
        return

    if dialog.counter == 3:
        dialog.user['occupation'] = text
        dialog.counter += 1
        await send_text(update, context, 'Мета знайомства?')
        return

    if dialog.counter == 4:
        dialog.user['goals'] = text
        dialog.counter += 1


        prompt = load_prompt('opener')
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, text='ChatGPT генерує ваше повідомлення..')
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)


#happy birthday
async def happybirthday(update, context):
    text = update.message.text
    if dialog.mode != 'happybirthday':
        dialog.mode = 'happybirthday'


        dialog.user.clear()
        dialog.counter = 1
        msg = load_message('happybirthday')
        await send_text(update, context, "Як звуть іменинника?")
        return

    if dialog.counter == 1:
        dialog.user['name'] = text
        dialog.counter += 1
        await send_text(update, context, 'Скільки йому/їй років?')
        return

    if dialog.counter == 2:
        dialog.user['age'] = text
        dialog.counter += 1
        await send_text(update, context, 'Хто ви йому/їй?')
        return

    if dialog.counter == 3:
        dialog.user['hb'] = text
        dialog.counter += 1



        prompt = load_prompt('happybirthday')
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, text='ChatGPT генерує привітання..')
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)
        return

#gpt
async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)
    elif dialog.mode == 'date':
        await date_dialog(update, context)
    elif dialog.mode == 'message':
        await message_dialog(update, context)
    elif dialog.mode == 'profile':
        await profile_dialog(update, context)
    elif dialog.mode == 'opener':
        await opener_dialog(update, context)
    elif dialog.mode == 'happybirthday':
        await happybirthday(update, context)

dialog = Dialog()
dialog.mode = None
dialog.list = []
dialog.user = {}
dialog.counter = 0
chatgpt = ChatGptService(token="gpt:AU54YW8RRi4TXANWp060hfjiJxU6btLIvPmqxAgYF0QLgPDwmNfdLT5NyC9Y8r_u4QZeQmwhzFJFkblB3T4yhgCdA9W2KZIQwDchnwN-SRJKHph3pqraKQNsAmcDeSXdm_4aNY-8_3oiLFalGXckzNJlfA-T")



app = ApplicationBuilder().token(tok).build()
app.add_handler(CommandHandler(command="start", callback=start))
app.add_handler(CommandHandler(command="gpt", callback=gpt))
app.add_handler(CommandHandler(command="date", callback=date))
app.add_handler(CommandHandler(command="message", callback=message))
app.add_handler(CommandHandler(command="profile", callback=profile))
app.add_handler(CommandHandler(command="opener", callback=opener))
app.add_handler(CommandHandler(command="happybirthday", callback=happybirthday))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, pattern= '^date_.*'))
app.add_handler(CallbackQueryHandler(message_button, pattern= '^message_.*'))
app.run_polling()
