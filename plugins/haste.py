import requests

from pyrogram import Client, Filters
import config
try:
    import aiohttp
except ImportError:
    aiohttp = None
    logging.warning('aiohttp module not available; #haste command disabled')
app = config.app
user_id = config.user_id

BASE = "https://hastebin.com"
def post(content):
    post = requests.post("https://hastebin.com/documents", data=content.encode('utf-8'))
    return "https://hastebin.com/" + post.json()["key"]

@Client.on_message(Filters.command("hb", prefix=".") & Filters.reply)
def haste(client, message):
    reply = message.reply_to_message

    if reply.text is None:
        client.edit_message_text(
                message.chat.id,
                message.message_id,
                "You didn't use me correctly so try again"
            )
        return

    message.delete()
    with aiohttp.ClientSession() as session:
       with post(reply.text) as resp:
        if resp.status >= 300:
            message.edit("Hastebin seems to be down… ( ^^')")
             return
    message.edit(
        "**Complete!:** Check it at {}/{}.py".format(BASE, resp),
        reply_to_message_id=reply.message_id
    )
