import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Startup Event ---
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Downloading videos ⚡"))
    print(f"Logged in as {bot.user}")

# --- Help Command ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📘 Flow Downloader Commands",
        description="Neon‑blue premium downloader bot",
        color=0x00FFFF
    )
    embed.add_field(name="!dl <link>", value="Download a video from TikTok, X, YouTube, Instagram, Reddit, etc.", inline=False)
    embed.add_field(name="!ping", value="Check if the bot is online.", inline=False)
    await ctx.send(embed=embed)

# --- Ping Command ---
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! Bot is online.")

# --- Download Command ---
@bot.command()
async def dl(ctx, url: str):
    status = await ctx.send("⏳ Downloading...")

    ydl_opts = {
        "outtmpl": "video.mp4",
        "format": "mp4/best",
        "quiet": True,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        embed = discord.Embed(
            title="🎬 Video Downloaded",
            description=f"Here’s your video from:\n{url}",
            color=0x00FFFF
        )
        embed.set_footer(text="Flow Downloader • Neon Blue Theme")

        await status.delete()
        await ctx.send(embed=embed, file=discord.File("video.mp4"))
        os.remove("video.mp4")

    except Exception as e:
        await status.delete()
        await ctx.send(f"⚠️ Error: {e}\nTry a direct video link.")

bot.run(os.getenv("TOKEN"))
