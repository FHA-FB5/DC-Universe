import discord


async def remove_reaction(guild: discord.Guild, payload: discord.RawReactionActionEvent):
    channel: discord.TextChannel = guild.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    await msg.remove_reaction(payload.emoji, payload.member)
    return


async def create_role_and_channels(guild: discord.Guild, role_name: str, channel_name: str) -> \
        (discord.Role, discord.VoiceChannel, discord.TextChannel):
    role = await guild.create_role(name=role_name)
    overwrites = {
        role: discord.PermissionOverwrite(view_channel=True, read_messages=True, connect=True),
        guild.default_role: discord.PermissionOverwrite(view_channel=False, read_messages=False, connect=False)
    }
    voice = await guild.create_voice_channel(name=channel_name, overwrites=overwrites)
    text = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
    return role, voice, text
