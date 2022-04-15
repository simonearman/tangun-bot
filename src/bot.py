import discord
from dotenv import load_dotenv
from os import getenv

client = discord.Client()
load_dotenv()

@client.event
async def on_ready():
    print(f"Ready! Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot or not message.content.startswith("s!"):
        return
    if message.content[2:].startswith("hello"):
        await message.channel.send("hello")


client.run(getenv("TOKEN"))
