import discord
from dotenv import load_dotenv
from os import getenv
from random import randint


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Ready! Logged in as {self.user}")

    async def on_message(self, message):
        if message.author.bot or not message.content.startswith("s!"):
            return
        args = message.content[2:].split()
        command = args.pop(0).lower()
        # Ping command
        if command == "ping":
            await message.channel.send("pong")
        # Say command
        elif command == "say":
            await message.delete()
            await message.channel.send(" ".join(args))
            print(" ".join(args))
        # RNG command
        elif command == "rng":
            if len(args) == 0:
                return
            if len(args) == 1:
                rng_min = 1
            else:
                rng_min = int(args.pop(0))
            rng_max = int(args.pop(0))
            await message.channel.send(f"Losowa liczba od {rng_min} do {rng_max}: **{randint(rng_min, rng_max)}**")
        # Role command
        elif command == "role":
            role = None
            # Fetching the mentioned role
            if len(args) > 0 and args[0].startswith("<@&"):
                role_id = int(args.pop(0)[3:-1])
                role = message.guild.get_role(role_id)
                if role is None:
                    await message.channel.send("Nie znalazłem roli")
                    return
            else:
                # Fetching the mentioned member
                if len(args) > 0 and args[0].startswith("<@"):
                    member_id = int(args.pop(0)[2:-1])
                    member = message.guild.get_member(member_id)
                # Else, use the message author
                else:
                    member = message.author
                # Fetching the private role based on the "member" variable
                for member_role in member.roles:
                    if len(member_role.members) == 1 and not member_role.is_premium_subscriber():
                        role = member_role
                if role is None:
                    await message.channel.send("Nie znalazłem prywatnej roli")
                    return
            # Checking if you own the role
            role_ownership = False
            if len(role.members) == 1 and role.members[0] == message.author:
                role_ownership = True
            # Reading the option
            if len(args) == 0:
                option = "info"
            else:
                option = args.pop(0)
            # Info option
            if option == "info":
                role_info = f"Rola: {role.mention}\n"
                if len(role.members) == 1 and not role.is_premium_subscriber():
                    role_info += f"Właściciel roli: {role.members[0].mention}\n"
                role_info += f"Nazwa roli: **{role.name}**\n" \
                             f"Kolor roli: **{role.color}**"
                await message.channel.send(role_info)
            # Name option
            elif option == "name":
                if len(args) == 0:
                    await message.channel.send("Komenda wymaga podania nazwy")
                    return
                if role_ownership is False and message.author.permissions_in(message.channel).manage_roles is False:
                    await message.channel.send("Nie masz uprawnień do zarządzania rolami")
                    return
                role_name = " ".join(args)
                await role.edit(name=role_name)
                await message.channel.send(f"Rola {role.mention} nazywa się teraz **{role_name}**")
            # Color option
            elif option == "color":
                if len(args) == 0:
                    await message.channel.send("Komenda wymaga podania koloru")
                    return
                if role_ownership is False and message.author.permissions_in(message.channel).manage_roles is False:
                    await message.channel.send("Nie masz uprawnień do zarządzania rolami")
                    return
                if args[0].startswith("#"):
                    args[0] = args[0][1:]
                if len(args[0]) > 6:
                    await message.channel.send(f"**#{args[0]}** nie jest poprawnym kolorem heksadecymalnym (maksymalnie 6 cyfer)")
                    return
                try:
                    role_color = int(args[0], 16)
                except ValueError:
                    await message.channel.send(f"**#{args[0]}** nie jest poprawnym kolorem heksadecymalnym (0-9, A-F)")
                    return
                await role.edit(color=role_color)
                await message.channel.send(f"Rola {role.mention} posiada teraz kolor **#{hex(role_color)[2:]}**")


load_dotenv()
intents = discord.Intents(guilds=True, members=True, messages=True)
client = MyClient(intents=intents)
client.run(getenv("TOKEN"))
