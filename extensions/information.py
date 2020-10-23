import discord
import os
import typing

from datetime import datetime
from discord.ext import commands

class Information(commands.Cog, name='Informations'):
    def __init__(self, bot):
        self.bot = bot

        self.fb5_logo = 'https://i.imgur.com/WBeaODR.jpg'

    @commands.command(aliases=['services','dienste'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def shortMentionForServices( self, ctx ):
        time = datetime.fromisoformat('2020-10-22')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'Verfügbare Services der FH Aachen',
            description = 'Für weitere Infos kannst du den Befehl zum entsprechenden Service benutzen',
            url = 'https://www.fh-aachen.de/fachbereiche/elektrotechnik-und-informationstechnik/',
            timestamp = time
        )
        embed.set_thumbnail( url=self.fb5_logo )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        embed.add_field(
            name = 'Services',
            value = 'Allgemeine FH-Account Verwaltung.\nhttps://www.services.fh-aachen.de/',
            inline = False
        )
        embed.add_field(
            name = 'Ilias',
            value = 'Die Online Lernplattform, wo alle Vorlesungsinhalte zusammengetragen sind.\nhttps://www.ili.fh-aachen.de/\n' +
                    'Diese Seite bekommt dir hoffentlich bereits bekannt vor :)\nhttps://www.ili.fh-aachen.de/goto_elearning_crs_610475.html',
            inline = False
        )
        embed.add_field(
            name = 'eLectures',
            value = 'Hier findest du Aufzeichnungen zu Vorlesungen \n(Meist aus Vor-Corona Zeiten).\nhttps://www.electures.fh-aachen.de/',
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
        embed.add_field(
            name = 'Bibliothek',
            value = 'Hier kannst du alle Infos rund um die Bib finden.\nhttps://www.fh-aachen.de/hochschule/bibliothek/',
            inline = False
        )
        
        await ctx.send( ctx.author.mention, embed=embed )

    @commands.command(aliases=['links', 'href'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def listOfImportantUrls( self, ctx ):
        time = datetime.fromisoformat('2020-10-22')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'Wichtige Seiten',
            description = 'Eine kurze Zusammenstellung von Links,\ndie hilfreich sein können.',
            timestamp = time
        )
        embed.set_thumbnail( url=self.fb5_logo )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        embed.add_field(
            name = 'Homepage',
            value = 'http://www.fh-aachen.de/',
            inline = False
        )
        embed.add_field(
            name = 'FB5 - Fachbereich 5',
            value = 'https://www.fh-aachen.de/fachbereiche/elektrotechnik-und-informationstechnik/',
            inline = False
        )
        embed.add_field(
            name = 'FSR5 - Fachschaftsrat des FB5',
            value = 'https://fsr5.de/',
            inline = False
        )
        embed.add_field(
            name = 'AStA - Allgeminer Studierenden Ausschuss',
            value = 'https://asta.fh-aachen.org/',
            inline = False
        )
        embed.add_field(
            name = 'ESP - ErstSemesterProjekt',
            value = 'https://esp.fh-aachen.org/',
            inline = False
        )
        embed.add_field(
            name = 'Prüfungsamt des FB5',
            value = 'https://www.fh-aachen.de/fachbereiche/elektrotechnik-und-informationstechnik/direkteinstieg/fuer-studierende/klausuren-pruefungen-pos/pruefungsamt/',
            inline = False
        )
        embed.add_field(
            name = 'DVZ - Datenverarbeitungszentrale',
            value = 'https://www.fh-aachen.de/hochschule/datenverarbeitungszentrale/',
            inline = False
        )
        embed.add_field(
            name = 'DigiBib',
            value = 'https://fhb-aachen.digibib.net/search/katalog',
            inline = False
        )

        await ctx.send(ctx.author.mention, embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))

