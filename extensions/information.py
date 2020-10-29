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
            title = 'Bib - Bibliothek',
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
            title = 'FSR - Fachschaftsrat',
            url = 'https://fsr5.de/',
            description = 'Der Fachschaftsrat besteht aus gewählten studentischen Mitgliedern des Fachbereichs.',
            timestamp = time
        )
        embed.add_field(
            name = 'Covid-19',
            value = 'Normalerweise könnt ihr zu gegebenen Sprechzeiten (9:45 - 10:15 und 11:45 - 12:15) einfach im Raum E034 vorbeischauen, dies ist aufgrund der aktuellen Situation leider nicht möglich.\nDennoch stehen euch die hübschen Menschen vom FSR auf verschiedenste Arten zur Verfügung.',
            inline = False
        )
        embed.set_image(url='https://fsr5.de/wp-content/uploads/2019/08/Pyramide4-768x512.jpg')
        embed.set_thumbnail( url=self.fb5_logo )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        embed.add_field(
            name = 'Aktuelles',
            value = 'Folgende Kanäle könnt ihr nutzen, um über aktuelle Themen des FSR informiert zu werden:\n- **Social Media:** [Facebook](http://www.facebook.com/fsr5.fhaachen/) | [Instagram](http://www.instagram.com/fsr5.fhaachen/)\n- **Podcast:** [Spotify](https://open.spotify.com/show/1x9WZEP3JcUGYmi0smQEK1) | [Apple](https://podcasts.apple.com/us/podcast/talking-beats-5-0/id1492162459?ign-mpt=uo%3D4) | [Anchor](https://anchor.fm/fb5-podcast)',
            inline = False
        )
        embed.add_field(
            name = 'Weitere Services',
            value = '- **Altklausuren:**\nDa einige Professoren Altklausuren zur Verfügung stellen, haben wir über die Jahre ein hohes Kontingent angesammelt. Wenn du also zu Klausurbedingungen üben möchtest, komm einfach mit deinem Laptop oder USB Stick vorbei.\n\n- **Skriptbindung:**\nDu hast im Fachschaftsraum die Möglichkeit, Skripte zu binden. Deckblätter und Spiralen sind vorhanden. Ein FSRler erklärt dir, wie die Bindemaschine genutzt wird. Anschließend kannst du dann dein Skript selbst binden.\n\n- **Klokurier:**\nDer Klokurier ist eines unserer neuen Projekte, bei dem wir Informationen und Events rund um den Fachbereich 5 übersichtlich in den Klokabinen am Campus veröffentlichen.\n\n- **Einfach mal schnacken:**\nDie FSRler sing allgemein sehr aufgeschlossene und spaßige Personen mit denen man sich bei Zeiten über fast alles unterhalten kann. In der lockeren Atmosphäre gibt es auch häufig was zu lachen.',
            inline = False
        )
        embed.add_field(
            name = 'Kontakt',
            value = 'Falls du Fragen oder Anmerkungen, wie beispielsweise zum Klorkurier oder zum Podcast, hast, zögere nicht dich beim FSR zu melden.\n- **Formular:** https://fsr5.de/kontakt/ \n- **Email:** fsr-fb5@fh-aachen.de',
            inline = False
        )
        
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

    # AStA
    @commands.command(aliases=['ausschuss'], hidden=True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def asta( self, ctx, member: typing.Optional[discord.Member] ):
        time = datetime.fromisoformat('2020-10-25')
        embed = discord.Embed(
            colour = 0x00b5ad,
            title = 'AStA - Allgemeiner Studierenden Ausschuss',
            url = 'https://asta.fh-aachen.org/',
            description = 'Egal, ob Finanzen, Politik, Soziales, Kultur, Öffentlichkeitsarbeit oder eines von vielen anderen Themen. Der AStA engagiert sich in all diesen Bereichen mit interessierten und kompetenten Vertretern aus der Studierendenschaft.\nEs gibt immer eine Anlaufstelle, wo ihr euch melden könnt damit ihr nicht verwzeifeln müsst.',
            timestamp = time
        )
        embed.set_thumbnail( url = 'https://asta.fh-aachen.org/img/universal/logo.png' )
        embed.set_footer( text = 'Alle Angaben ohne Gewähr!', 
                        icon_url = self.fb5_logo )
        embed.add_field(
            name = 'Weitere Services',
            value = '- **[Die Printe:](https://asta.fh-aachen.org/printe)**\nWas es in und um die Hochschule zu wissen gibt in der Studentischen Zeitung des AStA der FH Aachen...\n\n- **[ISIC:](https://asta.fh-aachen.org/isic)**\nBald auf Reisen? Nutz Rabatte weltweit und beantragt bei uns die "International Student Identitycard"...\n\n- **[Leihgeräte:](https://asta.fh-aachen.org/leihgeraete)**\nDu hast keinen eigenen Laptop für die Online-Klausur zur Verfügung? Wir verleihen diese kostenfrei.\n\n- **[Semesterticket:](https://asta.fh-aachen.org/semesterticket)**\nMit dem Semesterticket durch ganz NRW. Alle Infos und mögliche Rückerstattung im Härtefall...\n\n',
            inline = False
        )
        embed.add_field(
            name = 'Beratung',
            value = '- **[Hier klicken](https://asta.fh-aachen.org/#beratung)**, für ausführlicheren Text\nDer AStA bietet zu dem bei folgenden Themen einfache und Kompetente Beratung an:\n\t + **BAföG und Studienfinanzierung:**\n\t\t studienfinanzierung@asta.fh-aachen.org\n\t + **Hochschulwechselberatung:**\n\t\t hochschulwechsel@asta.fh-aachen.org\n\t + **Prüfungsordnungsberatung:** Über die angegebenen Kanäle\n\t + **Rechtsberatung:** Nach persönlicher Terminvereinbarung\n\t + **Studieren mit Beeinträchtigung:** stumibe@asta.fh-aachen.org\n\t + **Studieren mit Kind:** stumiki@asta.fh-aachen.org',
            inline = False
        )
        embed.add_field(
            name = 'Kontakt',
            value = 'Bei Fragen und Bedürnissen kannst du dich über eine der folgenden Kanäle beim AStA melden.\n- **Adresse:** Stephanstraße 58-62, 52064 Aachen\n- **Email:** asta@fh-aachen.org\n- **Telefon:** 0241 6009-52807',
            inline = False
        )
        
        
        user = ctx.author
        if member:
            user = member
        
        await ctx.send( user.mention, embed=embed )

def setup(bot):
    bot.add_cog(Information(bot))

