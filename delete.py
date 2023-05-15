import discord
from discord.ext import commands
 #supprimer les messages 

def add_event_message_suprimer(bot : commands.Bot):

    #Le bot aura la l'event on_message_delete

    @bot.event
    async def on_message_delete(message):
        print("Un message a été supprimé.")
        # print(f"Contenu du message : {message.content}")
    
    return Description

Description = (
    "\n> **on_message_delete**:\n>\t- Quand un message est supprimé. \"**Un message a été supprimé.**\" sera affiché dans le serveur de YassBot."
)