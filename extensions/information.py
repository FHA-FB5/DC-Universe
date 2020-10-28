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
    async def shortMentionForServices( self, ctx, member: typing.Optional[discord.Member] ):
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
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

    @commands.command(aliases=['links', 'href'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def listOfImportantUrls( self, ctx, member: typing.Optional[discord.Member] ):
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
            name = 'Studierendensekretariat',
            value = 'https://www.fh-aachen.de/hochschule/studierendensekretariat/',
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
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

    # Services
    @commands.command(aliases=['account'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def fhservice( self, ctx, member: typing.Optional[discord.Member] ):
        time = datetime.fromisoformat('2020-10-25')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'FH Aachen - Services',
            url = 'https://services.fh-aachen.de/',
            description = '',
            timestamp = time
        )
        embed.set_thumbnail( url=self.fb5_logo )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        
        await ctx.send(ctx.author.mention, embed=embed)

    # ilias
    @commands.command(aliases=['ili','elearning'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def ilias( self, ctx, member: typing.Optional[discord.Member] ):
        time = datetime.fromisoformat('2020-10-25')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'Ilias - eLearning',
            url = 'https://www.ili.fh-aachen.de/',
            description = '',
            timestamp = time
        )
        embed.set_thumbnail( url='https://itacademy.fh-aachen.de/templates/default/images/HeaderIcon100.png' )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )

        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )
    
    # eLectures
    @commands.command(aliases=['el','vorlesung','lectures','aufzeichnung'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def electures( self, ctx, member: typing.Optional[discord.Member] ):
        time = datetime.fromisoformat('2020-10-25')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'eLectures - FH Aachen',
            url = 'https://www.electures.fh-aachen.de/',
            description = '',
            timestamp = time
        )
        embed.set_thumbnail( url=self.fb5_logo )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

    # Campus Office
    @commands.command(aliases=['campusoffice','co','office','stundenplan'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def campus( self, ctx, member: typing.Optional[discord.Member] ):
        time = datetime.fromisoformat('2020-10-25')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'Campus Office',
            url = 'https://www.campusoffice.fh-aachen.de/',
            description = '',
            timestamp = time
        )
        embed.set_thumbnail( url='https://www.campusoffice.fh-aachen.de/custom/shared/img/cascampus-stroke-150.gif' )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

    # QIS
    @commands.command(aliases=['kis','kiss'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def qis( self, ctx, member: typing.Optional[discord.Member] ):
        time = datetime.fromisoformat('2020-10-25')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'QIS',
            url = 'https://www.qis.fh-aachen.de/',
            description = '',
            timestamp = time
        )
        embed.set_thumbnail( url=self.fb5_logo )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

    # Bibliothek
    @commands.command(aliases=['bibliothek','biblio'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def bib( self, ctx, member: typing.Optional[discord.Member] ):
        time = datetime.fromisoformat('2020-10-25')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'Bibliothek',
            url = 'https://www.fh-aachen.de/hochschule/bibliothek/',
            description = '',
            timestamp = time
        )
        embed.set_thumbnail( url=self.fb5_logo )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

    # Webex
    @commands.command(aliases=['meeting','meetings','meet'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def webex( self, ctx, member: typing.Optional[discord.Member] ):
        time = datetime.fromisoformat('2020-10-25')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'Cisco Webex Meetings',
            url = 'https://www.webex.com/de/index.html',
            description = '',
            timestamp = time
        )
        embed.set_thumbnail( url='https://www.webex.com/content/dam/wbx/global/images/home_2.png' )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

    # fsr
    @commands.command(aliases=['fachschaft','fachschaftsrat','rat','zweifelamstudium'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def fsr( self, ctx, member: typing.Optional[discord.Member] ):
        time = datetime.fromisoformat('2020-10-25')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'Fachschaftsrat',
            url = 'https://fsr5.de/',
            description = 'Der Fachschaftsrat besteht aus gewählten studentischen Mitgliedern des Fachbereichs.',
            timestamp = time
        )
        embed.set_image(url='https://fsr5.de/wp-content/uploads/2019/08/Pyramide4-768x512.jpg')
        embed.set_thumbnail( url=self.fb5_logo )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        
        
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

def setup(bot):
    bot.add_cog(Information(bot))

