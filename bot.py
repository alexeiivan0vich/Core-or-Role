import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.zealy_api import ZealyAPI

# Load environment variables once at startup
load_dotenv()

# Validate required environment variables
required_env_vars = ['DISCORD_TOKEN', 'ZEALY_API_KEY']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Bot setup with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
zealy = ZealyAPI()

@bot.event
async def on_ready():
    print(f'Bot başlatıldı: {bot.user}')
    print('------------------------')

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Merhaba {ctx.author.name}!')

@bot.command(name='whoami')
async def whoami(ctx):
    """Kullanıcının Discord bilgilerini gösterir"""
    user = ctx.author
    response = (
        f"👤 **Discord Bilgilerin**\n"
        f"ID: `{user.id}`\n"
        f"İsim: `{user.name}`\n"
        f"Tag: `{user.discriminator}`\n"
        f"Tam İsim: `{user.name}#{user.discriminator}`\n"
    )
    await ctx.send(response)

@bot.command(name='zealy')
async def check_zealy(ctx):
    """Kullanıcının Zealy bilgilerini gösterir"""
    user_id = str(ctx.author.id)
    
    # Zealy'den kullanıcı bilgilerini al
    user_info = await zealy.get_user_info(user_id)
    
    if user_info:
        response = (
            f"🏆 **Zealy Bilgilerin**\n"
            f"XP: `{user_info.get('xp', 0)}`\n"
            f"Level: `{user_info.get('level', 0)}`\n"
            f"Rank: `{user_info.get('rank', 'N/A')}`\n"
        )
    else:
        response = "❌ Zealy bilgileriniz bulunamadı. Zealy hesabınızı Discord ile bağladığınızdan emin olun."
    
    await ctx.send(response)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
