import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ======= Configs =======
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')

intents = discord.Intents.default().all()
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

EXCLUDE_COGS = ['sample']

# ======= Events =======
@bot.event
async def on_ready():
    print(f'{bot.user.name} is running!')

@bot.event
async def on_member_join(member: discord.Member):
    print(f'{member} has joined the server')

@bot.event
async def on_member_remove(member: discord.Member):
    print(f'{member} has left the server')

@bot.event
async def on_message(message: discord.Message):
    # Make sure on_message event not intercept command handlers
    if message.content.startswith(COMMAND_PREFIX):
        await bot.process_commands(message)
        return

    # Handle on_message normally here
    pass

# @commands.has_permissions(administrator=True, manage_messages=True)
@bot.command()
@commands.has_role(ADMIN_ROLE)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    print(f'module {extension} loaded!')

@bot.command()
@commands.has_role(ADMIN_ROLE)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    print(f'module {extension} unloaded!')

# ======= Load cogs =======
for dir_name in os.listdir('./cogs'):
    
    path = os.path.join('./cogs', dir_name)
    if os.path.isdir(path) and '__init__.py' in os.listdir(path):
        if dir_name not in EXCLUDE_COGS:
            bot.load_extension(f'cogs.{dir_name}')

# ======= Run =======
bot.run(DISCORD_TOKEN)
