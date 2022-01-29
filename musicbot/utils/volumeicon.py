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