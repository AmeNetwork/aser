import os
from interactions import Client, Intents, listen, slash_command, SlashContext,SlashCommandOption,OptionType

class DiscordClient:
    def __init__(self, agent):

        self.bot = Client(intents=Intents.DEFAULT)
        self.agent = agent
        self.setup()

    def setup(self):

        @self.bot.listen()
        async def on_startup():
            print(f"{self.agent.name} is ready!")

        @slash_command(
            name="chat",
            description="Chat with AI agent",
            options=[
                SlashCommandOption(
                    name="message",
                    description="Your message to the AI",
                    type=OptionType.STRING,
                    required=True,
                )
            ],
        )
        async def chat(ctx: SlashContext, message: str):
            await ctx.defer()

            response = self.agent.chat(message, ctx.author.id)

            await ctx.send(f"{ctx.author.mention} {response}")

        self.bot.add_command(chat)

        @slash_command(name="clear", description="Clear the conversation memory")
        async def clear(ctx: SlashContext):

            await ctx.defer()

            if self.agent.memory:
                self.agent.memory.clear(ctx.author.id)

            await ctx.send(f"{ctx.author.mention} AI agent memory has been cleared.")

        self.bot.add_command(clear)

    def run(self):

        self.bot.start(os.getenv("DISCORD_BOT_TOKEN"))
