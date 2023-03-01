import discord
from discord.ext import commands
import os


intents = discord.Intents.default()
intents.members = True  # this allows the bot to receive member events
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready!')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command()
async def info(ctx, member: discord.Member):
    embed = discord.Embed(title=member.name, description=member.mention, color=discord.Color.blue())
    embed.add_field(name='ID', value=member.id, inline=False)
    embed.add_field(name='Status', value=member.status, inline=False)
    embed.add_field(name='Top Role', value=member.top_role.mention, inline=False)
    embed.add_field(name='Joined', value=member.joined_at.strftime('%d/%m/%Y %H:%M:%S'), inline=False)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)
    

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(title="User Kicked", description=f"{member} has been kicked.", color=0x00ff00)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="Error", description="I do not have the proper permissions to kick this user.", color=0xff0000)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Error", description=f"An error occurred: {e}", color=0xff0000)
        await ctx.send(embed=embed)

        
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(title="Ban Successful", description=f"{member} has been banned for {reason}", color=0x00ff00)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Error", description=str(e), color=0xff0000)
        await ctx.send(embed=embed)
   


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int, *, reason=None):
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        embed = discord.Embed(title="Unban", description=f"{user.name} ({user.id}) has been unbanned.", color=0x00ff00)
        await ctx.send(embed=embed)
    except discord.NotFound:
        embed = discord.Embed(title="Error", description=f"User with ID {user_id} not found.", color=0xff0000)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="Error", description="I do not have permission to unban users.", color=0xff0000)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Error", description=str(e), color=0xff0000)
        await ctx.send(embed=embed)

        
bot.run(os.environ.get("TOKEN"))
