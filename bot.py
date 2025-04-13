from email.headerregistry import MessageIDHeader
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler
from gpt import *
from util import *

tok = '7624424149:AAHyEg7oSY9JAKYzv-2N0aBCUhLLYuQo7Oo'

async def start(update, context):
    #await send_photo(update, context, name= "avatar_main")
    #await send_text(update, context, text= 'Привіт, друже!')

    msg = load_message("main")
    await send_text(update, context, text= 'Привіт, як до тебе звертатися?') #+ update.message.text)


    #gpt
async def hello(update, context):
    #await send_text(update, context, text='Привіт, ' + update.message.text)
    await send_text_buttons(update, context,text='Привіт, ' + update.message.text + "."
                                                 +"\n\nЯ Аля. Буду рада з тобою співпрацювати. Бажаєш продовжити?", buttons= {
        "start": "START",
        "stop": "STOP"
    })

async def buttons_handler(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, text= "Started")
    elif query == "stop":
        await send_text(update, context, text="Stopped")


app = ApplicationBuilder().token(tok).build()
app.add_handler(CommandHandler(command="start", callback=start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(buttons_handler))
app.run_polling()
