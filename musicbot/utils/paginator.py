import discord
from typing import List
from discord.ui import View, Button

class Paginator(View):
    def __init__(self, embeds: List[discord.Embed], timeout: int = 180):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.current_page = 0

        # Add buttons
        self.first_page_button = Button(emoji="⏮️", style=discord.ButtonStyle.grey)
        self.prev_page_button = Button(emoji="◀️", style=discord.ButtonStyle.blurple)
        self.next_page_button = Button(emoji="▶️", style=discord.ButtonStyle.blurple)
        self.last_page_button = Button(emoji="⏭️", style=discord.ButtonStyle.grey)

        self.first_page_button.callback = self.first_page
        self.prev_page_button.callback = self.prev_page
        self.next_page_button.callback = self.next_page
        self.last_page_button.callback = self.last_page

        self.add_item(self.first_page_button)
        self.add_item(self.prev_page_button)
        self.add_item(self.next_page_button)
        self.add_item(self.last_page_button)

        self.update_buttons()

    def update_buttons(self):
        """Update button states based on current page"""
        self.first_page_button.disabled = self.current_page == 0
        self.prev_page_button.disabled = self.current_page == 0
        self.next_page_button.disabled = self.current_page == len(self.embeds) - 1
        self.last_page_button.disabled = self.current_page == len(self.embeds) - 1

    async def update_message(self, interaction: discord.Interaction):
        """Update the message with the current page"""
        self.update_buttons()
        await interaction.response.edit_message(
            embed=self.embeds[self.current_page],
            view=self
        )

    async def first_page(self, interaction: discord.Interaction):
        self.current_page = 0
        await self.update_message(interaction)

    async def prev_page(self, interaction: discord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_message(interaction)

    async def next_page(self, interaction: discord.Interaction):
        if self.current_page < len(self.embeds) - 1:
            self.current_page += 1
            await self.update_message(interaction)

    async def last_page(self, interaction: discord.Interaction):
        self.current_page = len(self.embeds) - 1
        await self.update_message(interaction)

    async def on_timeout(self):
        """Called when the view times out"""
        for item in self.children:
            item.disabled = True

        # Try to edit the message if it still exists
        try:
            await self.message.edit(view=self)
        except discord.NotFound:
            pass