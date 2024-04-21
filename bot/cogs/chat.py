import discord
from discord.ext import commands
import openai
import aiosqlite


class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def touka(self, ctx, *, message: str):
        """Handles messages directed to Touka."""
        bot_response = await self.handle_conversation(ctx, message)
        await ctx.send(bot_response)

    async def handle_conversation(ctx, message):
        # Define the AI's persona with anime girl characteristics
        personality_intro = {
            "role": "assistant",
            "content": "Hi there! 😊 I'm always excited to chat about anything fun! What's on your mind today?"
        }

        past_messages = [personality_intro]

        async with aiosqlite.connect('conversation_data.db') as conn:
            async with conn.execute("SELECT user_input, bot_response FROM conversation") as cursor:
                async for row in cursor:
                    user_input, bot_response = row
                    if user_input is not None:
                        past_messages.append({"role": "user", "content": user_input})
                        past_messages.append({"role": "assistant", "content": bot_response})

        past_messages.append({"role": "user", "content": message})

        try:
            filtered_messages = [msg for msg in past_messages if msg["content"] is not None]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=filtered_messages
            )
            bot_response = response['choices'][0]['message']['content']
            await store_conversation(message, bot_response)
        except Exception as e:
            bot_response = f"An error occurred: {e}"

        return bot_response

    @commands.Cog.listener()
    async def on_message(self, message):
        """Listener that processes every message seen by the bot."""
        if message.author == self.bot.user:
            return

        # Prevent processing commands as normal messages
        if message.content.startswith(self.bot.command_prefix):
            return

        # Handle general chatting outside of commands
        bot_response = await self.handle_conversation(message.channel, message.content)
        await message.channel.send(bot_response)


def setup(bot):
    bot.add_cog(ChatCog(bot))
