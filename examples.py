import discord
from discord.ext import commands, tasks
from discord import client
from discord.utils import get
import random
from discord import Embed
import googletrans
from googletrans import Translator
from random import choice
import discord.utils
import json
import requests
import wikipedia
#googletrans==3.1.0a0 (per far funzionare il plugin è necessaria questa versione di googletrans (versioni più aggiornate non funzioneranno))

#tutti questi moduli servono per creare il bot. Come primo passaggio è necessario scaricare questi moduli

print('Il bot è in fase di avvio...')
client = commands.Bot(command_prefix="$")
#il prefisso rappresenta ciò che utilizzeremo per invocare il bot, è necessario salvare questo prefisso per interagire con i vari comandi
token = 'SECRET'
#il token è una stringa di lettere e numeri reperibili una volta creato il bot. Per creare un bot vai qui: https://discord.com/developers/applications e crea prima una nuova applicazione e poi il bot legato all'applicazione
status = ['Digita $help per i comandi', 'Sto riposando']
#status del bot; potete creare il vostro status personalizzato scrivendo ad esempio come raggiungere il comando di aiuto (che cambia ogni 15 secondi)


@client.event
async def on_ready():
    change_status.start()
    print(client.user, "è finalmente online ")
    
    
@tasks.loop(seconds=15)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))
#tramite questo loop facciamo cambiare ogni 15 secondi lo stato del bot (sotto al nome del bot apparirà alternativamente uno degli stati creati nella variabile status)


@client.command(name='ping', help='Comando per la latenza del bot')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')
#esempio basico di un comando sfruttando la sintassi con async e await
#potete utilizzare il seguente link: https://discordpy.readthedocs.io/en/latest/index.html per imparare le basi di Discord.py


@client.command(name='kick', help='Espelli un membro')
async def kick(ctx, member: discord.Member, *, reason=None):
    if (ctx.message.author.permissions_in(ctx.message.channel).kick_members):
        await member.kick(reason=reason)
    else:
        await ctx.send('Non hai i permessi per usare questo comando')
#questo comando permette di espellere un utente. Procedendo con ordine nelle prime due righe si da il nome al comando e gli si da una piccola descrizione che compare nel comando di aiuto generale (nel mio caso $help)
#la prima condizione controlla che l'autore del messaggio abbia come permesso su Discord quello di espellere i membri. Se effettivamente ha quel permesso il bot andrà ad espellere il membro
#nel caso in cui l'autore del messaggio non abbia i permessi il bot restituirà il messaggio 'Non hai i permessi per usare questo comando'


@client.command(name='ban', help='Banna un membro')
async def ban(ctx, member: discord.Member, *, reason=None):
    if (ctx.message.author.permissions_in(ctx.message.channel).ban_members):
        await member.ban(reason=reason)
    else:
        await ctx.send('Non hai i permessi per usare questo comando')


@client.command(name='clear', help='Cancella dei messaggi')
async def clear(ctx, amount=2):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send('Non hai i permessi per usare questo comando')
#il comando ban e il comando clear sono molto simili al comando kick. Variano principalmente i permessi ma la struttura è identica


client.command(name='help_moderazione', help='Mostra informazioni per comandi di moderazione')
async def help_moderazione(ctx):
  await ctx.send('**Ecco il pannello di aiuto per la moderazione**!\n Per bannare un utente digita $ban @user (funziona solo con il ban_permission).\n Per espellere un utente digita $kick @user (funziona solo con il kick permission).\n Per cancellare dei messaggi digita $clear numero (al posto di numero digita il numero di messaggi, funziona solo con il manage_messages). \n Digita $help_automoderatore per vedere informazioni riguardo alla funzione di automoderazione. \n Per warnare un utente digita $warn @user motivo (funziona solo con il manage_roles). \n Digita $userwarn @user per controllare i warn di un utente (funziona solo con il manage_roles).')


@client.command(name='serverinfo', help='Info riguardanti il server')
async def serverinfo(ctx):
    title = ctx.guild.name
    region = ctx.guild.region
    member = ctx.guild.member_count
    idguild = ctx.guild.id
    icona = ctx.guild.icon_url
    owner = ctx.guild.owner_id
    embed = discord.Embed(title='**Info del server**', color=discord.Color.green())
    embed.add_field(name='**Nome del server**:', value=title)
    embed.add_field(name='**Regione del server**:', value=region)
    embed.add_field(name='**ID del server**:', value=idguild)
    embed.add_field(name='**Owner id**: ', value=owner)
    embed.add_field(name='**Numero di membri del server**:', value=member)

    embed.set_thumbnail(url=icona)
    await ctx.send(embed=embed)
#questo comando è molto particolare. Permette di ottenere informazioni riguardo al serverr in cui ci si trova. Per creare comandi simili basta guardare la documentazione ufficiale di Discord.py
#il comando sfrutta gli embed di Discord per dare la risposta (An Embed object is another component of Discord messages that can be used to present data with special formatting and structure.)


@client.command(name='userinfo', help='Ottieni informazioni riguardo ad un membro')
async def userinfo(ctx, member: discord.Member):
    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)

    embed.add_field(name='Id', value=member.id)
    embed.add_field(name='Is bot?', value=member.bot)
    roles = [role for role in member.roles]
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))

    await ctx.send(embed=embed)
#comando simile al precedente che restituisce informazioni su un utente


