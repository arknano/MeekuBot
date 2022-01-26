import random
import asyncio
import markovify
from functions.data import *
import sqlite3 as sql

config = load_bot_config()
db = sql.connect(config['chatlogDB'])
with db:
    cursor = db.cursor()
    db.execute("""
        CREATE TABLE IF NOT EXISTS chatlog (
            id integer NOT NULL,
            nick text NOT NULL,
            message text NOT NULL
        );
    """)
    cursor.execute("SELECT * FROM chatlog")
    data = cursor.fetchall()
    markovlines = ""
    line_count = 0
    for row in data:
        markovlines += "\n" + row[2] + ""
        line_count += 1
    print(f'Processed {line_count} lines in chat history.')
    markov_instance = markovify.NewlineText(markovlines, state_size=1)

def sponge_mock(input_text):
    output_text = ""
    for char in input_text:
        if char.isalpha():
            if random.random() > 0.5:
                output_text += char.upper()
            else:
                output_text += char.lower()
        else:
            output_text += char
    return output_text


async def type_nonsense(ctx):
    text = markov()
    async with ctx.channel.typing():
        await asyncio.sleep(len(text) * 0.05)
    return text

def markov():
    string = markov_instance.make_sentence(min_words=config['minMarkovWords'], max_words=config['maxMarkovWords'],
                                     max_overlap_ratio=config['markovOverlapRatio'], tries=100)
    return string.capitalize()