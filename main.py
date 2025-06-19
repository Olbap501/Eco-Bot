import discord, os, speech
import datetime
import random
import sqlite3
from retos import challenges
from discord.ext import commands
from dotenv import load_dotenv
from cubos_reciclar import cubos
from dato_reciclaje import dato
from tip_reciclaje import tip
from calcular_huella import calcular
from tip_agua import water_tip
from database_setup import init_db


load_dotenv()
token = os.getenv("dt")



# Configurar intents y bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)



# Comandos del bot
hablar = False


@bot.command(name="eco_help")
async def eco_help(ctx):
    await ctx.send(
        '''activate_speech = Enables voice output for all commands
        disable_speech = Disables the <activate_speech> command
        eco_fact = Random fun environmental fact
        recycle_guide (item) = How to recycle a specific item
        carbon_footprint (activity) (amount) = Carbon footprint of an activity
        eco_tip = Random eco-friendly tip
        water_saving_tips = Random water-saving advice
        eco_challenge = Eco-friendly challenge'''
    )


@bot.command(name="ativate_speech")
async def activate_speech(ctx):
    global hablar
    hablar = True
    await ctx.send("The voice is **Activated**")
    speech.read()


@bot.command(name="disable_speech")
async def disable_speech(ctx):
    global hablar
    hablar = False
    await ctx.send("The voice is **Disable**")


@bot.command(name="recycle_guide")
async def recycle_guide(ctx, *, item: str):
    global hablar
    item = item.lower()
    for color, items in cubos().items():
        if item in items:
            text = f"**{item}** should go in the **{color.capitalize()}** container."
            await ctx.send(text)
            if hablar:
                speech.read(text)
            return
  
    text = f"**{item}** should go in the **Gray** container or is not identified."
    await ctx.send(text)
    if hablar:
        speech.read(text)


@bot.command(name = "eco_fact")
async def eco_fact(ctx):
    global hablar
    text = dato()
    await ctx.send(text)
    if hablar:
        speech.read(text)


@bot.command(name = "eco_tip")
async def eco_fact(ctx):
    global hablar
    text = tip()
    await ctx.send(text)
    if hablar:
        speech.read(text)


@bot.command(name="carbon_footprint")
async def carbon_footprint(ctx, actividad: str, cantidad: float):
    global hablar
    try:
        resultado = calcular(actividad, cantidad)
        text = f"Your activity produces approximately **{resultado:.2f} kg de CO₂**."
        await ctx.send(text)
        if hablar:
            speech.read(text)

    except ValueError:
        text = "Unrecognized activity."
        await ctx.send(text)
        if hablar:
            speech.read(text)


bot.command(name="water_saving_tip")
async def water_saving_tip(ctx):
    global hablar
    text = water_tip()
    await ctx.send(text)
    if hablar:
        speech.read(text)


@bot.command(name="eco_challenge")
async def eco_challenge(ctx):
    global hablar
    user_id = str(ctx.author.id)
    today = datetime.date.today()
    year = today.year
    week = today.isocalendar()[1]

    conn = sqlite3.connect("eco_bot.db")
    cursor = conn.cursor()

    
    cursor.execute("SELECT challenge_index FROM user_challenges WHERE user_id=? AND year=? AND week=?", 
                   (user_id, year, week))
    row = cursor.fetchone()

    if row:
        
        challenge_index = row[0]
    else:
        
        cursor.execute("SELECT challenge_index FROM user_challenges WHERE user_id=? AND year=?", (user_id, year))
        used_indices = {r[0] for r in cursor.fetchall()}

        
        available = [i for i in range(len(challenges)) if i not in used_indices]
        if not available:
            text = "🎉 You've completed all eco-challenges this year!"
            await ctx.send(text)
            conn.close()
            if hablar:
                speech.read()
            return

        challenge_index = random.choice(available)

        
        cursor.execute("INSERT INTO user_challenges (user_id, year, week, challenge_index) VALUES (?, ?, ?, ?)",
                       (user_id, year, week, challenge_index))
        conn.commit()

    conn.close()

    text = f"Your eco-challenge for **week {week}**:\n**{challenges[challenge_index]}**"
    await ctx.send(text)
    if hablar:
        speech.read()



#Iniciar el bot
init_db()
bot.run(token)