import re
import os
import math
import difflib
import traceback
from sclib import SoundcloudAPI

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

import lavalink
from lavalink.events import TrackStartEvent, QueueEndEvent
from lavalink.errors import ClientError
from lavalink.server import LoadType

from musicbot.utils.language import get_lan
from musicbot.utils.volumeicon import volumeicon
from musicbot.utils.get_chart import get_melon, get_billboard, get_billboardjp
from musicbot.utils.play_list import play_list
from musicbot.utils.statistics import Statistics
from musicbot import LOGGER, BOT_ID, COLOR_CODE, BOT_NAME_TAG_VER, HOST, PSW, REGION, PORT
from musicbot.utils.equalizer import Equalizer, EqualizerButton
from musicbot.utils.database import Database
from musicbot.utils.paginator import Paginator

url_rx = re.compile(r'https?://(?:www\.)?.+')
is_youtube = re.compile(r'(youtube.com|youtu.be)')

class LavalinkVoiceClient(discord.VoiceClient):
    """
    This is the preferred way to handle external voice sending
    This client will be created via a cls in the connect method of the channel
    see the following documentation:
    https://discordpy.readthedocs.io/en/latest/api.html#voiceprotocol
    """
    
    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        self.client = client
        self.channel = channel
        self.guild_id = channel.guild.id
        self._destroyed = False

        if not hasattr(self.client, 'lavalink'):
            # Instantiate a client if one doesn't exist.
            # We store it in `self.client` so that it may persist across cog reloads,
            # however this is not mandatory.
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(host=HOST,
                                          port=PORT,
                                          password=PSW,
                                          region=REGION,
                                          name='default-node')

        # Create a shortcut to the Lavalink client here.
        self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
                't': 'VOICE_SERVER_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        channel_id = data['channel_id']

        if not channel_id:
            await self._destroy()
            return

        self.channel = self.client.get_channel(int(channel_id))

        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
            't': 'VOICE_STATE_UPDATE',
            'd': data
        }

        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool, self_deaf: bool = False, self_mute: bool = False) -> None:
        """
        Connect the bot to the voice channel and create a player_manager
        if it doesn't exist yet.
        """
        # ensure there is a player_manager when creating a new voice_client
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel, self_mute=self_mute, self_deaf=self_deaf)

    async def disconnect(self, *, force: bool = False) -> None:
        """
        Handles the disconnect.
        Cleans up running player and leaves the voice client.
        """
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        if player is not None:
            # no need to disconnect if we are not connected
            if not force and not player.is_connected:
                return

            # None means disconnect
            await self.channel.guild.change_voice_state(channel=None)

            # update the channel_id of the player to None
            # this must be done because the on_voice_state_update that would set channel_id
            # to None doesn't get dispatched after the disconnect
            player.channel_id = None
            await self._destroy()
    
    async def _destroy(self):
        self.cleanup()

        if self._destroyed:
            # Idempotency handling, if `disconnect()` is called, the changed voice state
            # could cause this to run a second time.
            return

        self._destroyed = True

        try:
            await self.lavalink.player_manager.destroy(self.guild_id)
        except ClientError:
            pass


