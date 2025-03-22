import os
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
class TelegramClient:
    def __init__(self, agent):
        self.agent = agent
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.app = None
        self.setup()

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        if update.message.text.startswith("/chat"):
            first_name = update.message.chat.first_name
            await update.message.reply_text(
                f"Hi {first_name}, how can I assist you today?"
            )
            return
        else:
            uid = update.message.chat.id
            text = update.message.text
            response = self.agent.chat(text, uid)
            await update.message.reply_text(response)

    async def clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.message.chat.id
        if  self.agent.memory:
            self.agent.memory.clear(uid)

        await update.message.reply_text("AI agent memory has been cleared.")

    def setup(self):
        self.app = ApplicationBuilder().token(self.token).build()
        self.app.add_handler(CommandHandler("chat", self.chat))
        self.app.add_handler(CommandHandler("clear", self.clear))
        self.app.add_handler(MessageHandler(filters.TEXT, self.chat))

    def run(self):
        print(f"{self.agent.name} is running...")
        self.app.run_polling()
