import datetime
import json
from typing import Literal
import pytz
import sqlite3

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]
urlToDB = "Cards.db"


class LoR(commands.Cog):
    """
    With LoR commands you can search for Legends of Runterra cards and their art. You can also get all sorts of info on
    Keywords or Vocab Terms via the info command. Have fun!
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=LoR,
            force_registration=True,
        )

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)


    @commands.command(aliases = ["lorcard"])
    async def card(self, ctx, *, cardSearchName):
        """Searched the card and displays all matches. For champions their tier 1, 2 and spell are displayed"""

        connection = sqlite3.connect(urlToDB)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from cards WHERE name like '%{cardSearchName}%'")
        results = cursor.fetchall()

        for currentcard in results:
            cardName = currentcard[0]
            cardCode = currentcard[3]
            flavorText = currentcard[2]
            cardGameAbsolutePath = currentcard[6]
            await ctx.send(embed=embedCard(cardName, cardCode, flavorText, cardGameAbsolutePath))

        if len(results) == 0:
            embed = discord.Embed(title=f"{cardSearchName}", colour=discord.Colour(2123412),
                                  url=f"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                                  description=f"No cards found with this name")
            await ctx.send(embed=embed)
        connection.close()

    @commands.command(aliases = ["lorart", "lorcardart", "cardart"])
    async def cardArt(self, ctx, *, cardSearchName):
        """Searched the card art and displays all matches. For champions their tier 1, 2 and spell are displayed"""

        connection = sqlite3.connect(urlToDB)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from cards WHERE name like '%{cardSearchName}%'")
        results = cursor.fetchall()

        for currentcard in results:
            cardName = currentcard[0]
            cardCode = currentcard[3]
            flavorText = currentcard[2]
            fullGameAbsolutePath = currentcard[5]
            await ctx.send(embed=embedCardArt(cardName, cardCode, flavorText, fullGameAbsolutePath))

        if len(results) == 0:
            embed = discord.Embed(title=f"{cardSearchName}", colour=discord.Colour(2123412),
                                  url=f"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                                  description=f"No cards found with this name")
            await ctx.send(embed=embed)
        connection.close()

    @commands.command(aliases = ["lorinfo", "vocab", "keyword"])
    async def cardInfo(self, ctx, *, cardSearchTerm):
        """With this command you can search for card terms such as the keywords or vocab terms"""

        connection = sqlite3.connect(urlToDB)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * from misc WHERE name like '%{cardSearchTerm}%'")
        results = cursor.fetchall()

        for currentcard in results:
            cardName = currentcard[0]
            description = currentcard[1]

            await ctx.send(embed=embedInfo(cardName, description))

        if len(results) == 0:
            embed = discord.Embed(title=f"{cardSearchTerm}", colour=discord.Colour(2123412),
                                  url=f"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                                  description=f"No terms found with this name")
            await ctx.send(embed=embed)
        connection.close()


def embedCard(cardName, cardCode, flavorText, cardGameAbsolutePath):

    embed = discord.Embed(title=f"{cardName}", colour=discord.Colour(0xa7f8f3),
                          url=f"https://lor.mobalytics.gg/cards/{cardCode}",
                          description=f"{flavorText}",
                          timestamp=datetime.datetime.now(pytz.UTC))

    embed.set_image(url=f"{cardGameAbsolutePath}")
    embed.set_footer(text="ANGRYBACTERIA")
    # embed.add_field(name="to be done", value="to be done")
    return embed

def embedCardArt(cardName, cardCode, flavorText, cardFullAbsolutePath):

    embed = discord.Embed(title=f"{cardName}", colour=discord.Colour(0xa7f8f3),
                          url=f"https://lor.mobalytics.gg/cards/{cardCode}",
                          description=f"{flavorText}",
                          timestamp=datetime.datetime.now(pytz.UTC))

    embed.set_image(url=f"{cardFullAbsolutePath}")
    embed.set_footer(text="ANGRYBACTERIA")
    # embed.add_field(name="to be done", value="to be done")
    return embed

def embedInfo(name, description):

    embed = discord.Embed(title=f"{name}", colour=discord.Colour(0xeb900),
                          description=f"{description}",
                          timestamp=datetime.datetime.now(pytz.UTC))

    #embed.set_image(url=f"{cardGameAbsolutePath}")
    embed.set_footer(text="ANGRYBACTERIA")
    return embed


class Card:
  def __init__(self, name, description, set, absolutePath, cardCode, loreText, fullAbsolutePath):
    self.name = name
    self.description = description
    self.set = set
    self.absolutePath = absolutePath
    self.cardCode = cardCode
    self.loreText = loreText
    self.fullAbsolutePath = fullAbsolutePath


