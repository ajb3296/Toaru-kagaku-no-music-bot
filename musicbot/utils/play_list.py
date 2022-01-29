import re
import discord
import lavalink

from musicbot.utils.language import get_lan
from musicbot import color_code

url_rx = re.compile(r'https?://(?:www\.)?.+')

async def play_list(player, ctx, title, artist, playmsg):
    trackcount = 0
    playmusic = get_lan(ctx.author.id, "music_none")
    passmusic = get_lan(ctx.author.id, "music_none")
    loading_dot_count = 0
    for i in range(0, 10) :
        # ... 개수 변경
        loading_dot = ""
        loading_dot_count += 1
        if loading_dot_count == 4:
            loading_dot_count = 1
        for a in range(0, loading_dot_count):
            loading_dot = loading_dot + "."
        musicname = str(f'{artist[i]} {title[i]}')
        embed=discord.Embed(title=get_lan(ctx.author.id, "music_adding_music").format(loading_dot=loading_dot), description=musicname, color=color_code)
        await playmsg.edit_original_message(embed=embed)
        query = musicname
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
    return info, playmusic, passmusic