@client.command(name='translate', help='Per tradurre scrivi $translate lang Parola')
async def translate(ctx, lang, *, args):
    tran = Translator()
    result = tran.translate(args, dest=lang)
    await ctx.send(result.text)
#comando molto semplice per tradurre parole o frasi sfruttando il modulo googletrans (che si installa con pip install googletrans==3.1.0a0) 
#Consulta https://py-googletrans.readthedocs.io/en/latest/ per la lista di lingue disponibili e per la documentazione ufficiale


@client.command(name='votazione', help='Esegue una votazione tramite le reazioni')
async def votazione(ctx, *, arg):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await ctx.channel.purge(limit=1)
        titolo_votazione = '**Nuova votazione**! *Usa le reazioni per votare*.'
        descrizione = '**Votazione di**: ' + str(ctx.author.mention) + '**Ecco il messaggio**: ' + arg
        embed = discord.Embed(title=titolo_votazione, description=descrizione, color=discord.Color.blue())
        embed_message = await ctx.send(embed=embed)
        await embed_message.add_reaction("✅")
        await embed_message.add_reaction("❌")
    else:
        await ctx.send('Per eseguire votazioni devi avere il permesso: manage_messages')
#comando semplice per creare votazioni (può essere creato anche senza la funzione che cancella automaticamente il messaggio dell'utente, in modo da togliere la condizione che controlla i permessi)
#per eseguire una votazione digita $votazione MESSAGGIO, ad esempio $votazione Mangiamo la pizza. Per usare questo comando il bot e l'autore del comando devono avere il permesso manage_messages.

OWNER_ID = your_discord_id
@client.command(name='spegnimento', help='Comando riservato')
async def spegnimento(ctx):
  if ctx.author.id ==OWNER_ID:
    await ctx.send('**Bot in spegnimento**...Bye bye. *Per riattivare il bot aprire il server e aggiornare i plugin necessari* (googletrans==3.1.0a0')
    await client.logout()
    await client.close()
  else:
    await ctx.send("Comando riservato all'Owner del bot")
#questo comando permette di spegnere il bot (se hostato) direttamente da Discord. Per evitare che lo usino tutti, il comando funziona solo se l'autore del messaggio è il creatore del bot
#per fare ciò basta creare una variabile in cui si inserisce il proprio id, se l'id dell'autore del messaggio coincide con l'id salvato nella variabile allora il bot esegue il comando
#utile per creare un sistema di blacklist


@client.command(name='addizione', help='Svolge una somma fra due numeri')
async def addizione(ctx, arg1:float, *, arg2:float):
  risultato = str(arg1 + arg2)
  await ctx.send('*Il risultato è* ' + risultato)


@client.command(name='sottrazione', help='Svolge una differenza fra due numeri')
async def sottrazione(ctx, arg1:float, *, arg2:float):
  risultato = str(arg1 - arg2)
  await ctx.send('*Il risultato è* ' + risultato)


@client.command(name='moltiplicazione', help='Svolge una moltiplicazione fra due numeri')
async def moltiplicazione(ctx, arg1:float, *, arg2:float):
  risultato = str(arg1 * arg2)
  await ctx.send('*Il risultato è* ' + risultato)


@client.command(name='divisione', help='Svolge una divisione fra due numeri')
async def divisione(ctx, arg1:float, *, arg2:float):
  risultato = str(arg1 / arg2)
  await ctx.send('*Il risultato è* ' + risultato)
#lista di semplicissimi comandi per eseguire operazioni (non è necessaria spiegazione)
#per eseguire una somma digita $addizione numero1 numero2 ($addizione 5 6) per le altre operazioni sostituisci a addizione la parola sottrazione, moltiplicazione o divisione.


@client.command(name='meteo', help='Previsioni meteo per una località')
async def meteo(ctx, *, args):
    api = 'http://api.openweathermap.org/data/2.5/weather?appid=YOURAPPID='
    city = str(args)
    url = api + city + '&units=metric'
    dati = requests.get(url).json()
    risultato = dati['weather'][0]['description']
    risultato1 = dati['main']['temp']
    tran = Translator()
    result = tran.translate(risultato, dest='it')
    await ctx.send('**Descrizione**: ' + str(result.text) + ' **Temperatura**: ' + str(risultato1))
#comando per ricevere previsioni meteo direttamente su Discord. Per utilizzare questo comando è necessario utilizzare un api di openweathermap
#https://openweathermap.org/api
#il risultato è in inglese ma fondendo all'interno il comando per la traduzione è possibile restituire il meteo già tradotto automaticamente dal bot


@client.command(name='wiki', help='Fa una ricerca su Wikipedia')
async def wiki(ctx, *, args):
    ricerca = str(args)
    await ctx.send(wikipedia.page(ricerca).title)
    await ctx.send(wikipedia.summary((ricerca), sentences=5))
#semplice comando per fare ricerche su Wikipedia (restituisce il risultato in inglese essendo un modulo inglese)
#è possibile far tradurre al bot il risultato automaticamente prima di inviarlo èrendendo spunto dal comando sopra

#è molto semplice creare altri comandi anche vocali per permettere al bot di entrare in una vocale e riprodurre ad esempio musica. Questi sono solo semplici esempi di comandi
#tutto è realizzabile leggendo i docs dei moduli utilizzati
#ovviamente è necessario munirsi del proprio token per far funzionare il codice

client.run(token)
