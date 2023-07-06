async def volumeicon(vol: int) -> str:
    vol_icon = ":loud_sound:"
    if 1 <= vol <= 10:
        vol_icon = ":mute:"
    elif 11 <= vol <= 30:
        vol_icon = ":speaker:"
    elif 31 <= vol <= 70:
        vol_icon = ":sound:"
    return vol_icon
