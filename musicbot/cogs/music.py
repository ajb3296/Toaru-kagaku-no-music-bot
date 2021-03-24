import os
import re
import math
import discord
import lavalink
from bs4 import BeautifulSoup
from discord.ext import commands
from EZPaginator import Paginator

from musicbot.utils.language import get_lan
from musicbot.utils.crawler import getReqTEXT
from musicbot import LOGGER, BOT_ID, color_code, BOT_NAME_TAG_VER, host, psw, region

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
        self.melon_url = 'https://www.melon.com/chart/index.htm'
        self.billboard_url = 'https://www.billboard.com/charts/hot-100'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(self._)
            bot.lavalink.add_node(host, 2333, psw, region, "default-node")  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')
        bot.lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        self.bot.lavalink._event_hooks.clear()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            voice_channel = self.bot.get_channel(int(before.channel.id))
            player = self.bot.lavalink.player_manager.get(int(voice_channel.guild.id))
            try:
                members = voice_channel.members
                mem = []
                nobot = []
                if not members == []:
                    for m in members:
                        mem.append(m.id)
                        if not m.bot:
                            nobot.append(m.id)
                    if self.bot.user.id in mem:
                        if len(nobot) == 0:
                            player.queue.clear()
                            await player.stop()
                            await self.connect_to(voice_channel.guild.id, None)
                            LOGGER.info(f"{voice_channel} 음성채널에 봇만 남았으므로 자동 연결해제")
            except Exception as a:
                print(a)

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

    @commands.command(aliases=['join', '들어와', 'c', 'ㅊ', '연결'])
    async def connect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            #await self.connect_to(ctx.guild.id, ctx.author.voice.channel.id)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_connect_voice_channel"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        embed=discord.Embed(title=get_lan(ctx.author.id, "music_already_connected_voice_channel"), description='', color=self.normal_color)
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
                    embed=discord.Embed(title=get_lan(ctx.author.id, "music_can_not_find_anything"), description='', color=self.normal_color)
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
            embed.title = get_lan(ctx.author.id, "music_play_playlist")
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'

        else:
            track = results['tracks'][0]
            embed.title = get_lan(ctx.author.id, "music_play_music")
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            info = track['info']
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)
        embed.set_thumbnail(url="http://img.youtube.com/vi/%s/0.jpg" %(info['identifier']))
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.reply(embed=embed, mention_author=True)
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['리스트', '재생목록'])
    async def list(self, ctx, *, arg: str = None):
        anilistpath = "musicbot/anilist"

        # 파일 목록
        files = []
        for file in os.listdir(anilistpath):
            if file.endswith(".txt"):
                files.append(file.replace(".txt", ""))
        # 정렬
        file = sorted(files)
        # 재생목록 총 개수
        if arg == "-a":
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_len_list"), description=get_lan(ctx.author.id, "music_len_list").format(files_len=len(files)), color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        if arg is None:
            arg = 1

        try:
            arg1 = int(arg)

        # 리스트 재생
        except ValueError:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_list_finding"), color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            playmsg = await ctx.send(embed=embed)

            try:
                f = open(f"{anilistpath}/{arg}.txt", 'r')
                list_str = f.read()
                f.close()

            except Exception:
                embed=discord.Embed(title=get_lan(ctx.author.id, "music_list_can_not_find"), description=arg, color=self.normal_color)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await playmsg.edit(embed=embed)

            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            music_list = list_str.split('\n')
            passmusic = get_lan(ctx.author.id, "music_none")
            playmusic = get_lan(ctx.author.id, "music_none")
            trackcount = 0

            loading_dot_count = 0
            for music in music_list:
                if not music == "":
                    # ... 개수 변경
                    loading_dot = ""
                    loading_dot_count += 1
                    if loading_dot_count == 4:
                        loading_dot_count = 1
                    for a in range(0, loading_dot_count):
                        loading_dot = loading_dot + "."

                    embed=discord.Embed(title=get_lan(ctx.author.id, "music_adding_music").format(loading_dot=loading_dot), description=music, color=self.normal_color)
                    embed.set_footer(text=BOT_NAME_TAG_VER)
                    await playmsg.edit(embed=embed)

                    query = music.strip('<>')
                    if not url_rx.match(query):
                        query = f'ytsearch:{query}'

                    nofind = 0
                    while True:
                        results = await player.node.get_tracks(query)
                        if results['loadType'] == 'PLAYLIST_LOADED' or not results or not results['tracks']:
                            if nofind < 3:
                                nofind += 1
                            elif nofind == 3:
                                if passmusic == get_lan(ctx.author.id, "music_none"):
                                    passmusic = music
                                else:
                                    passmusic = f"{passmusic}\n{music}"
                        else:
                            break

                    track = results['tracks'][0]
                    if playmusic == get_lan(ctx.author.id, "music_none"):
                        playmusic = music
                    else:
                        playmusic = f"{playmusic}\n{music}"
                    if trackcount != 1:
                        info = track['info']
                        trackcount = 1
                    track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
                    player.add(requester=ctx.author.id, track=track)

            embed=discord.Embed(title=get_lan(ctx.author.id, "music_play_music"), description='', color=self.normal_color)
            embed.add_field(name=get_lan(ctx.author.id, "music_played_music"), value = playmusic, inline=False)
            embed.add_field(name=get_lan(ctx.author.id, "music_can_not_find_music"), value = passmusic, inline=False)
            embed.set_thumbnail(url="http://img.youtube.com/vi/%s/0.jpg" %(info['identifier']))
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await playmsg.edit(embed=embed)
            if not player.is_playing:
                await player.play()

        # 리스트 목록
        else:
            # 총 리스트 수가 10 이하일 경우
            if len(file) <= 10:
                embed=discord.Embed(title=get_lan(ctx.author.id, "music_playlist_list"), description="\n".join(file), color=color_code)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                return await playmsg.edit(embed=embed)

            # 총 페이지수 계산
            allpage = math.ceil(len(file) / 15)

            embeds = []
            chack = False
            for i in range(1, allpage+1):
                filelist = ""
                numb = (15 * i)
                numa = numb - 15
                for a in range(numa, numb):
                    try:
                        filelist = filelist + f"{file[a]}\n"
                    except IndexError:
                        break
                embed1 = discord.Embed(title=get_lan(ctx.author.id, "music_playlist_list"), description=filelist, color=color_code)
                embed1.set_footer(text=f"{get_lan(ctx.author.id, 'music_page')} {str(i)}/{str(allpage)}\n{BOT_NAME_TAG_VER}")
                if not chack:
                    msg = await ctx.send(embed=embed1)
                    chack = True
                embeds.append(embed1)

            page = Paginator(bot=self.bot, message=msg, embeds=embeds, use_extend=True)
            await page.start()

    @commands.command(aliases=['멜론재생', '멜론차트재생', '멜론음악', 'ㅁㅈ', 'aw'])
    async def melonplay(self, ctx, arg:int = None):
        if arg is None or arg > 10 or arg < 1:
            arg = 10
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        embed=discord.Embed(title=get_lan(ctx.author.id, "music_parsing_melon"), color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        melonplaymsg = await ctx.send(embed=embed)

        data = await getReqTEXT (self.melon_url, self.header)
        parse = BeautifulSoup(data, 'lxml')
        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        songs = parse.find_all("div", {"class": "ellipsis rank02"})
        title = []
        song = []
        for t in titles:
            title.append(t.find('a').text)
        for s in songs:
            song.append(s.find('span', {"class": "checkEllipsis"}).text)
        trackcount = 0
        passmusic = get_lan(ctx.author.id, "music_none")
        playmusic = get_lan(ctx.author.id, "music_none")
        loading_dot_count = 0
        for i in range(0, arg):
            # ... 개수 변경
            loading_dot = ""
            loading_dot_count += 1
            if loading_dot_count == 4:
                loading_dot_count = 1
            for a in range(0, loading_dot_count):
                loading_dot = loading_dot + "."
            musicname = str(f'{song[i]} {title[i]}')
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_adding_music").format(loading_dot=loading_dot), description=musicname, color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await melonplaymsg.edit(embed=embed)
            query = musicname.strip('<>')
            if not url_rx.match(query):
                query = f'ytsearch:{query}'

            nofind = 0
            while True:
                results = await player.node.get_tracks(query)
                if results['loadType'] == 'PLAYLIST_LOADED' or not results or not results['tracks']:
                    if nofind < 3:
                        nofind += 1
                    elif nofind == 3:
                        if passmusic == get_lan(ctx.author.id, "music_none"):
                            passmusic = musicname
                        else:
                            passmusic = "%s\n%s" %(passmusic, musicname)
                else:
                    break

            track = results['tracks'][0]
            if playmusic == get_lan(ctx.author.id, "music_none"):
                playmusic = musicname
            else:
                playmusic = "%s\n%s" %(playmusic, musicname)
            if trackcount != 1:
                info = track['info']
                trackcount = 1
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        embed=discord.Embed(title=get_lan(ctx.author.id, "music_melon_chart_play"), description='', color=self.normal_color)
        embed.add_field(name=get_lan(ctx.author.id, "music_played_music"), value = playmusic, inline=False)
        embed.add_field(name=get_lan(ctx.author.id, "music_can_not_find_music"), value = passmusic, inline=False)
        embed.set_thumbnail(url="http://img.youtube.com/vi/%s/0.jpg" %(info['identifier']))
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await melonplaymsg.edit(embed=embed)
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['빌보드재생', '빌보드차트재생', '빌보드음악', 'ㅂㅈ', 'qw'])
    async def billboardplay(self, ctx, arg:int = None):
        if arg is None or arg > 10 or arg < 1:
            arg = 10
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        embed=discord.Embed(title=get_lan(ctx.author.id, "misic_parsing_billboard"), color=self.normal_color)
        melonplaymsg = await ctx.send(embed=embed)

        data = await getReqTEXT (self.billboard_url, self.header)
        parse = BeautifulSoup(data, 'lxml')
        # 음악명
        titles = parse.find_all("span", {"class" : "chart-element__information__song text--truncate color--primary"})
        # 아티스트
        songs = parse.find_all("span", {"class" : "chart-element__information__artist text--truncate color--secondary"})
        title = []
        song = []
        for t in titles:
            title.append(t.get_text())
        for s in songs:
            song.append(s.get_text())
        trackcount = 0
        passmusic = get_lan(ctx.author.id, "music_none")
        playmusic = get_lan(ctx.author.id, "music_none")
        loading_dot_count = 0
        for i in range(0, arg) :
            # ... 개수 변경
            loading_dot = ""
            loading_dot_count += 1
            if loading_dot_count == 4:
                loading_dot_count = 1
            for a in range(0, loading_dot_count):
                loading_dot = loading_dot + "."
            musicname = str(f'{song[i]} {title[i]}')
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_adding_music").format(loading_dot=loading_dot), description=musicname, color=self.normal_color)
            await melonplaymsg.edit(embed=embed)
            query = musicname.strip('<>')
            if not url_rx.match(query):
                query = f'ytsearch:{query}'

            nofind = 0
            while True:
                results = await player.node.get_tracks(query)
                if results['loadType'] == 'PLAYLIST_LOADED' or not results or not results['tracks']:
                    if nofind < 3:
                        nofind += 1
                    elif nofind == 3:
                        if passmusic == get_lan(ctx.author.id, "music_none"):
                            passmusic = musicname
                        else:
                            passmusic = "%s\n%s" %(passmusic, musicname)
                else:
                    break

            track = results['tracks'][0]
            if playmusic == get_lan(ctx.author.id, "music_none"):
                playmusic = musicname
            else:
                playmusic = "%s\n%s" %(playmusic, musicname)
            if trackcount != 1:
                info = track['info']
                trackcount = 1
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        embed=discord.Embed(title=get_lan(ctx.author.id, "music_billboard_chart_play"), description='', color=self.normal_color)
        embed.add_field(name=get_lan(ctx.author.id, "music_played_music"), value = playmusic, inline=False)
        embed.add_field(name=get_lan(ctx.author.id, "music_can_not_find_music"), value = passmusic, inline=False)
        embed.set_thumbnail(url="http://img.youtube.com/vi/%s/0.jpg" %(info['identifier']))
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await melonplaymsg.edit(embed=embed)
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['탐색'])
    async def seek(self, ctx, *, seconds: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        track_time = player.position + (seconds * 1000)
        await player.seek(track_time)
        embed=discord.Embed(title=get_lan(ctx.author.id, "music_seek_move_to").format(move_time=lavalink.utils.format_time(track_time)), description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['forceskip', '스킵', 's', 'ㄴ'])
    async def skip(self, ctx, arg: int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_not_playing"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if arg is None:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_skip_next"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
            await player.skip()
        else:
            for i in range(arg):
                if not player.current:
                    arg=i
                    break
                await player.skip()
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_skip_many_music").format(music_count=arg), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

    @commands.command(aliases=['np', 'n', 'playing', '현재재생중', 'ㅜ', 'ㅞ', 'ㅜㅔ'])
    async def now(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.current:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_no_playing_music"), description='', color=self.normal_color)
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
                              title=get_lan(ctx.author.id, "music_now_playing"), description=song)
        embed.set_thumbnail(url="%s/0.jpg"%player.current.uri.replace('https://www.youtube.com/watch?v=', 'http://img.youtube.com/vi/'))
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['q', '큐', 'ㅂ'])
    async def queue(self, ctx, page: int = 1):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_no_music_in_the_playlist"), description='', color=self.normal_color)
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
                              description=get_lan(ctx.author.id, "music_no_music_in_the_playlist").format(lenQ=len(player.queue), queue_list=queue_list))
        embed.set_footer(text=f'{get_lan(ctx.author.id, "music_page")} {page}/{pages}\n{BOT_NAME_TAG_VER}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume', '일시정지', '일시중지', '재개'])
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_not_playing"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if player.paused:
            await player.set_pause(False)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_resume"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
        else:
            await player.set_pause(True)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_pause"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

    @commands.command(aliases=['vol', 'v', '볼륨', '음량', 'ㅍ'])
    async def volume(self, ctx, volume: int = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if volume is None:
            volicon = await volumeicon(player.volume)
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_pause").format(volicon=volicon, volume=player.volume), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if volume > 1000 or volume < 1:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_input_over_vol"), description=get_lan(ctx.author.id, "music_default_vol"), color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        await player.set_volume(volume)
        volicon = await volumeicon(player.volume)
        embed=discord.Embed(title=get_lan(ctx.author.id, "music_set_vol").format(volume=player.volume), description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['셔플'])
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_not_playing"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        player.shuffle = not player.shuffle
        if player.shuffle:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_shuffle_on"), description='', color=self.normal_color)
        else:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_shuffle_off"), description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['loop', 'l', '반복', 'ㅣ'])
    async def repeat(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_not_playing"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
            return
        player.repeat = not player.repeat
        if player.repeat:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_repeat_on"), description='', color=self.normal_color)
        else:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_repeat_off"), description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['제거', 'rm'])
    async def remove(self, ctx, index: int):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_remove_no_wating_music"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if index > len(player.queue) or index < 1:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_remove_input_over").format(last_queue=len(player.queue)), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        removed = player.queue.pop(index - 1)  # Account for 0-index.
        embed=discord.Embed(title=get_lan(ctx.author.id, "music_remove_form_playlist").format(remove_music=removed.title), description='', color=self.normal_color)
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
                    embed=discord.Embed(title=get_lan(ctx.author.id, "music_youtube_can_not_found"), description='', color=self.normal_color)
                    embed.set_footer(text=BOT_NAME_TAG_VER)
                    return await ctx.send(embed=embed)
            break
        tracks = results['tracks'][:10]  # First 10 results
        o = ''
        for index, track in enumerate(tracks, start=1):
            track_title = track['info']['title']
            track_uri = track['info']['uri']
            o += f'`{index}.` [{track_title}]({track_uri})\n'
        embed = discord.Embed(color=self.normal_color, title=get_lan(ctx.author.id, "music_youtube_result"), description=o)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(aliases=['dc', '연결해제', '나가', 'ㅇㅊ', '중지', '정지', 'stop'])
    async def disconnect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_dc_not_connect_voice_channel"), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            embed=discord.Embed(title=get_lan(ctx.author.id, "music_dc_not_connect_my_voice_channel").format(name=ctx.author.name), description='', color=self.normal_color)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)
        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)

        embed=discord.Embed(title=get_lan(ctx.author.id, "music_dc_disconnected"), description='', color=self.normal_color)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    async def ensure_voice(self, ctx):
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play', 'melonplay', 'billboardplay', 'connect', 'find', 'list')

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError(get_lan(ctx.author.id, "music_come_in_voice_channel"))
        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError(get_lan(ctx.author.id, "music_not_connected_voice_channel"))
            permissions = ctx.author.voice.channel.permissions_for(ctx.me)
            if not permissions.connect or not permissions.speak:
                raise commands.CommandInvokeError(get_lan(ctx.author.id, "music_no_permission"))
            player.store('channel', ctx.channel.id)
            player.fetch('channel')
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError(get_lan(ctx.author.id, "music_come_in_my_voice_channel"))

def setup(bot):
    bot.add_cog (Music (bot))
    LOGGER.info("Music loaded!")