class Music(commands.Cog, name="music"):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(BOT_ID)
            bot.lavalink.add_node(host=HOST,
                                  port=PORT,
                                  password=PSW,
                                  region=REGION,
                                  name='default-node')

        self.lavalink: lavalink.Client = bot.lavalink
        self.lavalink.add_event_hooks(self)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(title=error.original, description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.
        else:
            print(traceback.format_exc())

    async def create_player(ctx: commands.Context):
        """
        A check that is invoked before any commands marked with `@commands.check(create_player)` can run.

        This function will try to create a player for the guild associated with this Context, or raise
        an error which will be relayed to the user if one cannot be created.
        """
        if ctx.guild is None:
            raise commands.NoPrivateMessage()

        player = ctx.bot.lavalink.player_manager.create(ctx.guild.id)
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ('play', 'scplay', 'connect', 'list', 'chartplay',)

        voice_client = ctx.voice_client

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError(get_lan(ctx.author.id, "먼저 음성 채널에 들어와주세요!"))
        
        voice_channel = ctx.author.voice.channel

        if voice_client is None:
            if not should_connect:
                raise commands.CommandInvokeError(get_lan(ctx.author.id, ":warning: | 음성 채널에 연결되어 있지 않아요!"))

            permissions = voice_channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError(get_lan(ctx.author.id, ":warning: | 권한이 없어요! (Connect, Speak 권한을 주세요!)"))

            if voice_channel.user_limit > 0:
                # A limit of 0 means no limit. Anything higher means that there is a member limit which we need to check.
                # If it's full, and we don't have "move members" permissions, then we cannot join it.
                if len(voice_channel.members) >= voice_channel.user_limit and not ctx.me.guild_permissions.move_members:
                    raise commands.CommandInvokeError(get_lan(ctx.author.id, ":warning: | 음성 채널 정원이 가득 찼어요!"))

            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        elif voice_client.channel.id != voice_channel.id:
            raise commands.CommandInvokeError(get_lan(ctx.author.id, ":warning: | 다른 음성 채널에 있어요! 제가 있는 음성 채널로 와주세요."))

        # 반복 상태 설정
        loop = Database().get_loop(ctx.guild.id)
        if loop is not None:
            player.set_loop(loop)

        # 셔플 상태 설정
        shuffle = Database().get_shuffle(ctx.guild.id)
        if shuffle is not None:
            player.set_shuffle(shuffle)

        return True

    @lavalink.listener(TrackStartEvent)
    async def on_track_start(self, event: TrackStartEvent):
        guild_id = event.player.guild_id
        channel_id = event.player.fetch('channel')
        guild = self.bot.get_guild(guild_id)

        if not guild:
            return await self.lavalink.player_manager.destroy(guild_id)

        channel = guild.get_channel(channel_id)

        if channel:
            embed = discord.Embed(title='Now playing: {} by {}'.format(event.track.title, event.track.author), color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await channel.send(embed=embed)


    @lavalink.listener(QueueEndEvent)
    async def on_queue_end(self, event: QueueEndEvent):
        guild_id = event.player.guild_id
        guild = self.bot.get_guild(guild_id)

        if guild is not None:
            await guild.voice_client.disconnect(force=True)


    @commands.hybrid_command(
        name="connect",
        aliases=['join', '들어와', 'c', 'ㅊ'],
        description="Connect to voice channel!",
    )
    @commands.check(create_player)
    async def connect(self, ctx: Context):
        """ Connect to voice channel! """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            embed = discord.Embed(title=get_lan(ctx.author.id, ":white_check_mark: | 음성 채널에 접속했어요!"), color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        embed = discord.Embed(title=get_lan(ctx.author.id, ":white_check_mark: | 이미 음성 채널에 접속해 있어요!"), color=COLOR_CODE)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        return await ctx.send(embed=embed)


    @commands.hybrid_command(
        name="play",
        aliases=['p', '재생', 'ㅔ', 'add'],
        description="Searches and plays a song from a given query.",
    )
    @app_commands.describe(
        query="찾고싶은 음악의 제목이나 링크를 입력하세요"
    )
    @commands.check(create_player)
    async def play(self, ctx: Context, *, query: str):
        """ Searches and plays a song from a given query. """
        await ctx.defer()

        # Get the player for this guild from cache.
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        nofind = 0
        while True:
            # Get the results for the query from Lavalink.
            results = await player.node.get_tracks(query)

            # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
            # ALternatively, results['tracks'] could be an empty array if the query yielded no tracks.
            if results.load_type == LoadType.EMPTY or not results or not results.tracks:
                if nofind < 3:
                    nofind += 1
                elif nofind == 3:
                    embed = discord.Embed(title=get_lan(ctx.author.id, "아무것도 찾지 못했어요!"), description='', color=COLOR_CODE)
                    embed.set_footer(text=BOT_NAME_TAG_VER)
                    return await ctx.send(embed=embed)
            else:
                break

        embed = discord.Embed(color=COLOR_CODE)  # discord.Color.blurple()

        # Valid load_types are:
        #   TRACK    - direct URL to a track
        #   PLAYLIST - direct URL to playlist
        #   SEARCH   - query prefixed with either "ytsearch:" or "scsearch:". This could possibly be expanded with plugins.
        #   EMPTY    - no results for the query (result.tracks will be empty)
        #   ERROR    - the track encountered an exception during loading
        thumbnail = None
        if results.load_type == LoadType.PLAYLIST:
            tracks = results.tracks

            trackcount = 0

            for track in tracks:
                if trackcount != 1:
                    thumbnail = track.identifier
                    trackcount = 1
                # Music statistical(for playlist)
                Statistics().up(track.identifier)

                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)

            embed.title = get_lan(ctx.author.id, ":arrow_forward: | 플레이리스트 재생!")
            embed.description = f'{results.playlist_info.name} - {len(tracks)} tracks'

        else:
            track = results.tracks[0]
            embed.title = get_lan(ctx.author.id, ":arrow_forward: | 음악 재생!")
            embed.description = f'[{track.title}]({track.uri})'
            thumbnail = track.identifier

            # Music statistical
            Statistics().up(track.identifier)

            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            player.add(requester=ctx.author.id, track=track)

        embed.add_field(name=get_lan(ctx.author.id, "셔플"), value=get_lan(ctx.author.id, "셔플") if player.shuffle else get_lan(ctx.author.id, "셔플"), inline=True)
        embed.add_field(name=get_lan(ctx.author.id, "음악 반복"), value=[get_lan(ctx.author.id, "음악 반복"), get_lan(ctx.author.id, "음악 반복"), get_lan(ctx.author.id, "음악 반복")][player.loop], inline=True)

        if thumbnail is not None:
            embed.set_thumbnail(url=f"http://img.youtube.com/vi/{thumbnail}/0.jpg")
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()


    @commands.hybrid_command(
        name="scplay",
        aliases=['sp', '사클재생', '네', 'addsc'],
        description="Searches and plays a song from a given query.",
    )
    @app_commands.describe(
        query="SoundCloud에서 찾고싶은 음악의 제목이나 링크를 입력하세요"
    )
    # @app_commands.describe(
        # query="찾고싶은 음악의 제목이나 링크를 입력하세요"
    # )
    @commands.check(create_player)
    async def scplay(self, ctx: Context, *, query: str):
        """ Searches and plays a song from a given query. """
        await ctx.defer()

        # Get the player for this guild from cache.
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if is_youtube.search(query):
            embed = discord.Embed(title="Currently youtube playback is not supported", description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'scsearch:{query}'

        nofind = 0
        while True:
            # Get the results for the query from Lavalink.
            results = await player.node.get_tracks(query)

            # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
            # ALternatively, results['tracks'] could be an empty array if the query yielded no tracks.
            if results.load_type == LoadType.EMPTY or not results or not results.tracks:
                if nofind < 3:
                    nofind += 1
                elif nofind == 3:
                    embed = discord.Embed(title=get_lan(ctx.author.id, "아무것도 찾지 못했어요!"), description='', color=COLOR_CODE)
                    embed.set_footer(text=BOT_NAME_TAG_VER)
                    return await ctx.send(embed=embed)
            else:
                break

        embed = discord.Embed(color=COLOR_CODE)  # discord.Color.blurple()

        # Valid load_types are:
        #   TRACK    - direct URL to a track
        #   PLAYLIST - direct URL to playlist
        #   SEARCH   - query prefixed with either "ytsearch:" or "scsearch:". This could possibly be expanded with plugins.
        #   EMPTY    - no results for the query (result.tracks will be empty)
        #   ERROR    - the track encountered an exception during loading
        thumbnail = None
        if results.load_type == LoadType.PLAYLIST:
            tracks = results.tracks

            trackcount = 0

            for track in tracks:
                if trackcount != 1:
                    thumbnail = track.uri
                    trackcount = 1
                # Music statistical(for playlist)
                # Statistics().up(track.identifier)

                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)

            embed.title = get_lan(ctx.author.id, ":arrow_forward: | 플레이리스트 재생!")
            embed.description = f'{results.playlist_info.name} - {len(tracks)} tracks'

        else:
            track = results.tracks[0]
            embed.title = get_lan(ctx.author.id, ":arrow_forward: | 음악 재생!")
            embed.description = f'[{track.title}]({track.uri})'
            thumbnail = track.uri

            # Music statistical
            # Statistics().up(track.identifier)

            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            player.add(requester=ctx.author.id, track=track)

        embed.add_field(name=get_lan(ctx.author.id, "셔플"), value=get_lan(ctx.author.id, "셔플") if player.shuffle else get_lan(ctx.author.id, "셔플"), inline=True)
        embed.add_field(name=get_lan(ctx.author.id, "음악 반복"), value=[get_lan(ctx.author.id, "음악 반복"), get_lan(ctx.author.id, "음악 반복"), get_lan(ctx.author.id, "음악 반복")][player.loop], inline=True)

        if thumbnail is not None:
            track = SoundcloudAPI().resolve(thumbnail)
            if track.artwork_url is not None:
                embed.set_thumbnail(url=track.artwork_url)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()

    @commands.hybrid_command(
        name="disconnect",
        aliases=['dc', '연결해제', '나가', 'ㅇㅊ'],
        description="Disconnects the player from the voice channel and clears its queue.",
    )
    @commands.check(create_player)
    async def disconnect(self, ctx: Context):
        """ Disconnects the player from the voice channel and clears its queue. """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not ctx.voice_client:
            # We can't disconnect, if we're not connected.
            embed = discord.Embed(title=get_lan(ctx.author.id, "음성 채널에 연결되어 있지 않아요!"), color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "{name}님은 제가 있는 음성 채널에 있지 않아요!").format(name=ctx.author.name),
                color=COLOR_CODE
            )
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await ctx.voice_client.disconnect(force=True)

        embed = discord.Embed(title=get_lan(ctx.author.id, ":x: | 연결이 해제되었습니다!"), color=COLOR_CODE)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="skip",
        aliases=['스킵', 's', 'ㄴ'],
        description="Skip to the next song!",
    )
    @commands.check(create_player)
    async def skip(self, ctx: Context):
        """ Skip to the next song! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            # We can't skip, if we're not playing the music.
            embed = discord.Embed(title=get_lan(ctx.author.id, "음악이 재생되고 있지 않습니다!"), description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        await player.skip()

        embed = discord.Embed(title=get_lan(ctx.author.id, "**:track_next: | 다음곡으로 넘어갑니다!**"), description='', color=COLOR_CODE)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="nowplaying",
        aliases=['np', 'n', 'playing', '현재재생중', 'ㅜ', 'ㅞ', 'ㅜㅔ'],
        description="Sending the currently playing song!",
    )
    @commands.check(create_player)
    async def nowplaying(self, ctx: Context):
        """ Sending the currently playing song! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.current:
            embed = discord.Embed(title=get_lan(ctx.author.id, "현재 재생중인 곡이 없습니다!"), description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '🔴 LIVE'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'
        embed = discord.Embed(color=COLOR_CODE,
                              title=get_lan(ctx.author.id, ":arrow_down_small: | 현재 재생중인 곡"), description=song)

        # 셔플, 반복 상태
        embed.add_field(name=get_lan(ctx.author.id, "셔플"), value=get_lan(ctx.author.id, "셔플") if player.shuffle else get_lan(ctx.author.id, "셔플"), inline=True)
        embed.add_field(name=get_lan(ctx.author.id, "음악 반복"), value=[get_lan(ctx.author.id, "음악 반복"), get_lan(ctx.author.id, "음악 반복"), get_lan(ctx.author.id, "음악 반복")][player.loop], inline=True)

        embed.set_thumbnail(url=f"{player.current.uri.replace('https://www.youtube.com/watch?v=', 'http://img.youtube.com/vi/')}/0.jpg")
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="queue",
        aliases=['q', '큐', 'ㅂ'],
        description="Send music queue!",
    )
    @commands.check(create_player)
    async def queue(self, ctx: Context):
        """Send music queue!"""
        async with ctx.typing():
            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            if not player.queue:
                embed = discord.Embed(
                    title=get_lan(ctx.author.id, "재생목록에 음악이 존재하지 않습니다!"),
                    description='',
                    color=COLOR_CODE
                )
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await ctx.send(embed=embed)

            # 페이지당 띄울 음악 개수
            items_per_page = 10

            if len(player.queue) <= items_per_page:
                queue_list = ''
                for index, track in enumerate(player.queue):
                    queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'
                embed = discord.Embed(
                    description=get_lan(ctx.author.id, "**:regional_indicator_q: | {lenQ} 개의 곡(들)이 예약되어 있습니다**\n\n{queue_list}").format(
                        lenQ=len(player.queue),
                        queue_list=queue_list
                    ),
                    color=COLOR_CODE
                )
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await ctx.send(embed=embed)

            # 총 페이지수 계산
            allpage = math.ceil(len(player.queue) / items_per_page)
            embeds = []

            for i in range(1, allpage + 1):
                queue_list = ''
                numb = (items_per_page * i)
                numa = numb - items_per_page

                for index, track in enumerate(player.queue[numa:numb], start=numa):
                    queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

                embed = discord.Embed(
                    description=get_lan(ctx.author.id, "**:regional_indicator_q: | {lenQ} 개의 곡(들)이 예약되어 있습니다**\n\n{queue_list}").format(
                        lenQ=len(player.queue),
                        queue_list=queue_list
                    ),
                    color=COLOR_CODE
                )
                embed.set_footer(text=f"{get_lan(ctx.author.id, 'music_page')} {str(i)}/{str(allpage)}\n{BOT_NAME_TAG_VER}")
                embeds.append(embed)

            # Create and send paginator
            paginator = Paginator(embeds)
            message = await ctx.send(embed=embeds[0], view=paginator)
            paginator.message = message

    @commands.hybrid_command(
        name="repeat",
        aliases=['loop', 'l', '반복', 'ㅣ'],
        description="Repeat one song or repeat multiple songs!",
    )
    @commands.check(create_player)
    async def repeat(self, ctx: Context):
        """ Repeat one song or repeat multiple songs! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed = discord.Embed(title=get_lan(ctx.author.id, "음악이 재생되고 있지 않습니다!"), description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        # 0 = off, 1 = single track, 2 = queue
        if player.loop == 0:
            player.set_loop(2)
        elif player.loop == 2:
            player.set_loop(1)
        else:
            player.set_loop(0)

        Database().set_loop(ctx.guild.id, player.loop)

        embed = None
        if player.loop == 0:
            embed = discord.Embed(title=get_lan(ctx.author.id, ":regional_indicator_x: | 음악 반복재생이 꺼졌습니다!"), description='', color=COLOR_CODE)
        elif player.loop == 1:
            embed = discord.Embed(title=get_lan(ctx.author.id, ":repeat_one: | 한곡 반복재생이 켜졌습니다!"), description='', color=COLOR_CODE)
        elif player.loop == 2:
            embed = discord.Embed(title=get_lan(ctx.author.id, ":repeat: | 전곡 반복재생이 켜졌습니다!"), description='', color=COLOR_CODE)
        if embed is not None:
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="remove",
        aliases=['제거', 'rm'],
        description="Remove music from the playlist!",
    )
    @app_commands.describe(
        index="Queue에서 제거하고 싶은 음악이 몇 번째 음악인지 입력해 주세요"
    )
    @commands.check(create_player)
    async def remove(self, ctx: Context, index: int):
        """ Remove music from the playlist! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            embed = discord.Embed(title=get_lan(ctx.author.id, "대기 중인 음악이 없어요!"), description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if index > len(player.queue) or index < 1:
            embed = discord.Embed(title=get_lan(ctx.author.id, "1 에서 {last_queue} **까지**만 음악이 존재합니다!").format(last_queue=len(player.queue)), description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        removed = player.queue.pop(index - 1)  # Account for 0-index.
        embed = discord.Embed(title=get_lan(ctx.author.id, ":asterisk: | 재생목록에서 음악이 제거되었습니다! :\n**{remove_music}**").format(remove_music=removed.title), description='', color=COLOR_CODE)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="shuffle",
        aliases=['셔플', 'sfl'],
        description="The music in the playlist comes out randomly from the next song!",
    )
    @commands.check(create_player)
    async def shuffle(self, ctx: Context):
        """ The music in the playlist comes out randomly from the next song! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed = discord.Embed(title=get_lan(ctx.author.id, "음악이 재생되고 있지 않습니다!"), description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        player.set_shuffle(not player.shuffle)

        # 셔플 상태 저장
        Database().set_shuffle(ctx.guild.id, player.shuffle)

        if player.shuffle:
            embed = discord.Embed(title=get_lan(ctx.author.id, ":twisted_rightwards_arrows: | 음악 셔플이 켜졌습니다!"), description='', color=COLOR_CODE)
        else:
            embed = discord.Embed(title=get_lan(ctx.author.id, ":twisted_rightwards_arrows: | 음악 셔플이 꺼졌습니다!"), description='', color=COLOR_CODE)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="volume",
        aliases=['vol', 'v', '볼륨', '음량', 'ㅍ'],
        description="Changes or display the volume",
    )
    @app_commands.describe(
        volume="볼륨값을 입력하세요"
    )
    @commands.check(create_player)
    async def volume(self, ctx: Context, volume: int = None):
        """ Changes or display the volume """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if volume is None:
            volicon = await volumeicon(player.volume)
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "{volicon} | {volume}% 로 설정되어 있습니다").format(volicon=volicon, volume=player.volume),
                description='',
                color=COLOR_CODE
            )
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if volume > 1000 or volume < 1:
            embed = discord.Embed(
                title=get_lan(ctx.author.id, ":loud_sound: | 음량은 1% ~ 1000% 까지로 한정되어 있습니다!"),
                description=get_lan(ctx.author.id, "기본값 : 100%"),
                color=COLOR_CODE
            )
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        # 볼륨 설정
        await player.set_volume(volume)

        # 볼륨 아이콘 가져오기
        volicon = await volumeicon(player.volume)
        embed = discord.Embed(
            title=get_lan(ctx.author.id, "{volicon} | {volume}% 로 설정되었습니다!").format(volicon=volicon, volume=player.volume),
            description='',
            color=COLOR_CODE
        )
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="pause",
        aliases=['resume', '일시정지', '일시중지', '재개'],
        description="Pause or resume music!",
    )
    @commands.check(create_player)
    async def pause(self, ctx):
        """ Pause or resume music! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed = discord.Embed(title=get_lan(ctx.author.id, "음악이 재생되고 있지 않습니다!"), description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if player.paused:
            await player.set_pause(False)
            embed = discord.Embed(title=get_lan(ctx.author.id, ":play_pause: | 재생합니다!"), description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
        else:
            await player.set_pause(True)
            embed = discord.Embed(title=get_lan(ctx.author.id, ":play_pause: | 일시정지 되었습니다!"), description='', color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="seek",
        aliases=['탐색'],
        description="Adjust the music play time in seconds by the number after the command!",
    )
    @app_commands.describe(
        seconds="이동할 초를 입력하세요"
    )
    async def seek(self, ctx: Context, *, seconds: int):
        """ Adjust the music play time in seconds by the number after the command! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)
        embed = discord.Embed(
            title=get_lan(ctx.author.id, "**:clock: | {move_time} 으로 이동합니다!**").format(move_time=lavalink.utils.format_time(track_time)),
            description='',
            color=COLOR_CODE
        )
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="chartplay",
        aliases=['cp', '차트재생', '차트', 'ㅊㅌ', '체'],
        description="Add the top 10 songs on the selected chart to your playlist!",
    )
    @app_commands.describe(
        chart="Choose chart",
        count="Enter the number of chart songs to play"
    )
    @commands.check(create_player)
    @app_commands.choices(chart=[
        app_commands.Choice(name="Melon", value="Melon"),
        app_commands.Choice(name="Billboard", value="Billboard"),
        app_commands.Choice(name="Billboard Japan", value="Billboard Japan")
    ])
    async def chartplay(self, ctx: Context, *, chart: str, count: int):
        """ Add the top 10 songs on the selected chart to your playlist! """
        await ctx.defer()

        embed = None
        artist = None
        title = None
        playmsg = None

        if count > 100:
            count = 100
        elif count < 1:
            count = 1

        if chart is not None:
            chart = chart.upper()
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if chart == "MELON":
            embed = discord.Embed(title=get_lan(ctx.author.id, "멜론 파싱중..."), color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            playmsg = await ctx.send(embed=embed)
            title, artist = await get_melon(count)
            embed = discord.Embed(title=get_lan(ctx.author.id, ":arrow_forward: | 멜론차트 음악 재생!"), color=COLOR_CODE)

        elif chart == "BILLBOARD":
            embed = discord.Embed(title=get_lan(ctx.author.id, "빌보드차트 파싱중..."), color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            playmsg = await ctx.send(embed=embed)
            title, artist = await get_billboard(count)
            embed = discord.Embed(title=get_lan(ctx.author.id, ":arrow_forward: | 빌보드차트 음악 재생!"), color=COLOR_CODE)

        elif chart == "BILLBOARD JAPAN":
            embed = discord.Embed(title=get_lan(ctx.author.id, "빌보드 재팬 차트 파싱중..."), color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            playmsg = await ctx.send(embed=embed)
            title, artist = await get_billboardjp(count)
            embed = discord.Embed(title=get_lan(ctx.author.id, ":arrow_forward: | 빌보드 재팬 차트 음악 재생!"), color=COLOR_CODE)

        musics = []
        if artist is not None and title is not None:
            for i in range(0, count):
                musics.append(f'{artist[i]} {title[i]}')

        # Play music list
        playmsg, player, thumbnail, playmusic, passmusic = await play_list(player, ctx, musics, playmsg)

        if embed is not None:
            embed.add_field(name=get_lan(ctx.author.id, "재생한 음악"), value=playmusic, inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "찾지 못한 음악"), value=passmusic, inline=False)
            if thumbnail is not None:
                embed.set_thumbnail(url=f"http://img.youtube.com/vi/{thumbnail}/0.jpg")
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await playmsg.edit(embed=embed)
            if not player.is_playing:
                await player.play()

    @commands.hybrid_command(
        name="equalizer",
        aliases=['eq', 'ㄷㅂ', '이퀄라이저', '이퀄'],
        description="Send equalizer dashboard",
    )
    @commands.check(create_player)
    async def equalizer(self, ctx: Context):
        """ Send equalizer dashboard """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        eq = player.fetch('eq', Equalizer())

        selector = f'{" " * 8}^^^'
        await ctx.send(f'```diff\n{eq.visualise()}\n{selector}```', view=EqualizerButton(ctx, player, eq, 0))


async def setup(bot):
    await bot.add_cog(Music(bot))
    LOGGER.info("Music loaded!")