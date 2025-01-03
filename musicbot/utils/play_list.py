import re
import discord
from lavalink.server import LoadType

from musicbot.utils.language import get_lan
from musicbot.utils.statistics import Statistics
from musicbot import COLOR_CODE
url_rx = re.compile(r'https?://(?:www\.)?.+')


async def play_list(player, ctx, musics: list, playmsg):
    """ 음악 리스트의 음악 재생 """
    trackcount = 0
    playmusic = get_lan(ctx.author.id, "없음")
    passmusic = get_lan(ctx.author.id, "없음")
    loading_dot_count = 0
    thumbnail = None

    for music in musics:
        # ... 개수 변경
        loading_dot = ""
        loading_dot_count += 1
        if loading_dot_count >= 4:
            loading_dot_count = 1
        for _ in range(0, loading_dot_count):
            loading_dot = loading_dot + "."

        embed = discord.Embed(
            title=get_lan(ctx.author.id, "음악 추가중{loading_dot}").format(loading_dot=loading_dot),
            description=music,
            color=COLOR_CODE
        )
        await playmsg.edit(embed=embed)
        query = music
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        nofind = 0
        while True:
            results = await player.node.get_tracks(query)
            # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
            # ALternatively, results['tracks'] could be an empty array if the query yielded no tracks.
            if results.load_type == LoadType.EMPTY or not results or not results.tracks:
                if nofind < 3:
                    nofind += 1
                elif nofind == 3:
                    if passmusic == get_lan(ctx.author.id, "없음"):
                        passmusic = music
                    else:
                        passmusic = f"{passmusic}\n{music}"
            else:
                break

        track = results.tracks[0]

        # Music statistical
        Statistics().up(track.identifier)

        if playmusic == get_lan(ctx.author.id, "없음"):
            playmusic = music
        else:
            playmusic = f"{playmusic}\n{music}"
        if trackcount != 1:
            thumbnail = track.identifier
            trackcount = 1
        player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()
    return playmsg, player, thumbnail, playmusic, passmusic
