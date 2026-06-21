# Import all the nessecary packages

from dotenv import load_dotenv
import discord, os, pybalt, yaml, aiofiles, base64
import random
from discord.ext import commands

# Loads the .env file and the data inside of it

load_dotenv(".env")
botToken = os.getenv("TOKEN")
botPrefix = os.getenv("PREFIX")
botStatusType = os.getenv("STATUS_TYPE", "playing").lower()
botStatusName = os.getenv("STATUS_NAME")
botStatusURL = os.getenv("STATUS_URL")
bot = commands.Bot(command_prefix=botPrefix,intents=discord.Intents.all())

# Function used for the custom Bot status
async def setStatus(statusType, statusName, statusURL):
    if statusType == "streaming":
        await bot.change_presence(activity=discord.Streaming(name=f"Streaming {statusName}", url=statusURL))
    elif statusType == "listening":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"Listening to {statusName}"))
    elif statusType == "playing":
        await bot.change_presence(activity=discord.Game(name=f"Playing {statusName}"))
    elif statusType == "watching":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Watching {statusName}"))
    else:
        print("[!] The status type entry you entered is incorrect or unavailable.")

# Using on_ready() so if the bot runs the user knows its running

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=discord.Intents.all())
@bot.event
async def on_ready():
    await setStatus(botStatusType,botStatusName,botStatusURL)
    print(f"[!] {bot.user} has woke up from the multibot grave!")

# The specified commands for the bot

@bot.command(name="ping",description="Used to check the bot's ping to Discord")
async def ping(ctx):
    await ctx.send(f"Ping: {int(round(bot.latency*1000,0))}ms")

@bot.command(name="random",description="Chooses a random from a range")
async def ran(ctx, first:int, last:int):
    await ctx.send(f"From {first} to {last}, I choose {random.randint(first,last)}!")

@bot.command(name="download",description="Downloads a video from YouTube/Instagram/Twitter/TikTok")
async def download(ctx, url):
    path = await pybalt.download(url, videoQuality='480')
    if "instagram" in url: await ctx.send("Your Instagram video has been downloaded!",file=discord.File(path))
    elif "youtube" in url: await ctx.send("Your YouTube video has been downloaded!",file=discord.File(path))
    elif "x.com" in url or "twitter" in url: await ctx.send("Your Twitter video has been downloaded!",file=discord.File(path))
    elif "tiktok" in url: await ctx.send("Your TikTok video has been downloaded!",file=discord.File(path))
    if os.name == "nt": os.system(f"del {path}") 
    else: os.system(f"rm {path}")

@bot.command(name="encodeb64",description=f"Encodes a string in Base64")
async def encodeb64(ctx, *, string):
    encoded = base64.b64encode(string.encode()).decode()
    await ctx.send(f"`{string}` encoded in Base64 is `{encoded}`.")

# Runs the bot with the token from .env

bot.run(botToken)
