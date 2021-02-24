import math
import re
import discord
import lavalink
from discord.ext import commands
from musicbot import LOGGER, BOT_ID, color_code, BOT_NAME_TAG_VER, host, psw, region, name, port

async def volumeicon(vol : int):
    if vol >= 1 and vol <= 10:
        volicon = ":mute:"
    elif vol >= 11 and vol <= 30:
        volicon = ":speaker:"
    elif vol >= 31 and vol <= 70:
        volicon = ":sound:"
    else:
        volicon = ":loud_sound:"
    return volicon

url_rx = re.compile('https?:\\/\\/(?:www\\.)?.+')  # noqa: W605
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._ = BOT_ID
        self.normal_color = color_code
        self.not_playing = "음악이 재생되고 있지 않습니다!"
        self.melon_url = 'https://www.melon.com/chart/index.htm'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(self._)
            bot.lavalink.add_node(host, port, psw, region, name)  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')
        bot.lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        if guild_check:
            await self.ensure_voice(ctx)
        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed=discord.Embed(title=error.original, description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(aliases=['join', '들어와', 'c', 'ㅊ'])
    async def connect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            #await self.connect_to(ctx.guild.id, ctx.author.voice.channel.id)
            embed=discord.Embed(title=":white_check_mark: | 음성 채널에 접속했어요!", description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        embed=discord.Embed(title=":white_check_mark: | 이미 음성 채널에 접속해 있어요!", description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        return await ctx.send(embed=embed)

    @commands.command(aliases=['p', '재생', 'ㅔ', 'add'])
    async def play(self, ctx, *, query: str = None):
        if query is None and ctx.message.reference is not None:
            query = await self.bot.get_channel(ctx.message.reference.channel_id).fetch_message(ctx.message.reference.message_id)
            query = query.content

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        nofind = 0
        while True:
            results = await player.node.get_tracks(query)
            if not results or not results['tracks']:
                if nofind < 3:
                    nofind += 1
                elif nofind == 3:
                    embed=discord.Embed(title="아무것도 찾지 못했어요!", description='', color=self.normal_color)
                    embed.set_footer(text=BOT_NAME_TAG_VER)
                    return await ctx.send(embed=embed)
            else:
                break

        embed = discord.Embed(color=self.normal_color)

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']
            trackcount = 0
            for track in tracks:
                if trackcount != 1:
                    info = track['info']
                    trackcount = 1
                player.add(requester=ctx.author.id, track=track)
            embed.title = ':arrow_forward: | 플레이리스트 재생!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'

        else:
            track = results['tracks'][0]
            embed.title = ':arrow_forward: | 음악 재생!'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            info = track['info']
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)
        embed.set_thumbnail(url="http://img.youtube.com/vi/%s/0.jpg" %(info['identifier']))
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.reply(embed=embed, mention_author=True)
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['탐색'])
    async def seek(self, ctx, *, seconds: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)
        embed=discord.Embed(title=f'**:clock: | {lavalink.utils.format_time(track_time)} 으로 이동합니다!**', description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['forceskip', '스킵', 's', 'ㄴ'])
    async def skip(self, ctx, arg: int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=self.not_playing, description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if arg is None:
            embed=discord.Embed(title="**:track_next: | 다음곡으로 넘어갑니다!**", description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
            await player.skip()
        else:
            for i in range(arg):
                if not player.current:
                    embed=discord.Embed(title=f"**:track_next: | {i}개의 곡을 건너뛰었어요!**", description='', color=self.normal_color)
                    embed.set_footer(text=BOT_NAME_TAG_VER)
                    return await ctx.send(embed=embed)
                await player.skip()
            embed=discord.Embed(title=f"**:track_next: | {arg}개의 곡을 건너뛰었어요!**", description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

    @commands.command(aliases=['np', 'n', 'playing', '현재재생중', 'ㅜ', 'ㅞ', 'ㅜㅔ'])
    async def now(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.current:
            embed=discord.Embed(title="현재 재생중인 곡이 없습니다!", description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
            return
        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '🔴 LIVE'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'
        embed = discord.Embed(color=self.normal_color,
                              title=':arrow_down_small: | 현재 재생중인 곡', description=song)
        embed.set_thumbnail(url="%s/0.jpg"%player.current.uri.replace('https://www.youtube.com/watch?v=', 'http://img.youtube.com/vi/'))
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['q', '큐', 'ㅂ'])
    async def queue(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            embed=discord.Embed(title="재생목록에 음악이 존재하지 않습니다!", description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
            return
        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)
        start = (page - 1) * items_per_page
        end = start + items_per_page
        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'
        embed = discord.Embed(colour=self.normal_color,
                              description=f'**:regional_indicator_q: | {len(player.queue)} 개의 곡(들)이 예약되어 있습니다**\n\n{queue_list}')
        embed.set_footer(text=f'페이지 {page}/{pages}\n%s' %BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume', '일시정지', '일시중지', '재개'])
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=self.not_playing, description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if player.paused:
            await player.set_pause(False)
            embed=discord.Embed(title=":play_pause: | 재생합니다!", description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
        else:
            await player.set_pause(True)
            embed=discord.Embed(title=":play_pause: | 일시정지 되었습니다!", description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

    @commands.command(aliases=['vol', 'v', '볼륨', '음량', 'ㅍ'])
    async def volume(self, ctx, volume: int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if volume is None:
            volicon = await volumeicon(player.volume)
            embed=discord.Embed(title=f'{volicon} | {player.volume}% 로 설정되어 있습니다', description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        elif volume > 1000 or volume < 1:
            embed=discord.Embed(title=':loud_sound: | 음량은 1% ~ 1000% 까지로 한정되어 있습니다!', description='기본값 : 100%', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        await player.set_volume(volume)
        volicon = await volumeicon(player.volume)
        embed=discord.Embed(title=f'{volicon} | {player.volume}% 로 설정되었습니다!', description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['셔플'])
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title="음악이 재생되고 있지 않습니다!", description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        player.shuffle = not player.shuffle
        embed=discord.Embed(title=':twisted_rightwards_arrows: | 음악 셔플이 ' + ('켜졌습니다' if player.shuffle else '꺼졌습니다') + '!', description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['loop', 'l', '반복', 'ㅣ'])
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=self.not_playing, description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
            return
        player.repeat = not player.repeat
        embed=discord.Embed(title=':repeat: | 음악 반복재생이 ' + ('켜졌습니다' if player.repeat else '꺼졌습니다') + '!', description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['제거', 'rm'])
    async def remove(self, ctx, index: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            embed=discord.Embed(title='대기 중인 음악이 없어요!', description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if index > len(player.queue) or index < 1:
            embed=discord.Embed(title=f'1 에서 {len(player.queue)} **까지**만 음악이 존재합니다!', description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        removed = player.queue.pop(index - 1)  # Account for 0-index.
        embed=discord.Embed(title=f':asterisk: | 재생목록에서 음악이 제거되었습니다 :\n**{removed.title}**', description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['유튜브', 'youtube'])
    async def find(self, ctx, *, query):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query
        search_count = 1
        while True:
            results = await player.node.get_tracks(query)
            if not results or not results['tracks']:
                if search_count != 3:
                    search_count += 1
                else:
                    embed=discord.Embed(title="음악을 찾을 수 없어요...", description='', color=self.normal_color)
                    embed.set_footer(text=BOT_NAME_TAG_VER)
                    return await ctx.send(embed=embed)
            break
        tracks = results['tracks'][:10]  # First 10 results
        o = ''
        for index, track in enumerate(tracks, start=1):
            track_title = track['info']['title']
            track_uri = track['info']['uri']
            o += f'`{index}.` [{track_title}]({track_uri})\n'
        embed = discord.Embed(color=self.normal_color, title="**:globe_with_meridians: | 검색 결과**", description=o)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['dc', '연결해제', '나가', 'ㅇㅊ', 'stop', '중지', '정지'])
    async def disconnect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            embed=discord.Embed(title='음성 채널에 연결되어 있지 않아요!', description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            embed=discord.Embed(title='%s 님은 제가 있는 음성 채널에 있지 않아요!' %ctx.author.id, description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        embed=discord.Embed(title=":x: | 연결이 해제되었습니다!", description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    async def ensure_voice(self, ctx):
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play', 'melonplay', 'connect', 'find')

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('먼저 음성 채널에 들어와주세요.')
        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError(':warning: | 음성 채널에 연결되어 있지 않아요!')
            permissions = ctx.author.voice.channel.permissions_for(ctx.me)
            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError(':warning: | 권한이 없어요! (Connect, Speak 권한을 주세요!)')
            player.store('channel', ctx.channel.id)
            player.fetch('channel')
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError(':warning: | 다른 음성 채널에 있어요! 제가 있는 음성 채널로 와주세요.')


def setup(bot):
    bot.add_cog (Music (bot))
    LOGGER.info("Music loaded!")
