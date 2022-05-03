import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, word):
        await ctx.reply(word)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user:commands.MemberConverter, *, reason = None):
        await user.kick(reason = reason)
        await ctx.reply(f'{user} telah di kick, alasan: `{reason}`')

    @commands.command(aliases = ['clean', 'purge'])
    @commands.has_permissions(manage_messages=True) #Hanya user dengan role permission ini yang mampu menjalankan command.
    async def clear(self, ctx, amount:int = None):
        amount = amount or 5 #Jika tidak dispesifikasi berapa banyak pesan yang akan dihapus.
        if amount <= 0:
            return await ctx.reply("Tidak mampu menghapus 0 pesan.")
        await ctx.channel.purge(limit = amount+1)
        await ctx.send(f"{amount} pesan dari **`#{ctx.channel.name}`** telah dihapus.", delete_after = 5.0) #delete_after akan menghapus pesan konfirmasi bot setelah <float> detik.

def setup(bot):
    bot.add_cog(Moderation(bot))