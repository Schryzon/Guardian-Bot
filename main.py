"""
Made by I Nyoman Widiyasa Jayananda. (G-Tech Programming Div.)
Bebas untuk di copy-paste dan dikembangkan sesuai keinginan.
"""

import discord
import os
import dotenv
from discord.ext import commands
dotenv.load_dotenv('./.gitignore/secret.env') #Meng-aktivasi penggunaan os.getenv()
token = os.getenv('token')

intents = discord.Intents.all() #Sesuaikan intents dengan bot kalian!
bot = commands.Bot(command_prefix="!", status = discord.Status.idle, intents = intents) 

"""
Event on_connect berbeda dengan event on_ready.
Baca dokumentasi discord.py untuk selengkapnya.
"""

@bot.event
async def on_connect():
    print('Guardian telah connect ke Discord!')

@bot.event
async def on_ready():
    print('Guardian siap!')

"""
Command-command dasar
"""

@bot.command()
async def ping(ctx): #discord.ext.commands.context.Context, wajib di setiap command.
    await ctx.reply(f'Pong! Latency: {round(bot.latency*1000)}ms')

@bot.command()
async def sayname(ctx, user:commands.MemberConverter):
    await ctx.reply(f'{user.name}')

"""
Aktifkan/nonaktifkan kategori command yang berada di ./commands
"""

@bot.command(aliases = ['on', 'enable']) #aliases berupa list
@commands.is_owner() #Hanya pemilik bot yang bisa menjalankan command ini
async def load(ctx, ext):
  try:
    bot.load_extension(f"commands.{ext}")
    await ctx.send(f"File `{ext}.py` sekarang aktif!")
  except commands.ExtensionAlreadyLoaded:
    await ctx.send(f"File `{ext}.py` sudah aktif!")
  except commands.ExtensionNotFound:
    await ctx.send(f"Tidak dapat menemukan file `{ext}.py`!")

@bot.command(aliases = ['off', 'disable'])
@commands.is_owner()
async def unload(ctx, ext):
  try:
    bot.unload_extension(f"commands.{ext}")
    await ctx.send(f"File `{ext}.py` sekarang tidak aktif!")
  except commands.ExtensionNotFound:
    await ctx.send(f"Tidak dapat menemukan file `{ext}.py`!")
  except commands.ExtensionNotLoaded:
    await ctx.send(f"File `{ext}.py` sudah tidak aktif!")

"""
Load semua command yang berada di ./commands
Dilakukan setiap boot-up bot.
"""

for file in os.listdir('./commands'):
    if file.endswith('.py'):
        bot.load_extension(f'commands.{file[:-3]}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot: return #Jika user = bot, exit.
    if not message.guild: return #Jika tidak dijalankan dalam sebuah server, abaikan semua command (opsional)

bot.run(token) #Jalankan bot