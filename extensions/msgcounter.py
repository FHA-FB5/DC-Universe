import discord
import os

from discord.ext import commands, tasks

from models.state import State


class MsgCounter(commands.Cog, name='MsgCounter'):
    def __init__(self, bot):
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID')
        if isinstance(self.bot_user_id, str):
            self.bot_user_id = int(
                self.bot_user_id)

        guild_message_count = State.get(
            'guild_message_count')
        self.guild_message_count = 0

        if not guild_message_count:
            State.set('guild_message_count', "0")
        else:
            self.guild_message_count = int(guild_message_count.value)

        self.update_in_db.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        # check if bot react
        if message.author.id == self.bot_user_id:
            return

        self.guild_message_count += 1

    def cog_unload(self):
        self.update_in_db.cancel()

    @tasks.loop(seconds=60.0)
    async def update_in_db(self):
        State.set('guild_message_count', str(self.guild_message_count))


def setup(bot):
    bot.add_cog(MsgCounter(bot))
