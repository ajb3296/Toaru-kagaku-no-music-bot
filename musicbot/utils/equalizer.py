import discord
from lavalink.filters import Equalizer as llEq

BAND_COUNT = 15


class Equalizer:
    __slots__ = ('_band_count', 'bands', 'freqs')

    def __init__(self):
        self._band_count = 15
        self.bands = [0.0 for x in range(self._band_count)]
        self.freqs = ('25', '40', '63', '100', '160', '250',
                      '400', '630', '1K', '1.6', '2.5', '4K',
                      '6.3', '10K', '16K')

    def set_gain(self, band: int, gain: float):
        if band < 0 or band >= self._band_count:
            raise IndexError(f'Band {band} does not exist!')

        gain = min(max(gain, -0.25), 1.0)

        self.bands[band] = gain

    def get_gain(self, band: int):
        if band < 0 or band >= self._band_count:
            raise IndexError(f'Band {band} does not exist!')

        return self.bands[band]

    def visualise(self):
        block = ''
        bands = [f'{self.freqs[band]:>3}' for band in range(self._band_count)]
        bottom = (' ' * 8) + ' '.join(bands)

        gains = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1, -0.2, -0.25]

        for gain in gains:
            prefix = ' '

            if gain > 0:
                prefix = '+'
            elif gain == 0:
                prefix = ' '
            else:
                prefix = ''

            block += f'{prefix}{gain:.2f} | '

            for value in self.bands:
                if value >= gain:
                    block += '■■■ '
                else:
                    block += '    '

            block += '\n'

        block += bottom
        return block

class EqualizerButton(discord.ui.View):
    def __init__(self, ctx, player, eq, selected):
        super().__init__()
        self.ctx = ctx
        self.player = player
        self.eq = eq
        self.selected = selected

    @discord.ui.button(label="", row=0, style=discord.ButtonStyle.primary, emoji="⬅")
    async def left(self, button, interaction):
        self.selected = max(self.selected - 1, 0)
        result = await self.button_interact()
        await interaction.response.edit_message(content=result)

    @discord.ui.button(label="", row=0, style=discord.ButtonStyle.primary, emoji="➡")
    async def right(self, button, interaction):
        self.selected = min(self.selected + 1, 14)
        result = await self.button_interact()
        await interaction.response.edit_message(content=result)

    @discord.ui.button(label="", row=0, style=discord.ButtonStyle.primary, emoji="⬆")
    async def up(self, button, interaction):

        gain = min(self.eq.get_gain(self.selected) + 0.1, 1.0)
        self.eq.set_gain(self.selected, gain)
        await self.apply_gains(self.player, self.eq.bands)
        result = await self.button_interact()

        await interaction.response.edit_message(content=result)

    @discord.ui.button(label="", row=0, style=discord.ButtonStyle.primary, emoji="⬇")
    async def down(self, button, interaction):

        gain = max(self.eq.get_gain(self.selected) - 0.1, -0.25)
        self.eq.set_gain(self.selected, gain)
        await self.apply_gains(self.player, self.eq.bands)
        result = await self.button_interact()

        await interaction.response.edit_message(content=result)

    @discord.ui.button(label="", row=0, style=discord.ButtonStyle.danger, emoji="🔄")
    async def reset(self, button, interaction):
        for band in range(self.eq._band_count):
            self.eq.set_gain(band, 0.0)

        await self.apply_gains(self.player, self.eq.bands)

        result = await self.button_interact()

        await interaction.response.edit_message(content=result)

    async def button_interact(self):
        self.player.store('eq', self.eq)
        selector = f'{" " * 8}{"    " * self.selected}^^^'
        return f"```diff\n{self.eq.visualise()}\n{selector}```"

    async def apply_gains(self, player, gains):
        if isinstance(gains, list):
            e = llEq()
            e.update(bands=[(x, y) for x, y in enumerate(gains)])
            await player.set_filter(e)
        elif isinstance(gains, dict):
            await player.set_gain(gains['band'], gains['gain'])

        await player._apply_filters()