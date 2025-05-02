import discord
from discord.ext import commands
from discord import app_commands
import aiosqlite
import aiohttp
import asyncio
from difflib import get_close_matches

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree
DB_NAME = "components.db"

component_cache = {
    "by_name": {},
    "by_type": {}
}

async def update_component_cache():
    url = "https://api.uexcorp.space/items"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                component_cache["by_name"] = {item["name"].lower(): item for item in data}
                component_cache["by_type"] = {}
                for item in data:
                    typ = item["type"].lower()
                    component_cache["by_type"].setdefault(typ, []).append(item)

async def refresh_cache_periodically():
    while True:
        await update_component_cache()
        await asyncio.sleep(3600)

@bot.event
async def on_ready():
    await update_component_cache()
    await tree.sync()
    bot.loop.create_task(refresh_cache_periodically())
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS components (
                user_id INTEGER,
                component TEXT
            )
        """)
        await db.commit()
    print(f"Logged in as {bot.user}")

async def component_autocomplete(interaction: discord.Interaction, current: str):
    current = current.lower()
    matches = [name for name in component_cache["by_name"] if current in name][:25]
    return [app_commands.Choice(name=name, value=name) for name in matches]

@tree.command(name="collect", description="Add a component to your inventory")
@app_commands.describe(component="Component name")
@app_commands.autocomplete(component=component_autocomplete)
async def collect(interaction: discord.Interaction, component: str):
    await interaction.response.defer()
    component_lower = component.lower()
    if component_lower not in component_cache["by_name"]:
        await interaction.followup.send(f"Component '{component}' not found.")
        return
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO components (user_id, component) VALUES (?, ?)", (interaction.user.id, component_lower))
        await db.commit()
    details = component_cache["by_name"][component_lower]
    info = f"Type: {details.get('type', 'Unknown')}, Grade: {details.get('grade', 'N/A')}, Size: {details.get('size', 'N/A')}"
    await interaction.followup.send(f"Collected: **{component}**\n{info}")

@tree.command(name="search", description="Find details about a component")
@app_commands.describe(component="Component name")
@app_commands.autocomplete(component=component_autocomplete)
async def search(interaction: discord.Interaction, component: str):
    await interaction.response.defer()
    data = component_cache["by_name"].get(component.lower())
    if not data:
        await interaction.followup.send("Component not found.")
        return
    embed = discord.Embed(
        title=data["name"],
        description=f"Type: {data.get('type', 'Unknown')}, Size: {data.get('size', 'N/A')}, Grade: {data.get('grade', 'N/A')}",
        color=discord.Color.blue()
    )
    if "description" in data:
        embed.add_field(name="Description", value=data["description"], inline=False)
    await interaction.followup.send(embed=embed)

# Replace with your actual bot token
bot.run("YOUR_BOT_TOKEN")