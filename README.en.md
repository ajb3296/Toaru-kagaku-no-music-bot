# Toaru-kagaku-no-music-bot

<a href="https://discord.gg/etzmFDGFVg"><img src="https://img.shields.io/discord/803935936219578368?color=7289da&logo=discord&logoColor=white" alt="Discord server" /></a>
<a href="https://discord.com/oauth2/authorize?client_id=714140461840728144&permissions=3165184&scope=bot"><img src="https://api.koreanbots.dev/widget/bots/servers/714140461840728144.svg" alt="Server count" /></a>
<a href="https://www.codefactor.io/repository/github/ajb3296/toaru-kagaku-no-music-bot"><img src="https://www.codefactor.io/repository/github/ajb3296/toaru-kagaku-no-music-bot/badge" alt="CodeFactor" /></a>

## Heroku Deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ajb3296/Toaru-kagaku-no-music-bot/tree/main)

## Note

[Lavalink Download](https://github.com/freyacodes/Lavalink/releases)<br>
[Lavalink Download(for arm or 32bit)](https://github.com/Cog-Creators/Lavalink-Jars/releases)

* This program follows [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html)

### Reference

* [lavalink.py](https://github.com/Devoxin/Lavalink.py)
* [EZPaginator](https://github.com/khk4912/EZPaginator)

## How to install

### How to use it with Heroku

1. Click the Heroku Deploy button above.
2. Set config
3. Deploy!

### How to use it as a computer

1. Create a `config.py` file in the `musicbot` folder.
2. Write the `config.py` file as follows.

```python
from musicbot.sample_config import Config

class Development(Config):
    TOKEN = 'token'
    OWNERS = [owners discord id(list)]
    DebugServer = [Debug server id]
    BOT_NAME = "bot name"
    BOT_TAG = "#bot tag"
    BOT_ID = bot_id
    AboutBot = f"""bot information"""

    # Music
    psw = "computer password"
```
You can create it by **referring** to `sample_config.py`.<br>
3. Run `python -m musicbot`

### Troubleshoot

If an SSL certificate-related problem occurs during parsing of the chart site :<br>

To do this you need to open up /etc/ssl/openssl.cnf and change `CipherString` from `DEFAULT@SECLEVEL=2` to `DEFAULT@SECLEVEL=1` Then you will have to reboot your system.<br>

Thanks to [KeonWoo PARK](https://github.com/parkkw472)