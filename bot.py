import disnake
from disnake.ext import commands
import os, re

loc = os.path.dirname(__file__)
with open(loc+'/key.txt', 'r') as key:
    key = key.read()

limit = 3

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='h.', intents=disnake.Intents.all(), activity=disnake.Activity(type=disnake.ActivityType.playing, name='Anti-Spam'), help_command=None)
        self.warnings = {}
    async def on_ready(self):
        print('Ready!')
    async def on_message(self, message):
        if re.search('@everyone', message.content) and re.search('https://discord.gg/', message.content):
            await message.delete()
            if message.author.id in self.warnings.keys():
                warning_count = int(self.warnings[message.author.id])+1
                if warning_count >=limit:
                    await message.channel.send(f'{message.author.mention} has been banned! | Spam | ({warning_count}/{limit})')
                    await message.guild.ban(message.author, reason='Spamming')
                    return
                else:
                    self.warnings[message.author.id] = str(warning_count)
            else:
                warning_count = '1'
                self.warnings[message.author.id] = warning_count
            await message.channel.send(f'{message.author.mention} has been warned! | Spam | ({warning_count}/{limit})')


bot = Client()
bot.run(key)