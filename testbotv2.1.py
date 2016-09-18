import logging, discord, asyncio, re, random, os

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:\
                                       %(message)s'))
logger.addHandler(handler)

client = discord.Client()
users = {}

@client.event
async def on_member_update(before, after):
    try:
        if repr(after.status) == '<Status.offline: \'offline\'>':
            users[str(after)] = False
        elif repr(after.status) == '<Status.online: \'online\'>':
            users[str(after)] = True
    except KeyError as e:
        pass

@client.event
async def on_ready():
    for i in client.get_all_members():
        if repr(i.status) == '<Status.offline: \'offline\'>':
            users[str(i)] = False
        elif repr(i.status) == '<Status.online: \'online\'>':
            users[str(i)] = True
    for i in client.get_all_channels():
        client.send_message(i, 'YuiBot powerup complete, Hello {}'.format(i))


@client.event
async def on_message(message):
    await checks(message)

@asyncio.coroutine
async def checks(message):
    if message.author != 'YuiBot#6311':
        if message.content == '!off':
                users[message.author] = False
        elif message.content.startswith('!state ') == True:
            users[message.author] = True
            if message.mentions == []:
                await client.send_message(
                    message.channel,
                    '!state requires at least one user to find the state of')
            else:
                print(len(list(message.mentions)))
                for i in message.mentions:
                    try:
                        if users[str(i)] == True:
                            await client.send_message(
                                message.channel,
                                '{} is online, they\'re probably being a bitch then...'.format(
                                    str(i)))
                        elif users[str(i)] == False:
                            await client.send_message(
                                message.channel,
                                '{} is not online, oh well...'.format(
                                    str(i)))
                        else:
                            await client.send_message(
                                message.channel,
                                'ummm...I\'m not quite sure to be honest...maybe they\'re dead?')
                    except KeyError as e:
                        await client.send_message(
                            message.channel,
                            'Sorry, i don\'t think i know the user "{}".'.format(
                                str(i)))
        elif message.content.startswith('!img '):
            try:
                print('img')
                await client.send_file(message.channel, loc)
            except:
                await client.send_message(
                    message.channel,
                    'Sorry, i couldn\'t find that file.')
        elif message.content == '!sleep':
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Sleep done')
        elif message.content.startswith('!dice '):
            sides = message.content[6:]
            await client.send_message(
                message.channel,
                '{} roles a {} sided dice, they got: {}'.format(
                    message.author, sides, random.randint(1, int(sides))))
        elif message.content == '!help':
            await client.send_message(message.channel, 'List of commands:\n\!dice [sides]: rolls a dice of [sides] sides\n\!img [file1] [file2] [filename]: sends a image from a folder the bot contains\n\!sleep: makes the bot sleep for 5 seconds\n\!help: sends this message\n!state @[name]: replies with the state of the selected user/s')
        else:
            users[message.author] = False

def test_keys(keys, string):
    count = 0
    for i in keys:
        if i in string:
            count += 1
    return count

def cut_files(fileDict, count):
    upperDict, lowerDict = {},{}

    for i, c in fileDict.items():
        if fileDict[i] > count:
            upperDict[i] = c
        else:
            lowerDict[i] = c
    return upperDict, lowerDict


def find_file(keys = [], directory = '', ftypes = [], matchRate = 0):
    ''' keys = strings to have in filename
    directory = location to search in
    ftypes = filetypes (including preceeding period, ie: .png)
    matchRate = minimum matches to consider

    returns:
    either: a random file that meets criteria
    or: None (when no file found)
    '''
    validFiles = {}
    # format: {filename: match count,}

    if matchRate > len(keys): matchRate = len(keys)
    for file in os.listdir(directory):
        if os.path.splitext(file)[1] in ftypes:
            fCount = test_keys(keys, file)
            if fCount:
                validFiles[file] = fCount
    if validFiles:
        for i in range(matchRate):
            upper, lower = cut_files(validFiles, i)
            if not upper: # no more files with more matches
                return random.choice(list(lower.keys()))
            else:
                validFiles = upper
        return random.choice(list(upper.keys()))

pattern1 = re.compile('!img * * *')
client.run('')
