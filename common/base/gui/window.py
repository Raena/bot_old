from common.abs.gui.window import AbstractWindow, AbstractWindowData
import discord


class WindowData(AbstractWindowData):

    def __init__(self, title: str, description: str, fields=None, emoji=[],
                 color: discord.colour.Colour = discord.colour.Color.magenta(), footer=None):
        self._emoji = emoji
        if footer is None:
            footer = {}
        if fields is None:
            fields = []
        self._description = description
        self._title = title
        self._fields = fields
        self._color = color
        self._footer = footer

    @property
    def reactions(self):
        return self._emoji

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def fields(self):
        return self._fields

    @property
    def color(self):
        return self._color

    @property
    def footer(self):
        return self._footer

    @title.setter
    def title(self, value: str):
        self._title = value

    @description.setter
    def description(self, value: str):
        self._description = value

    @fields.setter
    def fields(self, value: list):
        self._fields = value

    @color.setter
    def color(self, value: discord.colour.Colour):
        self._color = value

    @footer.setter
    def footer(self, value: dict):
        self._footer = value

    @reactions.setter
    def reactions(self, value: list):
        self._emoji = value


class Window(AbstractWindow):

    def __init__(self, window_data: AbstractWindowData):
        self.window_data = window_data
        self.is_sent = False
        self.message = None

    def generate_embed(self):
        embed = discord.embeds.Embed()
        embed.title = self.window_data.title
        embed.description = self.window_data.description
        if self.window_data.footer != {}:
            embed.set_footer(**self.window_data.footer)

        self._add_fields_to_embed(embed)

        return embed

    def _add_fields_to_embed(self, embed):
        for field in self.window_data.fields:
            if field is not None:
                embed.add_field(**field)

    async def send(self, channel: discord.abc.Messageable):
        embed = self.generate_embed()
        self.message = await channel.send(embed=embed)
        for emoji in self.window_data.reactions:
            await self.message.add_reaction(emoji=emoji)
        self.is_sent = True

    async def delete(self):
        if self.is_sent:
            await self.message.delete()
            self.is_sent = False

    async def update(self):
        await self.delete()
        await self.send(channel=self.message.channel)

    async def reaction(self, reaction):
        return reaction
