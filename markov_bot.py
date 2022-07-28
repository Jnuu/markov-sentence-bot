import discord
from markov import make_model, make_sentence

token = open("./token.txt", 'r').read()
intents = discord.Intents.all()

client = discord.Client(intents=intents)

commands = ["/", "!", "$"]


@client.event
async def on_ready():
    print(f'{client.user}としてログインしました！')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("/markov"):
        args = message.content.split()
        channel = message.channel

        #helpの表示
        if len(args) == 1 or args[1] == "-h":
            help = "```/markov [@username] Optional:[Num of acquisitions]```"
            await channel.send(help)

        else:
            lim = None
            for arg in args:
                if (arg[0] not in commands and arg[0] != '@' 
                    and arg.isdecimal()):
                    lim = int(arg)

            messages = []
            channel = message.channel
            memberIDs = [user.id for user in message.mentions]
            async for old_msg in channel.history(limit=lim):
                if old_msg.author.id in memberIDs:
                    if not old_msg.content:
                        continue
                    elif old_msg.content[0] not in commands:
                        messages += [old_msg.content]
            
            msg = "```ERROR：文章を生成できませんでした```"
            if messages != []:
                model = make_model(messages)
                msg = make_sentence(model)
                
            print(msg)
            await channel.send(msg)

client.run(token)
