import discord
from discord.ext import commands
from operator import itemgetter
import Loaders
import random
import asyncio


class TaylorBowl(commands.Cog):
    k = 4

    def __init__(self, client):
        self.votes = [0, 0]
        self.running = False
        self.client = client
        self.taylist = Loaders.csv_loader('./taysongs.csv')

    @commands.command(name='taylorbowl')
    async def taylor_bowl(self, ctx):
        """matches up two similarly-ranked Taylor songs, vote with a or b"""

        if self.running:
            return

        # Choose songs for bowl
        song_one_index = random.randrange(0, len(self.taylist))
        if song_one_index == len(self.taylist) - 1:
            song_two_index = song_one_index - 1
        elif song_one_index == 0:
            song_two_index = song_one_index + 1
        elif abs(self.taylist[song_one_index][1] - self.taylist[song_one_index - 1][1]) > abs(
                self.taylist[song_one_index][1] - self.taylist[song_one_index + 1][1]):
            song_two_index = song_one_index - 1
        else:
            song_two_index = song_one_index + 1

        # Create and send bowl
        tay_songs = discord.Embed()
        tay_songs.set_author(name=("%s started a new Taylor bowl!" % ctx.author.display_name), icon_url=ctx.author.avatar_url)
        tay_songs.title = 'TaylorBowl'
        tay_songs.description = "**A**: %s [%s]\n**B**: %s [%s]" % (
            self.taylist[song_one_index][0], self.taylist[song_one_index][1], self.taylist[song_two_index][0],
            self.taylist[song_two_index][1])

        # Begin bowl
        self.running = True
        print(self.running)
        poll = await ctx.channel.send(embed=tay_songs)
        await poll.add_reaction('🅰')
        await poll.add_reaction('🅱')
        await asyncio.sleep(20)
        # End bowl
        self.running = False

        # Create and send result of bowl
        cache_msg = discord.utils.get(self.client.cached_messages, id=poll.id)
        if cache_msg.reactions[0].count > cache_msg.reactions[1].count:
            description = "%s won!" % self.taylist[song_one_index][0]
            self.taylist[song_one_index][1] += TaylorBowl.k
            self.taylist[song_two_index][1] -= TaylorBowl.k
        elif cache_msg.reactions[1].count > cache_msg.reactions[0].count:
            description = "%s won!" % self.taylist[song_two_index][0]
            self.taylist[song_two_index][1] += TaylorBowl.k
            self.taylist[song_one_index][1] -= TaylorBowl.k
        else:
            description = 'Tie!'

        self.votes = [0, 0]

        tay_results = discord.Embed()
        tay_results.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        tay_results.title = 'TaylorBowl'
        tay_results.description = description
        await ctx.channel.send(embed=tay_results)

        self.taylist = sorted(self.taylist, key=itemgetter(1), reverse=True)
        Loaders.csv_writer('./taysongs.csv', self.taylist)


def k_value(x, y):
    if max(x, y) < 7:  # if the winner wins with less than 7 votes, kvalue is reduced
        return max(x, y) * 3
    else:  # kvalue is 50 unless "domination" happens
        return max(50, abs(x - y) * 7)


def setup(client):
    client.add_cog(TaylorBowl(client))
