import discord
import os
import typing

from datetime import datetime
from stringcolor import cs
from discord.ext import commands

class Information(commands.Cog, name='Informations'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['services'])
    async def shortMentionForServices( self, ctx ):
        time = datetime.fromisoformat('2020-10-22')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'Verfügbare Services der FH Aachen',
            description = 'Für weitere Infos kannst du den Befehl zum entsprechenden Service benutzen',
            url = 'https://www.fh-aachen.de/fachbereiche/elektrotechnik-und-informationstechnik/',
            timestamp = time
        )
        embed.set_thumbnail(url='https://www.fh-aachen.de/fileadmin/template/pics/logo_alt/logo-FH.png')
        embed.set_footer( text='Alle Angaben ohne Gewähr!', 
                        icon_url='' )
        embed.add_field(
            name = 'Services',
            value = 'Allgemeine FH-Account Verwaltung.\nhttps://services.fh-aachen.de/',
            inline = False
        )
        embed.add_field(
            name = 'Ilias',
            value = 'Die Online Lernplattform, wo alle Vorlesungsinhalte zusammengetragen sind.\nhttps://ili.fh-aachen.de/\n' +
                    'Diese Seite bekommt dir hoffentlich bereits bekannt vor :)\nhttps://www.ili.fh-aachen.de/goto_elearning_crs_610475.html',
            inline = False
        )
        embed.add_field(
            name = 'eLectures',
            value = 'Hier findest du Aufzeichnungen zu Vorlesungen (Meist aus Vor-Corona zeiten).\nhttps://www.electures.fh-aachen.de/',
            inline = False
        )
        embed.add_field(
            name = 'Campus Office',
            value = 'Hier kannst du deinen Stundenplan erstellen, deine Praktika anmelden, sowie generelle Informationen über Module erhalten.\nhttps://www.campusoffice.fh-aachen.de/',
            inline = False
        )
        embed.add_field(
            name = 'QIS',
            value = 'Im QIS erhälst du deine Studierendenbescheinigungen, kannst dich zu Prüfungen anmelden und deinen Notenstand einsehen.\nhttps://www.qis.fh-aachen.de/',
            inline = False
        )
        

        await ctx.send( ctx.author.mention, embed=embed )


def setup(bot):
    bot.add_cog(Information(bot))
