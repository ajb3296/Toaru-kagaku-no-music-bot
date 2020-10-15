import datetime
import discord
from musicbot import BOT_NAME_TAG_VER

def footer (embed) :
   embed.timestamp = datetime.datetime.utcnow()
   embed.set_footer(text = BOT_NAME_TAG_VER)