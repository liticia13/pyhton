import discord, os, json, delete
from discord.ext import commands

# fonction pour sauvegarder les données
def save_data(data, files):            #il les stocks dans un fichier specifie par parametre file 
    with open(files, 'w') as f:
        json.dump(data, f)

# fonction pour charger les données et les renvoyer
def load_data(files):
    with open(files) as f:
        data = json.load(f)
    return data


files = "data.json"
if os.path.isfile(files):  
    data = load_data(files)
    print("Sauvegarde trouvée. Les données ont été chargées.")
else:
    data = {"history": ["command1","command2"], "conversation": ["question1","reponse1","question2","reponse2"]}
    print("Aucune sauvegarde trouvée. Des données vides ont été initialisées.")

class CommandNode:
    def __init__(self, command, prev=None):
        self.command = command
        self.prev = prev

class CommandHistory:
    def __init__(self):
        self.history = {}

    def add_command(self, user_id, command):
        if user_id not in self.history:
            self.history[user_id] = CommandNode(command)
        else:
            self.history[user_id] = CommandNode(command, self.history[user_id])

    def get_last_command(self, user_id):
        if user_id not in self.history:
            return None
        return self.history[user_id].command

    def get_all_commands(self, user_id):
        if user_id not in self.history:
            return []
        commands = []
        node = self.history[user_id]
        while node:
            commands.append(node.command)
            node = node.prev
        return commands

    def get_previous_command(self, user_id):
        if user_id not in self.history:
            return None
        if not self.history[user_id].prev:
            return self.history[user_id].command
        self.history[user_id] = self.history[user_id].prev
        return self.history[user_id].command

    def get_next_command(self, user_id):
        if user_id not in self.history:
            return None
        if not self.history[user_id].prev:
            return self.history[user_id].command
        if not self.history[user_id].prev.prev:
            return self.history[user_id].prev.command
        self.history[user_id] = self.history[user_id].prev
        return self.history[user_id].command

    def clear_history(self, user_id):
        if user_id in self.history:
            self.history[user_id] = None

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents = intents)

history = CommandHistory()

class Node:
    def __init__(self, question, yes_node=None, no_node=None, response=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node
        self.response = response

class BinaryTree:
    def __init__(self, root=None):
        self.root = root

    async def ask_question(self, ctx, node):
      await ctx.send(node.question)
      def check(message):
          return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() in ['yes', 'no']

      try:
          message = await ctx.wait_for('message', check=check, timeout=60.0)
      except asyncio.TimeoutError:
          return await ctx.send('Vous n\'avez pas répondu à temps.')

      answer = message.content.lower()
      if answer == "yes":
          if node.yes_node:
              return await self.ask_question(ctx, node.yes_node)
          else:
              return await ctx.send("Votre réponse est OUI !")
      elif answer == "no":
          if node.no_node:
              return await self.ask_question(ctx, node.no_node)
          else:
              return await ctx.send("Votre réponse est NON !")
      else:
          await ctx.send("Veuillez répondre par OUI ou NON.")
          return await self.ask_question(ctx, node)


# Construction de l'arbre de questions
root = Node("Aimez-vous les aliments épicés ?")
node2 = Node("Aimez-vous les plats mexicains ?", response="Essayez notre burrito mexicain !")
node3 = Node("Aimez-vous les plats indiens ?", response="Essayez notre curry de poulet indien !")
node4 = Node("Aimez-vous les plats asiatiques ?", response="Essayez notre pad thaï !")
node5 = Node("Aimez-vous les plats épicés italiens ?", response="Essayez notre pâtes all'arrabbiata !")

node6 = Node("Aimez-vous les plats épicés à base de viande ?", yes_node=node2, no_node=node3)
node7 = Node("Aimez-vous les plats épicés végétariens ?", yes_node=node4, no_node=node5)

root.yes_node = node6
root.no_node = node7

# Création de l'arbre binaire et association de la racine
tree = BinaryTree(root)

# Fonction pour lancer la conversation
async def start_questionnaire(ctx):
    await ctx.send("Bienvenue dans notre questionnaire sur les préférences alimentaires. Veuillez répondre par OUI ou NON.")
    result = await tree.ask_question(ctx, tree.root)
    await ctx.send(result)

# Commande "food" pour lancer la conversation
@bot.command(name="food")
async def food_command(ctx):
    await start_questionnaire(ctx)

@bot.event
async def on_ready():
    print("Bot is ready")
    

@bot.command()
async def last(ctx):
    last_command = history.get_last_command(ctx.author.id)
    if last_command:
        await ctx.send(f"Your last command was: {last_command}")
    else:
        await ctx.send("You haven't entered any command yet")

@bot.command()
async def all(ctx):
    all_commands = history.get_all_commands(ctx.author.id)
    if all_commands:
        commands_str = "\n".join(all_commands)
        await ctx.send(f"Your command history:\n{commands_str}")
    else:
        await ctx.send("You haven't entered any command yet")

@bot.command(name="arr")
async def prev(ctx):
    previous_command = history.get_previous_command(ctx.author.id)
    if previous_command:
        await ctx.send(f"Your previous command was: {previous_command}")
    else:
        await ctx.send("You are already at the beginning of your command history")

@bot.command(name="avc")
async def next(ctx):
    next_command = history.get_next_command(ctx.author.id)
    if next_command:
        await ctx.send(f"Your next command was: {next_command}")
    else:
        await ctx.send("You are already at the ending of your command history")

@bot.command(name="sup")
async def clear_history(ctx):
    history.clear_history(ctx.author.id)
    await ctx.send("Your command history has been cleared")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")
    history.add_command(ctx.author.id, "hello")
    
@bot.command()
async def test(ctx):
    await ctx.send("test, world!")
    history.add_command(ctx.author.id, "test")
    
    # Fonction pour supprimer les messages automatiquement 
@bot.event                                           #si je la mets pas en commentaires les autres fonctions marchent pas i
async def on_message(message):
     if  str (message.channel) == "general" and message.content !="":
       await message.channel.purge(limit=1)
        


bot.run("MTA5MTI2MDgxNzc0NTM3OTM1MA.GY4pw3.-dfMGJwioIFkEzxENAzEBjbc1I5jkdtORZoh8I")
# save
save_data(data, files)


 

