from dotenv import load_dotenv
import discord, os, pybalt, yaml, aiofiles, base64
import random
from discord.ext import commands
load_dotenv(".env")
botToken = os.getenv('TOKEN')
bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=discord.Intents.all())
@bot.event
async def on_ready():
    print(f"{bot.user} has woke up from the multibot grave!")
@bot.command(name="ping",description="Used to check the bot's ping to Discord")
async def ping(ctx):
    await ctx.send(f"Ping: {int(round(bot.latency*1000,0))}ms")
@bot.command(name="random",description="Chooses a random from a range")
async def ran(ctx, first:int, last:int):
    await ctx.send(f"From {first} to {last}, I choose {random.randint(first,last)}!") # another fix
@bot.command(name="download",description="Downloads a video from YouTube/Instagram/Twitter/TikTok")
async def download(ctx, url):
    path = await pybalt.download(url, videoQuality='480')
    if "instagram" in url: await ctx.send("Your Instagram video has been downloaded!",file=discord.File(path))
    elif "youtube" in url: await ctx.send("Your YouTube video has been downloaded!",file=discord.File(path))
    elif "x" or "twitter" in url: await ctx.send("Your Twitter video has been downloaded!",file=discord.File(path))
    elif "tiktok" in url: await ctx.send("Your T witter video has been downloaded!",file=discord.File(path))
    if os.name == "nt": os.system(f"del {path}") 
    else: os.system(f"rm {path}")
@bot.command(name="encodeb64",description=f"Encodes a string in Base64")
async def encodeb64(ctx, *, string):
    encoded = base64.b64encode(string.encode()).decode()
    await ctx.send(f"`{string}` encoded in Base64 is `{encoded}`.")
bot.run(botToken)
