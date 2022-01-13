import discord 
from discord.ext import commands
from discord import message
from discord import channel
from discord import emoji
from itertools import permutations
from discord_components import DiscordComponents, Button, ButtonStyle
from discord import utils
import string
from discord.member import Member
import asyncio
import io
import datetime
import requests
from PIL import Image, ImageFont, ImageDraw



bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

@bot.command()
async def button(ctx):  
    await ctx.send(
        embed=discord.Embed(title="Наш Tik-Tok (Beta)"),
        components=[
            Button(style=ButtonStyle.green, label="Разрешить", emoji="✨"),
            Button(style=ButtonStyle.red, label="Запретить", emoji="🧨"),
            Button(style=ButtonStyle.URL, label="TikTok", url="https://tiktok.com/@_donyshky_")
        ]
    )

    response = await bot.wait_for("button_click")
    if response.channel == ctx.channel:
        if response.component.label == "Разрешить":
            await response.respond(content="Круто! :3")
        else:
            await response.respond(
                embed=discord.Embed(title="Ты уверен?"),
                components = [
                    Button(style=ButtonStyle.green, label="Да"),
                    Button(style=ButtonStyle.red, label="Нет"),
                    Button(style=ButtonStyle.blue, label="Я подумаю...", emoji="🙄")
                ]
            )

@bot.event
async def on_ready():	
    while True:
            delta = datetime.timedelta(hours=3)
            tz = datetime.timezone(delta)
            #dt = datetime.datetime.now(tz=tz).time().hour + ':' + str(datetime.datetime.now().time().minute)
            time = str(datetime.datetime.now(tz=tz).time().hour) + ':' + str(datetime.datetime.now().time().minute)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(f".help | _MultiBot_ | Сейчас {time} по Мск!"))

#@bot.event
#async def on_command_error(ctx, error):
			#pass	

@bot.command() 
@commands.has_any_role(930554558315397130) 
async def kick(ctx, member: discord.Member):
    embed=discord.Embed(title=ctx.member.name, colour=discord.Colour.red()) 
    embed.add_field(name=f'Пользоваталь был выгнан!', inline=False) 
    embed.add_field(name='Модератор: {ctx.author.name}' , inline=False) 
    embed.add_field(name='Нарушитель: {member.name}' , inline=False) 
    
    await ctx.send(embed=embed) 
    await ctx.add_reaction("✔️") 

@kick.error
async def kick_error(ctx, error):
    if isinstance( error, commands.MissingRequiredArgument):
        await ctx.send(embed = discord.Embed(title='{0}'.format(ctx.author.name), description='Команда введена не правильно! \n Введите по образцу: .kick @member :3', color=discord.Colour.red())) 

			
@bot.command()
async def help(ctx):
	embed=discord.Embed(title='Список команд',colour=discord.Colour.red())
	
	embed.add_field(name='.activity', value='Изменить активность бота')
	
	await ctx.send(embed=embed)
	
@bot.command() 
async def activity(ctx, arg=None):
    if arg == None:
        embed = discord.Embed(title='Активнось', color = discord.Color.green()) 
        embed.add_field(name='Активность: Онлайн', value='.activity online', inline=False) 
        embed.add_field(name='Активность: Спит',value='.activity idle', inline=False) 
        embed.add_field(name='Активность: Не беспокоить!',value='.activity dnd', inline=False) 
        await ctx.send(embed=embed) 
    if arg == 'online':
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(f".help | _MultiBot_ | _MultiBot_ | {time}")) 
        await ctx.send(embed=discord.Embed(title=f'Устанослена активность: Онлайн!', color=discord.Color.green())) 
    if arg == 'idle':
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(f".help | _MultiBot_ | _MultiBot_ | {time}")) 
        await ctx.send(embed=discord.Embed(title=f'Устанослена активность: Спит!', color=discord.Color.green())) 
    if arg == 'dnd':
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(f".help | _MultiBot_ | _MultiBot_ | {time}")) 
        await ctx.send(embed=discord.Embed(title=f'Устанослена активность: Не беспокоить!', color=discord.Color.green())) 

@bot.event
async def on_member_join(member):
	channel = bot.get_channel(929692687551037441)
	role = discord.utils.get(member.message.guild.roles, id = 928931558566543430)
	
	await member.add_roles(role)
	await channel.send(discord.Embed(description=f'Пользователь ``{member.name}``, присоеденился!',  color = 0x3ec95d))

@bot.command()
async def test(ctx):
    await ctx.send(
        embed = discord.Embed(title = 'Вы точно хотите перевевсти деньги?', timestamp = ctx.message.created_at),
        components = [
            Button(style = ButtonStyle.green, label = 'Да'),
            Button(style = ButtonStyle.red, label = 'Нет')
        ])
    responce = await bot.wait_for('button_click', check = lambda message: message.author == ctx.author)
    if responce.component.label == 'Да':
        await responce.respond(content = 'Деньги успешно переведены!')
    else:
        await responce.respond(content = 'Вы отменили перевод.')

@bot.command()
@commands.has_any_role(929164644579409952)
async def clear(ctx, amount : int):
	await ctx.channel.purge(limit=amount)

	await ctx.send(discord.Embed( description=f'Успешно очищено {amount}  сообщений', colour=discord.Colour.green()))

@clear.error
async def clear_error( ctx, error):
    if isinstance( error, commands.MissingRequiredArgument):
        await ctx.send(embed = discord.Embed(title='{0}'.format(ctx.author.name), description=' Укажите количество слов! :3', color=discord.Colour.red())) 

@bot.command()
async def cart(ctx):
    img = Image.new('RGBA', (400, 200), '#232529')
    url = str(ctx.author.avatar_url)[:-10]

    response = requests.get(url, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)

    img.paste(response, (15, 15, 115, 115))

    idraw = ImageDraw.Draw(img)
    name = ctx.author.name
    tag = ctx.author.discriminator


    headline = ImageFont.truetype('arial.ttf', size = 20)
    undertext = ImageFont.truetype('arial.ttf', size = 12)

    idraw.text((145, 15), f'{name}#{tag}', font = headline)
    idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)

    img.save('card//user_card.png')

    await ctx.send(file = discord.File(fp = 'card//user_card.png'))

@bot.command()
@commands.has_any_role(929881303116021822)
async def admin(ctx):
    embed = discord.Embed(title='Панель администратора', color=discord.Colour.blue())

    embed.add_field(name=".ban @ник причина(не обязательно)", value="Блокирует участнику достпуп к серверу!")
		
    await ctx.send(embed=embed)
	
@admin.error
async def admin_error( ctx, error ):	
    if isinstance( error, commands.MissingPermissions):
        await ctx.send(discord.Embed(title={ctx.author.name}, description=f' У вас недостаточно прав! :3', color=discord.Colour.red())) 


	
bot.run("OTI5ODQ0NDgxMzYzMTY1MTg0.YdtPKA.fSEpeNb8v0nHHE4L7n0k89pT7bk") 
