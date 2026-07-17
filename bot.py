import discord
from discord.ext import commands
import yt_dlp
import os

# Set up intents (no privileged intents required)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Startup Event ---
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="!dl <url> to download"))

# --- Ping Command ---
@bot.command()
async def ping(ctx):
    """Check if the bot is online."""
    await ctx.send("🏓 Pong! Bot is online.")

# --- Help Command ---
@bot.command()
async def help(ctx):
    """Display available commands."""
    embed = discord.Embed(
        title="📘 Video Downloader Commands",
        description="Download videos from any supported site",
        color=0x00FFFF
    )
    embed.add_field(
        name="!dl <url>",
        value="Download a video from TikTok, Instagram, YouTube, Twitter/X, Reddit, etc.",
        inline=False
    )
    embed.add_field(
        name="!ping",
        value="Check if the bot is online",
        inline=False
    )
    embed.set_footer(text="Video Downloader Bot")
    await ctx.send(embed=embed)

# --- Download Command ---
@bot.command()
async def dl(ctx, url: str):
    """Download a video from a supported platform."""
    status = await ctx.send("⏳ Downloading video...")

    ydl_opts = {
        "outtmpl": "video.mp4",
        "format": "best[ext=mp4]/best",
        "quiet": False,
        "no_warnings": True,
        "noplaylist": True,
    }

    try:
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Video")

        # Create success embed
        embed = discord.Embed(
            title="🎬 Video Downloaded",
            description=f"**Title:** {title}\n\n**Source:** {url}",
            color=0x00FFFF
        )
        embed.set_footer(text="Video Downloader Bot")

        # Delete status message and send video
        await status.delete()
        
        # Check file exists and send
        if os.path.exists("video.mp4"):
            await ctx.send(embed=embed, file=discord.File("video.mp4"))
            os.remove("video.mp4")
        else:
            await ctx.send("❌ Error: Video file not found after download.")

    except Exception as e:
        await status.delete()
        error_embed = discord.Embed(
            title="❌ Download Failed",
            description=f"**Error:** {str(e)}\n\n**Tip:** Make sure the link is valid and publicly accessible.",
            color=0xFF0000
        )
        error_embed.set_footer(text="Video Downloader Bot")
        await ctx.send(embed=error_embed)

# Run the bot
if __name__ == "__main__":
    token = os.getenv("TOKEN")
    if not token:
        print("ERROR: TOKEN environment variable not set!")
        exit(1)
    bot.run(token)

