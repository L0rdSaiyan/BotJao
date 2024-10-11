# @Author Victor Sales
#
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio

# CONFIGURAÇÃO DE PERMISSÕES
permissions = discord.Intents.default()
permissions.message_content = True
permissions.members = True
permissions.reactions = True 

bot = commands.Bot(command_prefix='.jao ', intents=permissions)

cafe_reacoes = {}
jaoChannelId = '711956562306007124'  # ID do canal 'geral'

# Função para calcular o tempo até quarta-feira às 16:00
def segundos_ate_quarta_16():
    now = datetime.now()
    futuro = datetime.combine(now, datetime.min.time()) + timedelta((2 - now.weekday()) % 7, hours=16)
    
    if now > futuro:
        futuro += timedelta(weeks=1)
    
    return (futuro - now).total_seconds()

# Evento para quando o bot estiver online
@bot.event
async def on_ready():
    print('Bot online')
    bot.loop.create_task(semana_praticamente_encerrada())
    sextou.start()

# Tarefa para enviar mensagem semanalmente às quartas-feiras às 16:00
async def semana_praticamente_encerrada():
    while True:
        segundos_espera = segundos_ate_quarta_16()
        await asyncio.sleep(segundos_espera)
        canal = bot.get_channel(int(jaoChannelId))  # Usando o ID do canal
        if canal:
            await canal.send("https://www.youtube.com/watch?v=Tmy5JtL58dE")
        await asyncio.sleep(60)  

@tasks.loop(minutes=1)
async def sextou():
    now = datetime.now()
    hora_minutos = now.strftime("%H:%M")
    dia_semana = now.weekday()

    if dia_semana == 4 and hora_minutos == "17:00":
       canal = bot.get_channel(int(jaoChannelId))  # Usando o ID do canal
       if canal:
           await canal.send('SEXTOU PROS ESTAGS!')

# Comando para o bot repetir uma frase especificada pelo usuário
@bot.command()
async def falar(ctx: commands.Context, *, frase):
    await ctx.send(frase)

# Comando para envio de café
@bot.command()
async def cafe(ctx: commands.Context):
    channel = ctx.channel.name
    if channel != 'geral':
        return

    # Envia a mensagem de café e armazena o ID da mensagem em cafe_reacoes
    message = await ctx.send('Cafézin?')
    await message.add_reaction('☕')
    cafe_reacoes[message.id] = set()  # Inicia um conjunto vazio para a nova mensagem

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == bot.user and user != bot.user:
        if reaction.message.id in cafe_reacoes:
            if user.id not in cafe_reacoes[reaction.message.id]:
                cafe_reacoes[reaction.message.id].add(user.id)
                await reaction.message.channel.send(f'{user.mention} café {reaction.emoji}!')
            else:
                await reaction.remove(user)  

@bot.command()
async def mopa(ctx:commands.Context):
    await ctx.reply('eu sei que você quer o que eu tenho aqui em baixo renanzinho')

# Comando para o bot entrar no canal de voz do usuário
@bot.command(pass_context=True)
async def entrar(ctx: commands.Context):
    user = ctx.message.author
    if user.voice:
        channel = user.voice.channel
        await channel.connect()
        await ctx.send(f'Conectado ao canal de voz: {channel.name}')
    else:
        await ctx.send('Você precisa estar em um canal de voz para usar esse comando.')

bot.run('')
