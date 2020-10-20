import discord
import os
import typing

from discord.ext import commands


class Polls(commands.Cog, name='Polls'):
    def __init__(self, bot):
        self.bot = bot

        self.bot_user_id = os.getenv(
            'BOT_USER_ID'
        )
        if isinstance(self.bot_user_id, str):
            self.bot_user_id = int(self.bot_user_id)

        self.emojis = [
                '1️⃣',
                '2️⃣',
                '3️⃣',
                '4️⃣',
                '5️⃣',
                '6️⃣',
                '7️⃣',
                '8️⃣',
                '9️⃣',
                '🔟',
            ]
    
    @commands.command(aliases=['poll', 'p'], hidden=True)
    async def createPoll(self, ctx, msg: typing.Optional[str], *args ):
        if not msg:
            embed = discord.Embed (
                colour = discord.Colour.red(),
                title = f'Bitte gib eine Frage oder eine Nachricht an, worüber abgestimmt werden kann!'
            )
            await ctx.send(ctx.author.mention, embed=embed)
            return

        else:

            option = ""
            length =  0
            for _ in args:
                length += 1
            
            if length > 0:
                it = 0
                while it != length and it != 10:
                    option = option + self.emojis[it] + '\t - \t' + str(args[it]) + "\n" 
                    it += 1
            
                embed = discord.Embed (
                    colour = discord.Colour.blue(),
                    title = f'Umfrage:',
                    description = '**' + f'{msg}' + '**' + '\n\n' + option + '\n\nStimmt jetzt über die verfügbaren Reaktionen ab.'
                )
                message = await ctx.send(ctx.channel.mention, embed=embed)

                newIt = 0
                while newIt != it:
                    await message.add_reaction(self.emojis[newIt])
                    newIt += 1
                
            else:
                embed = discord.Embed (
                    colour = discord.Colour.blue(),
                    title = f'Einfache Umfrage:',
                    description = '**' + f'{msg}' + '**' + "\n\nStimmt jetzt mit Ja oder Nein über die verfügbaren Reaktionen ab."
                )
                message = await ctx.send(ctx.channel.mention, embed=embed)
                await message.add_reaction('✅')
                await message.add_reaction('❌')
            
            return

    @ commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # check if bot react
        if payload.user_id == self.bot_user_id:
            return
        
        

        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        msg_id = payload.message_id
        msg = await channel.fetch_message(msg_id)

        if payload.emoji.name != '✅' and payload.emoji.name != '❌' and self.emojis.count(payload.emoji.name) == 0:
            await msg.remove_reaction(payload.emoji, payload.member)
            print("hier")
            return
        else:
            removeEmojis = self.emojis.copy()
            removeEmojis.extend('✅')
            removeEmojis.extend('❌')
            removeEmojis.remove(payload.emoji.name)
            print("da")
            for e in removeEmojis:
                await msg.remove_reaction(e, payload.member)
            return
        

def setup(bot):
    bot.add_cog(Polls(bot))