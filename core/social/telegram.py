from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
load_dotenv()
class TelegramClient:
    def __init__(self):

        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.app = None

    async def ask(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text.startswith('/'):
            return
        #call ai agent
        await update.message.reply_text("hello world")
        print(update)


    async def clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        #clear memory
        await update.message.reply_text("clear")

    def setup(self):
        self.app = ApplicationBuilder().token(self.token).build()
        self.app.add_handler(CommandHandler("ask", self.ask))
        self.app.add_handler(CommandHandler("clear", self.clear))
        self.app.add_handler(MessageHandler(filters.TEXT, self.ask))

    def run(self):
        self.app.run_polling()

