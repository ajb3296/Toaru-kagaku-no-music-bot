import re
import discord
import lavalink

from musicbot.utils.language import get_lan
from musicbot.utils.statistics import Statistics
from musicbot import color_code

url_rx = re.compile(r'https?://(?:www\.)?.+')

async def play_list(player, ctx, musics, playmsg):
    trackcount = 0
    playmusic = get_lan(ctx.author.id, "music_none")
    passmusic = get_lan(ctx.author.id, "music_none")
    loading_dot_count = 0

    for music in musics:
        # ... 개수 변경
        loading_dot = ""
        loading_dot_count += 1
        if loading_dot_count == 4:
            loading_dot_count = 1
        for a in range(0, loading_dot_count):
            loading_dot = loading_dot + "."

        embed=discord.Embed(title=get_lan(ctx.author.id, "music_adding_music").format(loading_dot=loading_dot), description=musics[i], color=color_code)
        await playmsg.edit(embed=embed)
        query = music
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
                        passmusic = "%s\n%s" %(passmusic, i)
            else:
                break
        track = results['tracks'][0]

        # Music statistical
        Statistics.up(track['info']['identifier'])

        if playmusic == get_lan(ctx.author.id, "music_none"):
            playmusic = music
        else:
            playmusic = "%s\n%s" %(playmusic, music)
        if trackcount != 1:
            info = track['info']
            trackcount = 1
        track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
        player.add(requester=ctx.author.id, track=track)
    return playmsg, player, info, playmusic, passmusic