import discord
import enum
import typing

class EmbedColour( enum.Enum ):
    SUCCESS = discord.Colour.green()
    INFO = discord.Colour.blue()
    ERROR = discord.Colour.red()
    FH_MINT = 0x00b5ad

async def create_embed( title: str, embed_colour: EmbedColour = EmbedColour.FH_MINT, url_string: str = None, description_text: str = None ):
    embed = discord.Embed(
        colour = embed_colour.value,
        title = title,
        url = url_string,
        description = description_text
    )

    return embed