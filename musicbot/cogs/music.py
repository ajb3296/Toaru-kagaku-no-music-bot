import re
import os
import math

import discord
import lavalink
from discord.ext import commands, pages
from discord.commands import slash_command, Option

from musicbot.utils.language import get_lan
from musicbot.utils.volumeicon import volumeicon
from musicbot.utils.get_chart import get_melon, get_billboard, get_billboardjp
from musicbot.utils.play_list import play_list
from musicbot.utils.statistics import Statistics
from musicbot import LOGGER, BOT_ID, color_code, BOT_NAME_TAG_VER, host, psw, region

url_rx = re.compile(r'https?://(?:www\.)?.+')


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
        # ensure there exists a client already
        if hasattr(self.client, 'lavalink'):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(
                    host,
                    2333,
                    psw,
                    region,
                    'default-node')
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
        # the data needs to be transformed before being handed down to
        # voice_update_handler
        lavalink_data = {
                't': 'VOICE_STATE_UPDATE',
                'd': data
                }
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool) -> None:
        """
        Connect the bot to the voice channel and create a player_manager
        if it doesn't exist yet.
        """
        # ensure there is a player_manager when creating a new voice_client
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel)

    async def disconnect(self, *, force: bool) -> None:
        """
        Handles the disconnect.
        Cleans up running player and leaves the voice client.
        """
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        # no need to disconnect if we are not connected
        if not force and not player.is_connected:
            return

        # None means disconnect
        await self.channel.guild.change_voice_state(channel=None)

        # update the channel_id of the player to None
        # this must be done because the on_voice_state_update that
        # would set channel_id to None doesn't get dispatched after the
        # disconnect
        player.channel_id = None
        self.cleanup()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(BOT_ID)
            bot.lavalink.add_node(host, 2333, psw, region, "default-node")  # Host, Port, Password, Region, Name

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None
        #  This is essentially the same as `@commands.guild_only()`
        #  except it saves us repeating ourselves (and also a few lines).

        if guild_check:
            await self.ensure_voice(ctx)
            #  Ensure that the bot and command author share a mutual voicechannel.

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed=discord.Embed(title=error.original, description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.respond(embed=embed)
            # The above handles errors thrown in this cog and shows them to the user.
            # This shouldn't be a problem as the only errors thrown in this cog are from `ensure_voice`
            # which contain a reason string, such as "Join a voicechannel" etc. You can modify the above
            # if you want to do things differently.

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        try:
            voice_channel = str(ctx.author.voice.channel.rtc_region)
        except AttributeError:
            raise commands.CommandInvokeError(get_lan(ctx.author.id, "music_not_connected_voice_channel"))

        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=voice_channel)
        # Create returns a player if one exists, otherwise creates.
        # This line is important because it ensures that a player always exists for a guild.

        # Most people might consider this a waste of resources for guilds that aren't playing, but this is
        # the easiest and simplest way of ensuring players are created.

        # These are commands that require the bot to join a voicechannel (i.e. initiating playback).
        # Commands such as volume/skip etc don't require the bot to be in a voicechannel so don't need listing here.
        should_connect = ctx.command.name in ('play', 'connect', 'list', 'chartplay',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            # Our cog_command_error handler catches this and sends it to the voicechannel.
            # Exceptions allow us to "short-circuit" command invocation via checks so the
            # execution state of the command goes no further.
            raise commands.CommandInvokeError(get_lan(ctx.author.id, "music_come_in_voice_channel"))

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError(get_lan(ctx.author.id, "music_not_connected_voice_channel"))

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError(get_lan(ctx.author.id, "music_no_permission"))

            player.store('channel', ctx.channel.id)
            await ctx.author.voice.channel.connect(cls=LavalinkVoiceClient)
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError(get_lan(ctx.author.id, "music_come_in_my_voice_channel"))

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            # When this track_hook receives a "QueueEndEvent" from lavalink.py
            # it indicates that there are no tracks left in the player's queue.
            # To save on resources, we can tell the bot to disconnect from the voicechannel.
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)

    @slash_command()
    async def connect(self, ctx):
        """ Connect to voice channel! """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_connect_voice_channel"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.respond(embed=embed)
        embed=discord.Embed(title=get_lan(ctx.author.id, "music_already_connected_voice_channel"), description='', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        return await ctx.respond(embed=embed)

    @slash_command()
    async def play(self, ctx, *, query: str):
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
            # ALternatively, resullts['tracks'] could be an empty array if the query yielded no tracks.
            if not results or not results['tracks']:
                if nofind < 3:
                    nofind += 1
                elif nofind == 3:
                    embed=discord.Embed(title=get_lan(ctx.author.id, "music_can_not_find_anything"), description='', color=color_code)
                    embed.set_footer(text=BOT_NAME_TAG_VER)
                    return await ctx.followup.send(embed=embed)
            else:
                break

        embed = discord.Embed(color=color_code) #discord.Color.blurple()

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            trackcount = 0

            for track in tracks:
                if trackcount != 1:
                    info = track['info']
                    trackcount = 1
                # Music statistical(for playlist)
                Statistics.up(track['info']['identifier'])

                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)

            embed.title = get_lan(ctx.author.id, "music_play_playlist")
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.title = get_lan(ctx.author.id, "music_play_music")
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            info = track['info']

            # Music statistical
            Statistics.up(info['identifier'])

            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        embed.set_thumbnail(url="http://img.youtube.com/vi/%s/0.jpg" %(info['identifier']))
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()

    @slash_command()
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_dc_not_connect_voice_channel"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_dc_not_connect_my_voice_channel").format(name=ctx.author.name), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await ctx.voice_client.disconnect(force=True)

        embed=discord.Embed(title=get_lan(ctx.author.id, "music_dc_disconnected"), description='', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)

    @slash_command()
    async def skip(self, ctx):
        """ Skip to the next song! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            # We can't skip, if we're not playing the music.
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_not_playing"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)

        await player.skip()

        embed=discord.Embed(title=get_lan(ctx.author.id, "music_skip_next"), description='', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)

    @slash_command()
    async def nowplaying(self, ctx):
        """ Sending the currently playing song! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.current:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_no_playing_music"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '🔴 LIVE'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'
        embed = discord.Embed(color=color_code,
                              title=get_lan(ctx.author.id, "music_now_playing"), description=song)
        embed.set_thumbnail(url=f"{player.current.uri.replace('https://www.youtube.com/watch?v=', 'http://img.youtube.com/vi/')}/0.jpg")
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)

    @slash_command()
    async def queue(self, ctx):
        """ Send a playlist on the page in (*Number of page*) of the playlist list! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_no_music_in_the_playlist"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)

        # 페이지당 띄울 음악 개수
        items_per_page = 10

        if len(player.queue) <= items_per_page:
            queue_list = ''
            for index, track in enumerate(player.queue):
                queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'
            embed = discord.Embed(description=get_lan(ctx.author.id, "music_q").format(lenQ=len(player.queue), queue_list=queue_list), colour=color_code)
            embed.set_footer(text=f'{get_lan(ctx.author.id, "music_page")}\n{BOT_NAME_TAG_VER}')
            return await ctx.followup.send(embed=embed)

        # 총 페이지수 계산
        allpage = math.ceil(len(player.queue) / items_per_page)

        pages_list = []

        for i in range(1, allpage+1):
            queue_list = ''
            numb = (items_per_page * i)
            numa = numb - items_per_page
            
            for index, track in enumerate(player.queue[numa:numb], start=numa):
                queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

            pages_list.append(
                [
                    discord.Embed(description=get_lan(ctx.author.id, "music_q").format(lenQ=len(player.queue), queue_list=queue_list), color=color_code).set_footer(text=f"{get_lan(ctx.author.id, 'music_page')} {str(i)}/{str(allpage)}\n{BOT_NAME_TAG_VER}")
                ]
            )
        paginator = pages.Paginator(pages=pages_list)
        await paginator.respond(ctx.interaction, ephemeral=False)

    @slash_command()
    async def repeat(self, ctx):
        """ Play all the songs in the playlist over and over again! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_not_playing"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)

        # 0 = off, 1 = single track, 2 = queue
        if player.loop == 0:
            player.set_loop(2)
        elif player.loop == 2:
            player.set_loop(1)
        else:
            player.set_loop(0)

        if player.loop == 0:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_repeat_off"), description='', color=color_code)
        elif player.loop == 1:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_repeat_one"), description='', color=color_code)
        elif player.loop == 2:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_repeat_all"), description='', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)

    @slash_command()
    async def remove(self, ctx, index: int):
        """ Remove music from the playlist! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_remove_no_wating_music"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)
        if index > len(player.queue) or index < 1:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_remove_input_over").format(last_queue=len(player.queue)), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)
        removed = player.queue.pop(index - 1)  # Account for 0-index.
        embed=discord.Embed(title=get_lan(ctx.author.id, "music_remove_form_playlist").format(remove_music=removed.title), description='', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)

    @slash_command()
    async def shuffle(self, ctx):
        """ The music in the playlist comes out randomly from the next song! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_not_playing"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)
        player.shuffle = not player.shuffle
        if player.shuffle:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_shuffle_on"), description='', color=color_code)
        else:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_shuffle_off"), description='', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)
    
    @slash_command()
    async def volume(self, ctx, volume: int = None):
        """ Changes or display the volume """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if volume is None:
            volicon = await volumeicon(player.volume)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_now_vol").format(volicon=volicon, volume=player.volume), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)
        if volume > 1000 or volume < 1:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_input_over_vol"), description=get_lan(ctx.author.id, "music_default_vol"), color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)
        await player.set_volume(volume)
        volicon = await volumeicon(player.volume)
        embed=discord.Embed(title=get_lan(ctx.author.id, "music_set_vol").format(volicon=volicon, volume=player.volume), description='', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)
    
    @slash_command()
    async def pause(self, ctx):
        """ Pause or resume music! """
        await ctx.defer()
        
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_not_playing"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)
        if player.paused:
            await player.set_pause(False)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_resume"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.followup.send(embed=embed)
        else:
            await player.set_pause(True)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_pause"), description='', color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.followup.send(embed=embed)
    
    @slash_command()
    async def seek(self, ctx, *, seconds: int):
        """ Adjust the music play time in seconds by the number after the command! """
        await ctx.defer()

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)
        embed=discord.Embed(title=get_lan(ctx.author.id, "music_seek_move_to").format(move_time=lavalink.utils.format_time(track_time)), description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)

    @slash_command()
    async def chartplay(self, ctx, *, chart : Option(str, "Choose chart.", choices=["Melon", "Billboard", "Billboard Japan"]), count : int = 10):
        """ Add the top 10 songs on the selected chart to your playlist! """
        await ctx.defer()

        if count > 100:
            count = 100
        elif count < 1:
            count = 1

        if chart is not None:
            chart = chart.upper()
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if chart == "MELON":
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_parsing_melon"), color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            playmsg = await ctx.followup.send(embed=embed)
            title, artist = await get_melon(count)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_melon_chart_play"), description='', color=color_code)

        elif chart == "BILLBOARD":
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_parsing_billboard"), color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            playmsg = await ctx.followup.send(embed=embed)
            title, artist = await get_billboard(count)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_billboard_chart_play"), description='', color=color_code)

        elif chart == "BILLBOARD JAPAN":
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_parsing_billboardjp"), color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            playmsg = await ctx.followup.send(embed=embed)
            title, artist = await get_billboardjp(count)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_billboardjp_chart_play"), description='', color=color_code)

        musics = []
        for i in range(0, count):
            musics.append(f'{artist[i]} {title[i]}')

        # Play music list
        playmsg, player, info, playmusic, passmusic = await play_list(player, ctx, musics, playmsg)

        embed.add_field(name=get_lan(ctx.author.id, "music_played_music"), value = playmusic, inline=False)
        embed.add_field(name=get_lan(ctx.author.id, "music_can_not_find_music"), value = passmusic, inline=False)
        embed.set_thumbnail(url=f"http://img.youtube.com/vi/{info['identifier']}/0.jpg")
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await playmsg.edit(embed=embed)
        if not player.is_playing:
            await player.play()

    @slash_command()
    async def list(self, ctx, *, arg: str = None):
        """ Load playlists or play the music from that playlist! """
        await ctx.defer()

        anilistpath = "musicbot/anilist"

        # Files list
        files = []
        for file in os.listdir(anilistpath):
            if file.endswith(".txt"):
                files.append(file.replace(".txt", ""))
        # Sort
        files = sorted(files)
        # 재생목록 총 개수
        if arg == "-a":
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_len_list").format(files_len=len(files)), description=get_lan(ctx.author.id, "music_len_list").format(files_len=len(files)), color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.followup.send(embed=embed)

        if arg is not None:
            # List play
            try:
                f = open(f"{anilistpath}/{arg}.txt", 'r')
                list_str = f.read()
                f.close()

            except Exception:
                embed=discord.Embed(title=get_lan(ctx.author.id, "music_list_can_not_find"), description=arg, color=color_code)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await ctx.followup.send(embed=embed)

            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            music_list = list_str.split('\n')
            music_list_process = []
            for music in music_list:
                if music != "":
                    music_list_process.append(music)
            music_list = music_list_process

            # Play music list
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_list_finding"), color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            playmsg = await ctx.respond(embed=embed)

            playmsg, player, info, playmusic, passmusic = await play_list(player, ctx, music_list, playmsg)

            embed=discord.Embed(title=get_lan(ctx.author.id, "music_play_music"), description='', color=color_code)
            embed.add_field(name=get_lan(ctx.author.id, "music_played_music"), value = playmusic, inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "music_can_not_find_music"), value = passmusic, inline=False)
            embed.set_thumbnail(url=f"http://img.youtube.com/vi/{info['identifier']}/0.jpg")
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await playmsg.edit(embed=embed)
            if not player.is_playing:
                await player.play()

        # 리스트 목록
        else:
            # 페이지당 띄울 리스트 개수
            page = 15
            # 총 리스트 수가 page개 이하일 경우
            if len(files) <= page:
                embed=discord.Embed(title=get_lan(ctx.author.id, "music_playlist_list"), description="\n".join(file), color=color_code)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await ctx.followup.send(embed=embed)

            # 총 페이지수 계산
            allpage = math.ceil(len(files) / page)

            pages_list = []

            for i in range(1, allpage+1):
                filelist = ""
                numb = (page * i)
                numa = numb - page
                for a in range(numa, numb):
                    try:
                        filelist = filelist + f"{files[a]}\n"
                    except IndexError:
                        break
                pages_list.append(
                    [
                        discord.Embed(title=get_lan(ctx.author.id, "music_playlist_list"), description=filelist, color=color_code).set_footer(text=f"{get_lan(ctx.author.id, 'music_page')} {str(i)}/{str(allpage)}\n{BOT_NAME_TAG_VER}")
                    ]
                )
            paginator = pages.Paginator(pages=pages_list)
            await paginator.respond(ctx.interaction, ephemeral=False)

def setup(bot):
    bot.add_cog(Music(bot))
    LOGGER.info("Music loaded!")