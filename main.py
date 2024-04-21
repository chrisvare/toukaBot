# main.py
from discord.ext import commands
import os

from bot.cogs import setup_cogs

def main():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix='~', intents=intents)

    setup_cogs(bot)

    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    main()
