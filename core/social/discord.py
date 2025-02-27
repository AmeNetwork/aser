from dotenv import load_dotenv
import os
import asyncio

load_dotenv()


from interactions import Client, Intents, listen, slash_command, SlashContext


class DiscordClient:
    def __init__(self, **properties):

        self.bot = Client(intents=Intents.DEFAULT)
        self.setup()

    def setup(self):

        @self.bot.listen()
        async def on_startup():
            print("Discord Bot is ready!")

        @slash_command(name="ask", description="ask ai agent")
        async def ask(ctx: SlashContext):
            await ctx.defer()
            # call ai agent
            await ctx.send("Hello World")

        self.bot.add_command(ask)

        @slash_command(name="clear", description="clear memory")
        async def clear(ctx: SlashContext):
            # need to defer it, otherwise, it fails
            await ctx.defer()
            # call ai agent
            await ctx.send("Hello World")

        self.bot.add_command(clear)

    def run(self):

        self.bot.start(os.getenv("DISCORD_BOT_TOKEN"))
