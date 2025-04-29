# main.py
import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread

# ---- Keep-Alive Server ----
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"
def run_web():
    app.run(host='0.0.0.0', port=8080)
Thread(target=run_web).start()

# ---- Bot Setup ----
OWNER_ID = 1160976559184818176
GUILD_ID = 1363546001700421774  # for testing; remove guild parameter for global

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree

# a consistent embed style
EMBED_COLOR = discord.Color.blurple()

# sync slash commands on ready
@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Logged in as {bot.user}")

# ---- /setup (owner only) ----
@tree.command(name="setup", description="Create all roles & channels", guild=discord.Object(id=GUILD_ID))
async def setup(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        return await interaction.response.send_message("❌ You can’t run this.", ephemeral=True)
    roles = ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','R11',
             'PR1','PR2','PR3','PR4','PR5','PR6','PR7','PR8','PR9','PR10','PR11',
             'Low','Mid','High','P low','P mid','P high',
             'Hoster','Moderator','Admin']
    for name in roles:
        if not discord.utils.get(interaction.guild.roles, name=name):
            await interaction.guild.create_role(name=name)
    # you can add channel/category creation here...
    embed = discord.Embed(title="Setup Complete", color=EMBED_COLOR)
    await interaction.response.send_message(embed=embed)

# ---- /hostgame ----
@tree.command(name="hostgame", description="Host a league game", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    teamsize="Number of players per side (2,3,4)",
    perks="Enable perks?",
    region="Server region"
)
@app_commands.choices(region=[
    app_commands.Choice(name="EU", value="EU"),
    app_commands.Choice(name="NA", value="NA"),
    app_commands.Choice(name="Asia", value="Asia"),
])
async def hostgame(interaction: discord.Interaction,
                   teamsize: app_commands.Range[int, 2, 4],
                   perks: bool,
                   region: app_commands.Choice[str]):
    embed = discord.Embed(
        title="🎮 New Game Hosted",
        description=f"**Mode:** {teamsize}v{teamsize}\n"
                    f"**Region:** {region.value}\n"
                    f"**Perks:** {'✅' if perks else '❌'}",
        color=EMBED_COLOR
    )
    await interaction.response.send_message(embed=embed)

# ---- /leaderboard ----
@tree.command(name="leaderboard", description="Display the league leaderboard", guild=discord.Object(id=GUILD_ID))
async def leaderboard(interaction: discord.Interaction):
    # TODO: fetch & format your leaderboard data
    embed = discord.Embed(title="🏆 Leaderboard", color=EMBED_COLOR)
    embed.add_field(name="1. PlayerA", value="10 wins", inline=False)
    embed.add_field(name="2. PlayerB", value="8 wins", inline=False)
    await interaction.response.send_message(embed=embed)

# ---- /recordmatch ----
@tree.command(name="recordmatch", description="Record the result of a match", guild=discord.Object(id=GUILD_ID))
async def recordmatch(interaction: discord.Interaction,
                      winner: discord.Member,
                      loser: discord.Member):
    # TODO: record in DB
    embed = discord.Embed(
        title="✅ Match Recorded",
        description=f"{winner.mention} beat {loser.mention}",
        color=EMBED_COLOR
    )
    await interaction.response.send_message(embed=embed)

# ---- /warn ----
@tree.command(name="warn", description="Warn a user", guild=discord.Object(id=GUILD_ID))
async def warn(interaction: discord.Interaction,
               member: discord.Member,
               reason: str = "No reason provided"):
    embed = discord.Embed(
        title="⚠️ User Warned",
        description=f"{member.mention}\nReason: {reason}",
        color=EMBED_COLOR
    )
    await interaction.response.send_message(embed=embed)

# ---- /endgame ----
@tree.command(name="endgame", description="End the current game", guild=discord.Object(id=GUILD_ID))
async def endgame(interaction: discord.Interaction):
    embed = discord.Embed(title="🏁 Game Ended", color=EMBED_COLOR)
    await interaction.response.send_message(embed=embed)

# ---- /leave ----
@tree.command(name="leave", description="Leave the current game", guild=discord.Object(id=GUILD_ID))
async def leave(interaction: discord.Interaction):
    embed = discord.Embed(description=f"{interaction.user.mention} left the game.", color=EMBED_COLOR)
    await interaction.response.send_message(embed=embed)

# (…repeat similarly for all your other commands…)

# ---- Run Bot ----
bot.run(os.getenv("TOKEN"))