import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def dl(ctx, url: str):
    await ctx.send("Downloading...")

    ydl_opts = {
        "outtmpl": "video.mp4",
        "format": "mp4/best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await ctx.send(file=discord.File("video.mp4"))
        os.remove("video.mp4")

    except Exception as e:
        await ctx.send(f"Error: {e}")

bot.run(os.getenv("TOKEN"))
