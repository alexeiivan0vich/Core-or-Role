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

@bot.command(name='add_xp')
async def add_xp(ctx, amount: int):
    """Test: Kullanıcıya XP ekle"""
    discord_id = str(ctx.author.id)
    
    # Önce Zealy user bilgilerini al
    user_info = await zealy.get_user_info(discord_id)
    if not user_info:
        await ctx.send("❌ Zealy hesabınız bulunamadı!")
        return
        
    zealy_user_id = user_info.get('id')
    success = await zealy.add_xp(zealy_user_id, amount)
    
    if success:
        await ctx.send(f"✅ {amount} XP eklendi!")
    else:
        await ctx.send("❌ XP eklenirken bir hata oluştu!")

@bot.command(name='remove_xp')
async def remove_xp(ctx, amount: int):
    """Test: Kullanıcıdan XP sil"""
    discord_id = str(ctx.author.id)
    
    # Önce Zealy user bilgilerini al
    user_info = await zealy.get_user_info(discord_id)
    if not user_info:
        await ctx.send("❌ Zealy hesabınız bulunamadı!")
        return
        
    zealy_user_id = user_info.get('id')
    success = await zealy.remove_xp(zealy_user_id, amount)
    
    if success:
        await ctx.send(f"✅ {amount} XP silindi!")
    else:
        await ctx.send("❌ XP silinirken bir hata oluştu!")

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
