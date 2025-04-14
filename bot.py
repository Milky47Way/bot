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

#gpt
async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)

dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token="gpt:AU54YW8RRi4TXANWp060hfjiJxU6btLIvPmqxAgYF0QLgPDwmNfdLT5NyC9Y8r_u4QZeQmwhzFJFkblB3T4yhgCdA9W2KZIQwDchnwN-SRJKHph3pqraKQNsAmcDeSXdm_4aNY-8_3oiLFalGXckzNJlfA-T")



app = ApplicationBuilder().token(tok).build()
app.add_handler(CommandHandler(command="start", callback=start))
app.add_handler(CommandHandler(command="gpt", callback=gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
#app.add_handler(CallbackQueryHandler(buttons_handler))
app.run_polling()
